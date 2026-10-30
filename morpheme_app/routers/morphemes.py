from fastapi import FastAPI, APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from ..schemas.schemas import MorphemeRequest,MorphemeeRequest, MorphemeResponse, WordResponse, WordGroupsResponse, MorphemesRequest, WordGroupssResponse, MorphemeeRequest, WordData, MainWordResponse, SubGroupResponse, GroupResponse, MorphemeData
from ..config.db_config import get_db
import logging
from ..models.MorphemeDetailNew_model import MorphemeDetailNew
from ..models.Word_model import Word
from ..utils.utils import (
    get_morpheme_details,
    get_words_by_morpheme_detail,
    get_existing_root_word_ids,
    get_quranic_data,
)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
morphemes_router = APIRouter(prefix="/api", tags=["Morphemes"])
@morphemes_router.post("/new-get", response_model=dict)
def get_words_by_group(request: MorphemeRequest, db: Session = Depends(get_db)):
    """Fetch words by group based on root word and provided data."""
    quranic_data = get_quranic_data()
    root_word_id = next(
        (rw["id"] for rw in quranic_data["rootWords"] if rw["englishRootWord"] == request.rootWord),
        None,
    )

    if not root_word_id:
        raise HTTPException(status_code=422, detail="Invalid root word")

    result_list = []

    for data_item in request.data:
        morpheme_details = get_morpheme_details(
            db=db,
            root_word_id=root_word_id,
            weight=data_item.weight,
            morpheme_no=data_item.morpheme_no,
        )

        if morpheme_details:
            for morpheme_detail in morpheme_details:
                words = get_words_by_morpheme_detail(
                    db=db,
                    morpheme_detail_id=morpheme_detail.id,
                    word_number=data_item.word_number,
                )

                for word in words:
                    result_list.append({
                        "morpheme_no": morpheme_detail.morpheme_no,
                        "weight": morpheme_detail.weight,
                        "word": word.word if word.word else "",
                        "group": str(word.group),
                        "subgroup": str(word.subgroup),
                        "word_number": str(word.word_number),
                        "isbroken": bool(word.isbroken),
                        "broken_plurals": [],
                        "template": word.template.template_text if word.template else "",
                        "ar": word.heading.ar if word.heading else "",
                        "en": word.heading.en if word.heading else "",
                        "sub_ar": word.subheading.sub_ar if word.subheading else "",
                        "sub_en": word.subheading.sub_en if word.subheading else "",
                        "reference": False,
                        "word_id": word.id if word.id else None,
                        "matchingWords": [],
                    })

    return {
        "success": True,
        "message": "Words data Retrieved Successfully",
        "list": result_list,
    }


@morphemes_router.get("/get-root-words", response_model=dict)
def get_root_words(db: Session = Depends(get_db)):
    """Fetch root words along with existing flags."""
    try:
        existing_root_word_ids = get_existing_root_word_ids(db)
        existing_root_word_ids = [rw[0] for rw in existing_root_word_ids]

        result = get_quranic_data()
        root_words = result["rootWords"]

        list_response = []
        if root_words:
            for value in root_words:
                list_response.append({
                    "id": value["id"],
                    "englishWord": value["englishRootWord"],
                    "rootWord": value["rootWord"],
                    "seperateRootWord": value["seprateRootWord"],
                    "isExist": value["id"] in existing_root_word_ids,
                })

        return {
            "success": True,
            "message": "Root Word Data Retrieved Successfully",
            "list": list_response,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving root words: {str(e)}")


@morphemes_router.post("/get-morphemes", response_model=MorphemeResponse)
def get_morphemes(morpheme_request: MorphemesRequest, db: Session = Depends(get_db)):
    """Endpoint to get morphemes based on the provided root word."""
    try:
        # Extract root word from the request
        root_word = morpheme_request.rootWord.strip()
        quranic_data = get_quranic_data()
        root_words_list = quranic_data['rootWords']

        # Find the root word ID
        root_word_id = next(
            (rw['id'] for rw in root_words_list if rw['englishRootWord'].lower() == root_word.lower()), 
            None
        )

        if root_word_id is None:
            raise HTTPException(status_code=404, detail="Root word not found.")

        # Query morpheme details associated with the root word
        result = db.query(MorphemeDetailNew).filter_by(root_word_id=root_word_id).all()
        list_response = []

        for md in result:
            # Query words associated with each morpheme detail
            words = db.query(Word).filter_by(morpheme_detail_id=md.id).all()

            for word in words:
                # Check if the word has an ID and define 'reference'
                word_id_list = [word.id] if word.id else []
                reference = bool(word.id)

                # Safe handling of broken plurals
                broken_plurals = []
                if word.isbroken and word.broken_plurals:
                    first_broken_plural = word.broken_plurals[0].broken_plural if word.broken_plurals else None
                    if first_broken_plural:
                        broken_plurals = {
                            "word": first_broken_plural.word or "",
                            "template": first_broken_plural.template.template_text if first_broken_plural.template else "",
                            "references": [str(word.word_number)],
                        }

                # Append data to the response list
                list_response.append({
                    "morpheme_no": md.morpheme_no,
                    "weight": md.weight,
                    "word": word.word or "",
                    "group": str(word.group),
                    "subgroup": str(word.subgroup),
                    "word_number": str(word.word_number),
                    "isbroken": bool(word.isbroken),
                    "broken_plurals": broken_plurals,
                    "template": word.template.template_text if word.template else "",
                    "ar": word.heading.ar if word.heading else "",
                    "en": word.heading.en if word.heading else "",
                    "sub_ar": word.subheading.sub_ar if word.subheading else "",
                    "sub_en": word.subheading.sub_en if word.subheading else "",
                    "reference": reference,  # Properly defined here
                    "word_id": word_id_list,
                    "matchingWords": [
                        {
                            "wordId": word.id,
                            "reference": f"{word.group}:{word.subgroup}:{word.word_number}"
                        }
                    ] if reference else []
                })

        return {
            "success": True,
            "message": "Morphemes Data Retrieved Successfully",
            "totalRecords": len(list_response),
            "list": list_response
        }

    except Exception as e:
        # Catch and return any exception as an HTTPException
        raise HTTPException(status_code=500, detail=f"Error retrieving morphemes: {str(e)}")


@morphemes_router.post("/words-by-groups-only", response_model=WordGroupsResponse)
def get_word_by_groups_only(request: MorphemeeRequest, db: Session = Depends(get_db)):
    """Fetch words grouped by their categories."""
    try:
        root_word = request.rootWord.strip()
        quranic_data = get_quranic_data()
        root_word_id = next(
            (rw["id"] for rw in quranic_data["rootWords"] if rw["englishRootWord"].lower() == root_word.lower()),
            None,
        )

        if not root_word_id:
            raise HTTPException(status_code=404, detail="Root word not found")

        morphemes = get_morpheme_details(db, root_word_id)

        grouped_words = {}
        for morpheme in morphemes:
            words = get_words_by_morpheme_detail(db, morpheme.id)
            for word in words:
                group_key = f"Group {word.group}"
                if group_key not in grouped_words:
                    grouped_words[group_key] = []

                # Handle the 'broken_plurals' field properly
                broken_plurals = [
                    broken_plural.broken_plural.word for broken_plural in word.broken_plurals
                ] if word.broken_plurals else []

                # Handle 'reference' as a string
                reference = str(bool(word.id))  # Convert boolean to string ("True" or "False")

                # Create the WordResponse object for each word
                word_response = WordResponse(
                    morpheme_no=word.morpheme_no,
                    weight=word.weight,
                    word=word.word,
                    group=str(word.group),
                    subgroup=str(word.subgroup),
                    word_number=str(word.word_number),
                    isbroken=bool(word.isbroken),
                    broken_plurals=broken_plurals,  # Ensure broken_plurals is a list of strings
                    template=word.template.template_text if word.template else "",
                    ar=word.heading.ar if word.heading else "",
                    en=word.heading.en if word.heading else "",
                    sub_ar=word.subheading.sub_ar if word.subheading else "",
                    sub_en=word.subheading.sub_en if word.subheading else "",
                    reference=reference,  # Now a string, not a boolean
                    word_id=word.id,
                    matchingWords=[
                        {
                            "wordId": word.id,
                            "reference": f"{word.group}:{word.subgroup}:{word.word_number}"
                        }
                    ] if word.id else [],
                )
                grouped_words[group_key].append(word_response)

        # Format the response to include a list of groups
        list_response = [{"key": key, "words": word_list} for key, word_list in grouped_words.items()]

        return {
            "success": True,
            "message": "Words grouped successfully",
            "list": list_response,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error grouping words: {str(e)}")



@morphemes_router.post("/words-by-groups", response_model=WordGroupssResponse)
def get_words_by_groups(request: MorphemeeRequest = Body(...), db: Session = Depends(get_db)):
    try:
        # Fetch Quranic data and root word logic remains the same
        quranic_data = get_quranic_data()
        root_words_list = quranic_data.get('rootWords', [])
        root_word = request.rootWord.strip()

        root_word_id = next(
            (rw['id'] for rw in root_words_list if rw['englishRootWord'].lower() == root_word.lower()),
            None
        )
        if not root_word_id:
            raise HTTPException(status_code=404, detail="Root word not found.")

        morphemes = db.query(MorphemeDetailNew).filter_by(root_word_id=root_word_id).all()
        if not morphemes:
            raise HTTPException(status_code=404, detail="No morphemes found for the given root word.")

        response_list = []

        for morpheme in morphemes:
            morpheme_form = morpheme.form or ""
            weight = f"Weight {morpheme.weight}"
            words = db.query(Word).filter_by(morpheme_detail_id=morpheme.id).all()

            groups_dict = {}

            for word in words:
                group_key = f"Group {word.group}"
                subgroup_key = f"Subgroup {word.subgroup}"

                if group_key not in groups_dict:
                    groups_dict[group_key] = GroupResponse(
                        key=group_key,
                        isReferenceExist=False,
                        subGroups=[]
                    )

                subgroup = next(
                    (sg for sg in groups_dict[group_key].subGroups if sg.key == subgroup_key),
                    None
                )
                if not subgroup:
                    subgroup = SubGroupResponse(
                        key=subgroup_key,
                        referenceWordCount=0,
                        arabicHeading=word.heading.ar if word.heading else "",
                        englishHeading=word.heading.en if word.heading else "",
                        mainWords=[]
                    )
                    groups_dict[group_key].subGroups.append(subgroup)

                main_word_key = f"{word.word_number}"
                main_word = next(
                    (mw for mw in subgroup.mainWords if mw.key == main_word_key),
                    None
                )
                if not main_word:
                    main_word = MainWordResponse(
                        key=main_word_key,
                        arabicHeading=word.subheading.sub_ar if word.subheading else "",
                        englishHeading=word.subheading.sub_en if word.subheading else "",
                        words=[]
                    )
                    subgroup.mainWords.append(main_word)

                main_word.words.append(WordData(
                    morpheme_no=morpheme.morpheme_no,
                    weight=morpheme.weight,
                    word=word.word or "",
                    group=str(word.group) if word.group else "",
                    subgroup=str(word.subgroup) if word.subgroup else "",
                    word_number=str(word.word_number) if word.word_number else "",
                    isbroken=bool(word.isbroken),
                    broken_plurals=[bp.broken_plural.word for bp in word.broken_plurals] if word.broken_plurals else [],
                    template=word.template.template_text if word.template else "",
                    ar=word.heading.ar if word.heading else "",
                    en=word.heading.en if word.heading else "",
                    sub_ar=word.subheading.sub_ar if word.subheading else "",
                    sub_en=word.subheading.sub_en if word.subheading else "",
                    reference=str(bool(word.id)),
                    word_id=word.id,
                    matchingWords=[],
                ))

            # Sorting groups and subgroups
            groups_response = sorted(
                groups_dict.values(),
                key=lambda g: int(g.key.split()[1]) if g.key.split()[1].isdigit() else float('inf')
            )
            for group in groups_response:
                group.subGroups = sorted(
                    group.subGroups,
                    key=lambda sg: tuple(map(float, sg.key.split()[1].split('.'))) if sg.key.split()[1].replace('.', '', 1).isdigit() else (float('inf'),)
                )

            response_list.append(MorphemeData(
                weight=weight,
                morphemeForm=morpheme_form,
                isReferenceExist=any(
                    w.reference
                    for g in groups_response
                    for s in g.subGroups
                    for mw in s.mainWords
                    for w in mw.words
                ),
                groups=groups_response
            ))

        return WordGroupssResponse(
            success=True,
            message="Words data retrieved successfully",
            list=response_list
        )

    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

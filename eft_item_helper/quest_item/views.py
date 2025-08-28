from fastapi import APIRouter

from eft_item_helper.dependencies import SessionDep
from eft_item_helper.quest_item.schemas import (
    ItemWithDetailSchema,
    ItemWithDetailAndQuestsSchema,
)
from eft_item_helper.quest_item.services import (
    get_all_items_with_detail,
    get_all_items_with_detail_and_quests,
)


router = APIRouter(prefix="/quest-item", tags=["quest-item"])


@router.get("/items/")
async def get_items_with_detail(
    session: SessionDep,
) -> list[ItemWithDetailSchema]:
    """
    Возвращает список квестовых предметов с их деталями
    """
    return await get_all_items_with_detail(session)


@router.get("/items-with-quests/")
async def get_items_with_quest_and_detail(
    session: SessionDep,
) -> list[ItemWithDetailAndQuestsSchema]:
    """
    Возвращает список квестовых предметов с их деталями
    и квестами в которых они используются
    """
    return await get_all_items_with_detail_and_quests(session)

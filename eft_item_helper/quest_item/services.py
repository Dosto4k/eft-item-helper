from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from db import engine
from item.services import parse_traders_urls, parse_quests_urls
from item.models import Item
from item.schemas import ParsedQuestItem, ParsedQuest
from quest_item.models import QuestItemDetail, Quest, QuestItemAssociation
from quest_item.schemas import ItemWithDetailSchema, ItemWithDetailAndQuestsSchema


def fill_db_tables_related_quests_items() -> None:
    """
    Заполняет таблицы бд связанные с квестовыми предметами данными
    """
    parsed_quest_urls = parse_traders_urls()
    parsed_items = parse_quests_urls(parsed_quest_urls)
    with Session(engine) as session:
        for parsed_item in parsed_items:
            item = _get_item_with_detail_by_name_or_none(parsed_item.name, session)
            if item is None:
                item = _create_item_with_detail(parsed_item)
            for parsed_quest in parsed_item.quests:
                quest = _get_quest_by_name_or_none(parsed_quest.name, session)
                if quest is None:
                    quest = _create_quest(parsed_quest)
                if _quest_item_association_is_exists(item, quest, session):
                    continue
                quest_item_association = QuestItemAssociation(
                    total_count=parsed_quest.total_count,
                    found_in_raid=parsed_quest.found_in_raid,
                )
                quest_item_association.quest = quest
                item.quests.append(quest_item_association)
            session.add(item)
            session.commit()


def _quest_item_association_is_exists(
    item: Item, quest: Quest, session: Session
) -> bool:
    """
    Проверяет существует ли ассоциативная таблица quest_item для переданных item и quest
    """
    if item.id is None or quest.id is None:
        return False
    association_obj = session.execute(
        select(QuestItemAssociation)
        .where(QuestItemAssociation.item_id == item.id)
        .where(QuestItemAssociation.quest_id == quest.id)
    ).scalar_one_or_none()
    return bool(association_obj)


def _get_quest_by_name_or_none(name: str, session: Session) -> Quest | None:
    """
    Возвращает объект Quest или None если объект Quest не существует
    """
    return session.execute(select(Quest).where(Quest.name == name)).scalar_one_or_none()


def _create_quest(quest_data: ParsedQuest) -> Quest:
    """
    Создаёт объект Quest
    """
    return Quest(
        name=quest_data.name,
        guide_url=quest_data.guide_url,
    )


def _get_item_with_detail_by_name_or_none(name: str, session: Session) -> Item | None:
    """
    Возвращает объект Item или None если объект Item не существует
    """
    return session.execute(
        select(Item).where(Item.name == name).options(joinedload(Item.detail))
    ).scalar_one_or_none()


def _create_item_with_detail(item_data: ParsedQuestItem) -> Item:
    """
    Создаёт объект Item
    """
    item = Item(name=item_data.name)
    item.detail = QuestItemDetail(
        total_count=item_data.total_count,
        count_of_found_in_raid=item_data.count_of_found_in_raid,
    )
    return item


async def get_all_items_with_detail(session: Session) -> list[ItemWithDetailSchema]:
    """
    Получает все квестовые предметы с их деталями
    """
    items_objects = session.execute(
        select(Item).options(joinedload(Item.detail))
    ).scalars()
    items_schemas = []
    for item_object in items_objects:
        item_schema = ItemWithDetailSchema.model_validate(
            item_object,
            from_attributes=True,
        )
        items_schemas.append(item_schema)
    return items_schemas


async def get_all_items_with_detail_and_quests(
    session: Session,
) -> list[ItemWithDetailAndQuestsSchema]:
    """
    Получает все квестовые предметы с их деталями и квестами в которых они используются
    """
    items_objects = session.execute(
        select(Item).options(
            joinedload(Item.detail),
            selectinload(Item.quests).joinedload(QuestItemAssociation.quest),
        )
    ).scalars()
    items_schemas = []
    for item_object in items_objects:
        item_schema = ItemWithDetailAndQuestsSchema.model_validate(
            item_object,
            from_attributes=True,
        )
        items_schemas.append(item_schema)
    return items_schemas

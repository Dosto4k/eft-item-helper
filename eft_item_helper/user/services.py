from sqlalchemy import select
from sqlalchemy.orm import Session

from auth.schemas import RegisterCredentials
from auth.utils import get_pw_hash
from user.models import User, UserItemQuestAssociation
from item.models import Item
from quest_item.models import QuestItemDetail


async def create_user_and_add_quest_items(
    user_data: RegisterCredentials, session: Session
) -> None:
    """
    Создаёт объект User и связывает его с квестовыми предметами
    """
    user_object = User(
        username=user_data.username, password=await get_pw_hash(user_data.password)
    )
    items_objects = session.execute(select(Item).join(QuestItemDetail)).scalars().all()
    for item_object in items_objects:
        user_item_association = UserItemQuestAssociation(
            found_in_raid=0, found_not_in_raid=0
        )
        user_item_association.item = item_object
        user_object.items.append(user_item_association)
    session.add(user_object)
    session.commit()

from pydantic import BaseModel as BaseSchema
from pydantic_string_url import HttpUrl

from eft_item_helper.item.schemas import ItemSchema


class DetailSchema(BaseSchema):
    total_count: int
    count_of_found_in_raid: int


class ItemWithDetailSchema(ItemSchema):
    detail: DetailSchema


class QuestSchema(BaseSchema):
    name: str
    guide_url: HttpUrl


class QuestItemSchema(BaseSchema):
    quest: QuestSchema
    total_count: int
    found_in_raid: bool


class ItemWithDetailAndQuestsSchema(ItemWithDetailSchema):
    quests: list[QuestItemSchema]

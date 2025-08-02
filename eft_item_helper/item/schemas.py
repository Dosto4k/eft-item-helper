from pydantic import BaseModel as BaseSchema
from pydantic_string_url import HttpUrl


class ParsedQuestUrls(BaseSchema):
    quest_name: str
    guide_url: HttpUrl
    info_url: HttpUrl


class ParsedQuest(BaseSchema):
    name: str
    guide_url: HttpUrl
    total_count: int
    found_in_raid: bool


class ParsedQuestItem(BaseSchema):
    name: str
    total_count: int
    count_of_found_in_raid: int
    quests: list[ParsedQuest]


class ItemSchema(BaseSchema):
    id: int
    name: str

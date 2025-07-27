import requests
from tqdm import tqdm

from config import TRADERS
from schemas import ParsedQuestUrls, ParsedQuest, ParsedQuestItem


def parse_traders_urls() -> list[ParsedQuestUrls]:
    '''
    Парсит TRADERS и собирает ссылки на квесты торговцев
    '''
    quests_urls = []
    for trader in TRADERS:
        response = requests.get(trader['url'], timeout=5)
        response.raise_for_status()
        quests = response.json()['data']
        print(f'Получаем ссылки на квесты торговца \'{trader["name"]}\'.')
        for quest in tqdm(quests):
            seo_link = quest['seo_link']
            quests_urls.append(ParsedQuestUrls(
                quest_name=quest['name'], 
                guide_url=f'https://tarkov.help/ru/quest/{seo_link}',  # type: ignore
                info_url=f'https://api.tarkov.help/api/ru/quests/{seo_link}' # type: ignore
            ))
    return quests_urls


def parse_quests_urls(quests_urls: list[ParsedQuestUrls]) -> list[ParsedQuestItem]:
    """
    Парсит quests_urls и получает информацию о предметах и 
    квестах в которых они используются
    """
    items = {}
    print('Парсим квесты.')
    for quest_url in tqdm(quests_urls):
        response = requests.get(quest_url.info_url, timeout=5)
        if response.status_code == 404:
            continue
        item_goals = response.json()['data']['item_goals']
        for item_goal in item_goals:
            name = item_goal['item']['name']
            total_count = item_goal['count']
            count_of_found_in_raid = item_goal['count'] if item_goal['found_in_raid'] else 0
            quest = ParsedQuest(
                name=quest_url.quest_name,
                guide_url=quest_url.guide_url,
                total_count=total_count,
                found_in_raid=bool(count_of_found_in_raid)
            )
            if item := items.get(name):
                item.total_count += total_count
                item.count_of_found_in_raid += count_of_found_in_raid
                item.quests.append(quest)
            else:
                items[name] = ParsedQuestItem(
                    name=name,
                    total_count=total_count,
                    count_of_found_in_raid=count_of_found_in_raid,
                    quests=[quest]
                )  
    return list(items.values())

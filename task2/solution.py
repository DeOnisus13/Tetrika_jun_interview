"""
Выбрал подход с использованием API Wikipedia, что удобнее и проще, чем парсинг html-страницы.
"""
import asyncio
import csv
import re
from collections import Counter

import aiohttp

WIKI_API_URL = "https://ru.wikipedia.org/w/api.php"


async def fetch_category_members(session, category, cmcontinue=None):
    """Получает страницы из категории."""
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": category,
        "cmlimit": "max",
        "format": "json",
    }
    if cmcontinue:
        params["cmcontinue"] = cmcontinue

    async with session.get(WIKI_API_URL, params=params) as response:
        return await response.json()


async def get_all_animals():
    """Собирает все элементы из категории 'Животные по алфавиту'."""
    animals_counter = Counter()
    async with aiohttp.ClientSession() as session:
        category = "Категория:Животные_по_алфавиту"
        cmcontinue = None

        while True:
            data = await fetch_category_members(session, category, cmcontinue)
            members = data["query"]["categorymembers"]

            for member in members:
                # Обновляем счетчик по первой букве названия
                first_char = member["title"][0]
                if first_char == "Ё":
                    first_char = "Е"
                if not re.match(r'[А-Яа-яЁё]', first_char):
                    return animals_counter
                animals_counter[first_char] += 1
            # Проверяем, есть ли следующая страница
            cmcontinue = data.get("continue", {}).get("cmcontinue")
            if not cmcontinue:
                break

    return animals_counter


def write_data(data: list):
    """Функция записи данных в .csv файл."""
    with open('beasts.csv', 'w+', newline='') as csvfile:
        csvfile.truncate()
        writer = csv.writer(csvfile)
        writer.writerows(data)


async def main():
    """Основная функция для запуска."""
    print("Начато выполнение программы. Подождите...")
    animals_counter = await get_all_animals()
    total = animals_counter.total()
    print(f"Всего животных в категориях: {total}")
    write_data(sorted(animals_counter.items()))
    print("Запись в файл успешна.")


if __name__ == "__main__":
    asyncio.run(main())

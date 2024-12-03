import pytest
import aiohttp
from unittest.mock import patch
from collections import Counter
from aioresponses import aioresponses

from task2.solution import fetch_category_members, get_all_animals

WIKI_API_URL = "https://ru.wikipedia.org/w/api.php"


@pytest.mark.asyncio
async def test_fetch_category_members():
    """Тестирование получения данных из категории."""

    # Мок ответ с использованием aioresponses
    mock_response = {
        "query": {
            "categorymembers": [
                {"title": "Кролик"},
                {"title": "Черепаха"},
            ]
        }
    }

    # Формируем URL с параметрами
    mock_url = (f"{WIKI_API_URL}?action=query&list=categorymembers&cmtitle=Категория:Животные_по_алфавиту&"
                f"cmlimit=max&format=json")

    # Используем aioresponses для мока
    with aioresponses() as m:
        # Мокаем только нужный запрос с правильным URL
        m.get(mock_url, payload=mock_response)

        # Запускаем функцию с реальной сессией, но запрос будет замокан
        async with aiohttp.ClientSession() as session:
            result = await fetch_category_members(session, "Категория:Животные_по_алфавиту")

    # Проверяем результат
    assert result == mock_response


@pytest.mark.asyncio
async def test_get_all_animals():
    """Тестирование сбора всех животных."""
    mock_responses = [
        {
            "query": {
                "categorymembers": [
                    {"title": "Альпака"},
                    {"title": "Буйвол"},
                    {"title": "Крокодил"},
                ]
            },
            "continue": {"cmcontinue": "next_page_token"},
        },
        {
            "query": {
                "categorymembers": [
                    {"title": "Жираф"},
                    {"title": "Elephant"},  # Латинская буква прерывает выполнение
                ]
            }
        }
    ]

    async def mock_fetch_category_members(session, category, cmcontinue=None):
        if cmcontinue == "next_page_token":
            return mock_responses[1]
        return mock_responses[0]

    with patch("task2.solution.fetch_category_members", new=mock_fetch_category_members):
        animals_counter = await get_all_animals()

    assert animals_counter == Counter({"А": 1, "Б": 1, "Ж": 1, "К": 1})

from typing import Any
from aiogram.types import CallbackQuery, Message
import json
# from services.parser import table_parse


# Фунция для обрезания ссылки до удоборимого варианта
# Например, https://journal.tinkoff.ru/flows/economics/ -- journal.tinkoff
def cut_url(url: str):
    # Делим ссылку на части, чтобы они не были равны пустому символу
    cropped_url = [item for item in url.split('/') if item != '']
    # Достаем из ссылки доменное имя исключая домен первого уровня
    cropped_url = '_'.join(cropped_url[1].split('.')[:-1]).strip()
    return cropped_url


# Save to Json
def save_json_file(data) -> None:
    with open('data/users.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# Append to Json file
def append_to_file(data) -> None:
    with open('data/users.json', 'a', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# Load from json
def load_from_file():
    with open('data/users.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        if data == None:
            return {}
        return data

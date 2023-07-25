from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_RU
from services.parser import table_parse
from services.services import load_from_file, save_json_file


button_rbc: InlineKeyboardButton = InlineKeyboardButton(
    text='rbc.ru',
    callback_data='rbc_pressed')

button_tinkoff: InlineKeyboardButton = InlineKeyboardButton(
    text='journal.tinkoff.ru',
    callback_data='tinkoff_pressed')

button_rb: InlineKeyboardButton = InlineKeyboardButton(
    text='rb.ru',
    callback_data='pressed_rb')

button_kommersant: InlineKeyboardButton = InlineKeyboardButton(
    text='komersant.ru',
    callback_data='pressed_kommersant')

button_skillbox: InlineKeyboardButton = InlineKeyboardButton(
    text='skillbox.ru',
    callback_data='pressed_skillbox')

button_start_customize: InlineKeyboardButton = InlineKeyboardButton(
    text='Начать настройку',
    callback_data='pressed_start_customize')

button_next_step: InlineKeyboardButton = InlineKeyboardButton(
    text='Следующий шаг',
    callback_data='pressed_next_step')


# Keyboards
keyboard_start_customize: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_start_customize]])


def Built_keyboard_choose_sites(user_id: str):
    buttons: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    users = load_from_file()
    
    for key in table_parse.keys():
        if f'pressed_button_{key}' in users[str(user_id)]['pressed_sites'].keys():
            buttons.append(InlineKeyboardButton(
                text=key + '✅',
                callback_data=f'pressed_button_{key}'))
        else:    
            buttons.append(InlineKeyboardButton(
                text=key + '❌',
                callback_data=f'pressed_button_{key}'))

    kb_builder.add(*buttons)
    kb_builder.adjust(1)
    kb_builder.row(button_next_step)
    return kb_builder

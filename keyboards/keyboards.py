from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_RU, COLLEGE_SCHEDULE


#Создаем объект строителя клавиатур KeyboardBuilder
missing_list_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

#Создаем кнопки клавиатур
button_missing_list: InlineKeyboardButton = InlineKeyboardButton(
    text='Список отсутствующих',
    callback_data='missing_list_pressed')
button_statement: InlineKeyboardButton = InlineKeyboardButton(
    text='Все ведомости',
    url='https://drive.google.com/drive/folders/13Dh7dt1E03W48_8JgdDsp6A1FAdYb-vs?usp=sharing',
    callback_data='statements_pressed')
button_schedule_site: InlineKeyboardButton = InlineKeyboardButton(
    text='Замены на сайте колледжа',
    url='http://xn--j1aejj.xn--p1ai/students/class-schedule',
    callback_data='schedule_site_pressed')

back_button: InlineKeyboardButton = InlineKeyboardButton(
    text='Назад',
    callback_data='back_button_pressed')

#Кнопка при нажатии которой будет отправлен список отсутствующих
button_get_missing_list: InlineKeyboardButton = InlineKeyboardButton(
    text='Получить список',
    callback_data='get_missing_list_pressed')

#Кнопка при нажатии которой будет сбрасываться весь список к пустому
button_reset_missing_list: InlineKeyboardButton = InlineKeyboardButton(
    text='Сбросить список',
    callback_data='reset_missing_list_pressed')
    # callback_data='reset_missing_list')

buttons: list[InlineKeyboardButton] = []
for button, text in COLLEGE_SCHEDULE.items():
    buttons.append(InlineKeyboardButton(
        text='✅ ' + text,
        callback_data=button))

#Создаем клавиатуры
admin_main_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_missing_list],
                     [button_statement],
                     [button_schedule_site]])
not_admin_main_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_statement],
                     [button_schedule_site]])
back_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[back_button]])


#Создание клавиатуры которая появляется по нажатию кнопки 'button_missing_list'
missing_list_kb_builder.add(*buttons)
missing_list_kb_builder.adjust(1)
missing_list_kb_builder.row(back_button)

#Функция которая создает клавиатуру по словарю
def built_keyboard(dict_text_buttons: dict[str, str]) -> InlineKeyboardBuilder:
    buttons: list[InlineKeyboardButton] = []
    for callback_text, text_button in dict_text_buttons.items():
        buttons.append(InlineKeyboardButton(
            text=text_button,
            callback_data=callback_text))
    new_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    new_kb_builder.add(*buttons)
    new_kb_builder.adjust(1)
    new_kb_builder.row(button_reset_missing_list)
    new_kb_builder.row(button_get_missing_list)
    new_kb_builder.row(back_button)
    return new_kb_builder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_RU, COLLEGE_SCHEDULE


#Создаем объект строителя клавиатур KeyboardBuilder
# missing_list_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

#Создаем кнопки клавиатур
button_missing_list: InlineKeyboardButton = InlineKeyboardButton(
    text='Список отсутствующих',
    callback_data='missing_list_pressed')

#Кнопка которая открывает доступ к другим кнопкам с ведомостями
button_statement: InlineKeyboardButton = InlineKeyboardButton(
    text='Все ведомости',
    callback_data='statements_pressed')

#Кнопки на все ведомости и на ведомости по курсам
button_all_statements: InlineKeyboardButton = InlineKeyboardButton(
    text='Все ведомости',
    url='https://drive.google.com/drive/folders/13Dh7dt1E03W48_8JgdDsp6A1FAdYb-vs?usp=sharing',
    callback_data='all_statements_pressed')
button_statement_1_course: InlineKeyboardButton = InlineKeyboardButton(
    text='1 курс',
    url='https://drive.google.com/drive/folders/1ofGrbzpzpDKFxMbkURir6UvPAXnMFC78?usp=sharing',
    callback_data='1_course_pressed')
button_statement_2_course: InlineKeyboardButton = InlineKeyboardButton(
    text='2 курс',
    url='https://drive.google.com/drive/folders/1IhMnimrjRuZoNKtUyQDUXl3LgCb60Crk?usp=sharing',
    callback_data='2_course_pressed')
button_statement_3_course: InlineKeyboardButton = InlineKeyboardButton(
    text='3 курс',
    url='https://drive.google.com/drive/folders/1IhMnimrjRuZoNKtUyQDUXl3LgCb60Crk?usp=sharing',
    callback_data='3_course_pressed')

#Кнопка ведущая на сайт колледжа с заменами
button_schedule_site: InlineKeyboardButton = InlineKeyboardButton(
    text='Замены на сайте колледжа',
    url='http://xn--j1aejj.xn--p1ai/students/class-schedule',
    callback_data='schedule_site_pressed')

#Кнопка назад
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
statements_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_statement_1_course],
                     [button_statement_2_course],
                     [button_statement_3_course],
                     [button_all_statements],
                     [back_button]])


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
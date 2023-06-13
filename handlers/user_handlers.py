from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Text, Command
from lexicon.lexicon import LEXICON_RU, COLLEGE_SCHEDULE
from keyboards.keyboards import not_admin_main_keyboard, admin_main_keyboard, back_keyboard, missing_list_kb_builder, built_keyboard
from filters.filters import IsAdmin, admin_ids
from services.services import get_text_from_file, add_status_button


#инициализация роутера
router: Router = Router()

#Хэндлер срабатывает на команду /start
@router.message(CommandStart(), IsAdmin(admin_ids))
async def process_admin_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'],
                         reply_markup=admin_main_keyboard)
    # print(message.from_user.id)

#Хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_not_admin_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'],
                         reply_markup=not_admin_main_keyboard)

#Хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'],
                         reply_markup=back_keyboard)

#Хэндлер реагирует на нажатия кнопки 'button_missing_list'
@router.callback_query(IsAdmin(admin_ids), Text(text='missing_list_pressed'))
async def pressed_button_missing_list(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU['button_missing_list'],
        reply_markup=built_keyboard(add_status_button(callback, COLLEGE_SCHEDULE)).as_markup())
    
#Хэндлер реагирует на нажатия кнопки 'button_statements'
@router.callback_query(Text(text='statements_pressed'))
async def pressed_button_statements(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU['button_statements'],
        reply_markup=back_keyboard)

#Хэндлер реагирует на нажатия кнопки 'button_schedule_site'
@router.callback_query(Text(text='schedule_site_pressed'))
async def pressed_button_schedule_site(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU['button_schedule_site'],
        reply_markup=back_keyboard)
    
#Хэндлер реагирует на нажатия кнопки 'back_button' администратором
@router.callback_query(IsAdmin(admin_ids), Text(text='back_button_pressed'))
async def pressed_admin_back_button(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU['/start'],
        reply_markup=admin_main_keyboard)

#Хэндлер реагирует на нажатия кнопки 'back_button'
@router.callback_query(Text(text='back_button_pressed'))
async def pressed_back_button(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU['/start'],
        reply_markup=not_admin_main_keyboard)
    
#Хэндлер реагирует на нажатия кнопок с фамилиями в которые
#можно попасть через кнопку 'button_missing_list'
@router.callback_query(F.data.isdigit())
async def pressed_name(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU['button_missing_list'],
        reply_markup=built_keyboard(add_status_button(callback, COLLEGE_SCHEDULE)).as_markup())

#Хэндлер реагирует на нажатия кнопки 'button_get_missing_list'
@router.callback_query(Text(text='get_missing_list_pressed'))
async def pressed_get_missing_list(callback: CallbackQuery):
    text: list[str] = add_status_button.get_missing_list()
    await callback.message.answer(text=text)
    
# Хэндлер срабатывает на нажатия кнопки 'button_reset_missing_list'
# Удаляет все данные о нажатых кнопках
@router.callback_query(Text(text='reset_missing_list_pressed'))
async def pressed_reset_missing_list(callback: CallbackQuery):
    await callback.answer(text='Список сбросился')
    add_status_button.reset_missing_list()
    await callback.message.edit_text(
        text=LEXICON_RU['button_missing_list'],
        reply_markup=built_keyboard(add_status_button(callback, COLLEGE_SCHEDULE)).as_markup())
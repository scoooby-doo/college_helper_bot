from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Text, Command
from filters.filters import IsAdmin, admin_ids, IsTime, NewUser
from lexicon.lexicon import LEXICON_RU, LEXICON_COMMAND_RU, LEXICON_CALLBACK_RU
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.apsched import send_message_cron, send_message_interval, send_message_time
from keyboards.keyboards import keyboard_start_customize
from keyboards.keyboards import Built_keyboard_choose_sites
from services.services import save_json_file, load_from_file, append_to_file
from services.parser import parse_user_sites
import os


#инициализация роутера
router: Router = Router()

#Хэндлер срабатывает на команду /start для пользователя который уже зарегестрирован
@router.message(CommandStart())
async def process_start_command(message: Message, bot: Bot):
    await message.answer(text=LEXICON_COMMAND_RU['/start'])
    # if not os.path.exists('data'):
    #     os.mkdir('data')
    users = load_from_file()
    users[message.from_user.id] = {'pressed_sites': {}}
    save_json_file(users)
    
    # if len(users.keys()) > 1:
    #     users[message.from_user.id] = {'pressed_sites': {}}
    #     append_to_file(data=users)    
    # else:
    #     users = {}
    #     users[message.from_user.id] = {'pressed_sites': {}}
    #     save_json_file(users)

#Хэндлер срабатывает на команду /start для нового пользователя
@router.message(CommandStart(), NewUser())
async def process_start_command(message: Message, bot: Bot):
    await message.answer(text=LEXICON_COMMAND_RU['/start'])
    try:
        users = load_from_file()
        users[message.from_user.id] = {'pressed_sites': {}}
        append_to_file(data=users)
    except Exception as ex:
        print(ex)
        users = {}
        users[message.from_user.id] = {'pressed_sites': {}}
        save_json_file(users)

#Хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_COMMAND_RU['/help'])

# Хэндлер срабатывает на команду /go
@router.message(Command(commands='go'))
async def process_go_command(message: Message):
    await message.answer(text=LEXICON_COMMAND_RU['/go'],
                         reply_markup=keyboard_start_customize)

# Хэндлер срабатывает на callback 'pressed_start_customize'
@router.callback_query(Text(text='pressed_start_customize'))
async def pressed_start_customize(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_CALLBACK_RU['pressed_start_customize'],
        reply_markup=Built_keyboard_choose_sites(callback.from_user.id).as_markup())

# Хэндлер срабатывает на выбор пользователя какие сайты парсить
@router.callback_query(Text(startswith='pressed_button_'))
async def pressed_button_choose_sites(callback: CallbackQuery):
    users = load_from_file()
    if callback.data not in users[str(callback.from_user.id)]['pressed_sites']:
        users[str(callback.from_user.id)]['pressed_sites'][callback.data] = {}
    else:
        users[str(callback.from_user.id)]['pressed_sites'].pop(callback.data)
    save_json_file(users)

    await callback.message.edit_text(
        text=LEXICON_CALLBACK_RU['pressed_start_customize'],
        reply_markup=Built_keyboard_choose_sites(callback.from_user.id).as_markup())
    
# Хэндлер срабатывает на callback 'pressed_next_step'
@router.callback_query(F.data=='pressed_next_step')
async def pressed_next_step(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_CALLBACK_RU['pressed_next_step'])


async def bring_news_to_user(message: Message):
    all_news = parse_user_sites(message.from_user.id)
    # print(all_news)
    # print('-' * 30)
    for news in all_news:
        news_title = news[0]
        news_url = news[1]
        await message.answer(text=f'{news_title}\n{news_url}')

# хэндлер срабатывает на отправку времени в чат
@router.message(IsTime())
async def process_get_time(message: Message, time: list):
    await message.answer('Время получено')
    await message.answer(f'В это время {message.text} вы будете получать новости')

    # scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    # scheduler.add_job(parse_user_sites(str(message.from_user.id)), trigger='cron', hour=time[0], minute=time[1], kwargs={'message': message})
    # scheduler.start()

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(bring_news_to_user, trigger='cron', hour=time[0], minute=time[1], kwargs={'message': message})
    scheduler.start()

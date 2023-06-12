from aiogram.types import Message
from aiogram import Router
from lexicon.lexicon import LEXICON_RU


#Инициализируем роутер
router: Router = Router()

#Срабатывает на все остальные команды
#кроме комманд которые записаны в user_handlers.py
@router.message()
async def send_echo(message: Message):
    try:
        # print(message.json(indent=2, exclude_none=True))
        await message.send_copy(chat_id=message.chat_id)
    except:
        await message.reply(text=LEXICON_RU['no_echo'])
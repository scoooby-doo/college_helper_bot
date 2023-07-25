from aiogram import Bot
from aiogram.types import Message


async def send_message_time(bot: Bot, message: Message):
    await bot.send_message(message.chat.id, f'Это сообщение отправлено через несколько секунд после старта бота')


async def send_message_cron(bot: Bot, message: Message):
    await bot.send_message(message.chat.id, f'Это сообщение будет отправляться ежедневно в указанное время')
    

async def send_message_interval(bot: Bot, message: Message):
    await bot.send_message(message.chat.id, f'Это сообщение будет отправляться с интервалом в 1 минуту')
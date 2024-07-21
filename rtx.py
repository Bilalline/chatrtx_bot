import os
import asyncio
import rtx_api_3_5 as rtx_api
from telebot.async_telebot import AsyncTeleBot
from aiogram import types
from dotenv import load_dotenv
import random

options = ["Работаю", "Выполняю", "Обождите", "Занимаюсь", "В работе", "Делаю чудо", "Бип буп бип буп"]


load_dotenv()
TOKEN = os.getenv("TOKEN")

# Создаем объект бота
bot = AsyncTeleBot(TOKEN)

@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.reply_to(message, """\
Приветствую, Я чатбот на основе ChatRtx.
Сейчас я работаю на чистом энтузиазме и жгу электроэнергию в квартире. Для получения этого сообщения выполни команду /help.\
""")

@bot.message_handler(func=lambda message: True)
async def handle_message(message):
    selected_option = random.choice(options)
    await bot.reply_to(message, selected_option)
    res = rtx_api.send_message(message.text)
    # print(response)
    await bot.reply_to(message, res, parse_mode=telegram.ParseMode.MARKDOWN_V2)

# Запускаем бота
asyncio.run(bot.polling())

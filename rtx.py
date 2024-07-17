import os
import asyncio
import rtx_api_3_5 as rtx_api
from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

# Создаем объект бота
bot = AsyncTeleBot(TOKEN)


@bot.message_handler(func=lambda message: True)
async def handle_message(message):
    await bot.reply_to(message, 'wait')
    res = rtx_api.send_message(message.text)
    # print(response)
    await bot.reply_to(message, res)

# Запускаем бота
asyncio.run(bot.polling())
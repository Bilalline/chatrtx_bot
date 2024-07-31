import os
import asyncio
import rtx_api_3_5 as rtx_api
from telebot.async_telebot import AsyncTeleBot
from telebot import TeleBot
from dotenv import load_dotenv
import random

options = ["Работаю", "Выполняю", "Обождите", "Занимаюсь", "В работе", "Делаю чудо", "Бип буп бип буп"]
LOG = -1002165280593

load_dotenv()
TOKEN = os.getenv("TOKEN")

# Создаем объект бота
bot = AsyncTeleBot(TOKEN)

@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.reply_to(message, 'Приветствую, Я чатбот на основе ChatRtx.\n'
                                'Сейчас я работаю на чистом энтузиазме и '
                                'жгу электроэнергию в квартире. Для получения этого сообщения выполни команду /help.')

@bot.message_handler(commands=['id'])
async def like(message):
  cid = message.chat.id
  await bot.reply_to(message, cid)

@bot.message_handler(content_types=['text'])
async def handle_message(message):
    question = await bot.send_message(LOG, f'Q by [User](tg://openmessage?user_id={message.from_user.id}): {message.text}', parse_mode='markdown')
    try:
        # print(f'Q by [User](tg://user?id={message.from_user.id})')
        selected_option = random.choice(options)
        await bot.reply_to(message, selected_option)

        try:
            res = rtx_api.send_message(message.text)
            if len(res) > 2500:
                msgs = [res[i:i + 2500] for i in range(0, len(res), 2500)]
                for text in msgs:
                    await bot.reply_to(message, text)
        except Exception as e:
            await bot.reply_to(question, f'Error RTX:{e}')

        await bot.reply_to(message, res, parse_mode='markdown')
        await bot.reply_to(question, f'A: {res}', parse_mode='markdown')
    
    except Exception as e:
            await bot.reply_to(question, f'Error RTX:{e}')



# Запускаем бота
asyncio.run(bot.polling())

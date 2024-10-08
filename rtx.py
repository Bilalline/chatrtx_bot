import os
import asyncio
import rtx_api_july_2024 as rtx_api
from telebot.async_telebot import AsyncTeleBot
from telebot import TeleBot
from dotenv import load_dotenv
import pprint
import random
import re
from my_functions import options

load_dotenv()
TOKEN = os.getenv("TOKEN")
IP = os.getenv("IP")
PORT = os.getenv("PORT")
GROUP_CHAT_LOG = os.getenv("GROUP_CHAT_LOG")

# Создаем объект бота
bot = AsyncTeleBot(TOKEN)


async def convert_to_markdown(text):
    # Преобразование HTML разметки в Markdown
    text = await asyncio.to_thread(re.sub, r'<b>(.*?)</b>', r'*\1*', text)  # Жирный
    text = await asyncio.to_thread(re.sub, r'<i>(.*?)</i>', r'_\1_', text)  # Курсив
    text = await asyncio.to_thread(re.sub, r'<code>(.*?)</code>', r'`\1`', text)  # Код
    text = await asyncio.to_thread(re.sub, r'<a href="(.*?)">(.*?)</a>', r'\2', text)  # Ссылки
    text = await asyncio.to_thread(re.sub, r'<.*?>', '', text)  # Удаление любых других HTML-тегов
    
    return text

@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.reply_to(message, 'Приветствую, Я чатбот на основе ChatRtx.\n'
                                'Сейчас я работаю на чистом энтузиазме и '
                                'жгу электроэнергию в квартире. Если ответ получили на английском и вас это не устраевает, '
                                'попросите просто продублируйте вопрос с посьбой написать на русском. \n'
                                'Для получения этого сообщения выполни команду /help.')

@bot.message_handler(commands=['id'])
async def like(message):
    cid = message.chat.id
    await bot.reply_to(message, cid)

@bot.message_handler(content_types=['text'])
async def handle_message(message):
    if message.chat.type == "supergroup":
        if "@chatrtxbill_bot" in message.text:
            user_id = message.from_user.id
            group_id = message.chat.id
            username = message.from_user.username if message.from_user.username else f'User {user_id}'  # Проверка наличия ника
            question = await bot.send_message(GROUP_CHAT_LOG, f'Q by t.me/{username} ({user_id}): {message.text[15:]}, from group {group_id}', parse_mode='Markdown')
            selected_option = random.choice(options)
            await bot.reply_to(message, selected_option)

            try:
                res = await asyncio.to_thread(rtx_api.send_message, message.text[15:])
                markdown_message = await convert_to_markdown(res)

                if len(markdown_message) > 2500:
                    msgs = [markdown_message[i:i + 2500] for i in range(0, len(markdown_message), 2500)]
                    for text in msgs:
                        await bot.reply_to(message, text, parse_mode='markdown')
                        await bot.reply_to(question, f'A: {text}', parse_mode='markdown')
                else:
                    await bot.reply_to(message, markdown_message, parse_mode='markdown')
                    await bot.reply_to(question, f'A: {markdown_message}', parse_mode='markdown')
            except Exception as e:
                await bot.reply_to(question, f'Error RTX: {e}')
        else: print('in group but not @')
    elif message.chat.type == "private":
        user_id = message.from_user.id
        username = message.from_user.username if message.from_user.username else f'User {user_id}'  # Проверка наличия ника
        question = await bot.send_message(GROUP_CHAT_LOG, f'Q by t.me/{username} ({user_id}): {message.text}', parse_mode='Markdown')
        selected_option = random.choice(options)
        await bot.reply_to(message, selected_option)

        try:
            res = await asyncio.to_thread(rtx_api.send_message, message.text)
            markdown_message = await convert_to_markdown(res)

            if len(markdown_message) > 2500:
                msgs = [markdown_message[i:i + 2500] for i in range(0, len(markdown_message), 2500)]
                for text in msgs:
                    await bot.reply_to(message, text, parse_mode='markdown')
                    await bot.reply_to(question, f'A: {text}', parse_mode='markdown')
            else:
                await bot.reply_to(message, markdown_message, parse_mode='markdown')
                await bot.reply_to(question, f'A: {markdown_message}', parse_mode='markdown')
        except Exception as e:
            await bot.reply_to(question, f'Error RTX: {e}')

# Запускаем бота
try:
    asyncio.run(bot.polling(skip_pending=True))
except Exception as e:
    print(f'Polling error: {e}')
    asyncio.sleep(30)
    asyncio.run(bot.polling(skip_pending=True))
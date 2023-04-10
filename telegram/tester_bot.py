# @TesterYLbot
# задача про тестировку

import logging
from telegram.ext import Application, MessageHandler, filters, Updater
from telegram.ext import CommandHandler, ConversationHandler
import datetime
import json
import random


BOT_TOKEN = '6226822966:AAFIEGWq2cUt4y-tgiwAFFW2BkYbQBZ37Ms'

   
test_spis = []   
count = 0
last_spis = []


def random_def(spis):
    global last_spis
    
    if len(spis) <= 10:
        last_spis = random.sample(spis, len(spis))
    else:
        last_spis = random.sample(spis, 10) 
    

async def downloader(update, context):
    global test_spis, last_spis
    
    file = await context.bot.get_file(update.message.document)
    await file.download_to_drive('data.json')
    
    with open('data.json', encoding="utf-8") as file:
        f = file.read()
        data = json.loads(f)
        data = data['test']
        
        for i in data:
            test_spis.append((i['question'], i['response']))
            
        random_def(test_spis)
            
    await context.bot.send_message(update.message.chat_id, text=f'{last_spis[0][0]}')
    return 2


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Отправьте мне файл и я буду вас тестить ;)",
    )
    
    return 1
    

async def test(update, context):
    global count, last_spis, test_spis
    
    if update.message.text == last_spis[0][1]:
        count += 1
        
    last_spis.pop(0)
    if len(last_spis) != 0:
        await context.bot.send_message(update.message.chat_id, text=f'{last_spis[0][0]}')
        return 1
    else:
        await context.bot.send_message(update.message.chat_id, text=f'Правильных ответов было {count}\n Введите /start для нового теста')
        count = 0
        last_spis = []
        test_spis = []
        return ConversationHandler.END


async def stop(update, context):
    global count, test_spis, last_spis
    
    await update.message.reply_text(f"Chao. Введите /start для нового теста")
    
    count = 0
    test_spis = []
    last_spis = []
    
    return ConversationHandler.END


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('start', start)],
        
        states={
            1: [MessageHandler(filters.Document.ALL, downloader)],   
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, test)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
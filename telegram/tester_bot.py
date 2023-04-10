# @TesterYLbot
# задача про тестировку

import logging
from telegram.ext import Application, MessageHandler, filters, Updater
from telegram.ext import CommandHandler
import datetime
import json


BOT_TOKEN = '6226822966:AAFIEGWq2cUt4y-tgiwAFFW2BkYbQBZ37Ms'

   
test_spis = []   
    
async def downloader(update, context):
    global test_spis
    
    file = await context.bot.get_file(update.message.document)
    await file.download_to_drive('data.json')
    
    with open('data.json', encoding="utf-8") as file:
        f = file.read()
        data = json.loads(f)
        data = data['test']
        
        for i in data:
            test_spis.append((i['question'], i['response']))
            
    print(test_spis)
    
    await context.bot.send_message(update.message.chat_id, text=f'Задания получены! Начнем тест!')
    await context.bot.send_message(update.message.chat_id, text=f'вопрос')


async def start(update, context):
    """Отправляет сообщение когда получена команда /go"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Отправьте мне файл и я буду вас тестить ;)",
    )

    

async def test(update, context):
    pass


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, test)

    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)
    application.add_handler(MessageHandler(filters.Document.ALL, downloader))
    
    application.add_handler(CommandHandler("start", start))
    

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
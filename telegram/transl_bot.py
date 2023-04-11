# @translatorYlbot
# задача про перевод

import logging
from telegram.ext import Application, MessageHandler, filters, Updater
from telegram.ext import CommandHandler, ConversationHandler
import datetime
import json
import random
from telegram import ReplyKeyboardMarkup
from googletrans import Translator, constants


BOT_TOKEN = '5921422933:AAGSdehY8F2nXo2UuELxED0MqgCv02y6BzY'


language = 1



def translator1(txt):
    translator = Translator() 
    translation = translator.translate(txt, dest='en')     
    
    return translation.text


def translator2(txt):
    translator = Translator()
    translation = translator.translate(txt, dest='ru')     
    
    return translation.text


async def ru_en(update, context):
    global language
    language = 1
    await update.message.reply_text('Введите текст:')
    return 1
    


async def en_ru(update, context):
    global language
    language = 2
    await update.message.reply_text('Введите текст:')
    return 1
    
    
async def answer(update, context):   
    global language
    
    if language == 2:
        text = translator2(update.message.text)
    else:
        text = translator1(update.message.text)
    
    await update.message.reply_text(text)
    
    return ConversationHandler.END
    
    #await context.bot.send_message(update.message.chat_id, text=f'Нажмите /start для нового перевода')
    

async def start(update, context):
    reply_keyboard = [['/ru-en'], ['/en-ru']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text("Я бот-переводчик, выберите язык:", reply_markup=markup)
    

async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


def main():
    application = Application.builder().token('5921422933:AAGSdehY8F2nXo2UuELxED0MqgCv02y6BzY').build()
    
    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('start', start)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            2: [CommandHandler("ru-en", ru_en)], 
            3: [CommandHandler("en-ru", en_ru)]
            
        },
        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
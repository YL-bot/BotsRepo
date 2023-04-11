# @TranslYLbot
# задача про перевод

import logging
from telegram.ext import Application, MessageHandler, filters, Updater
from telegram.ext import CommandHandler, ConversationHandler
import datetime
import json
import random
from telegram import ReplyKeyboardMarkup
from googletrans import Translator, constants


BOT_TOKEN = '6181021435:AAERJar6_wtLFDONNE8g0tITitWrGMlHlNE'


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
    


async def en_ru(update, context):
    global language
    language = 2
    await update.message.reply_text('Введите текст:')
    
    
async def answer(update, context):   
    global language
    
    if language == 2:
        text = translator2(update.message.text)
    else:
        text = translator1(update.message.text)
    
    await update.message.reply_text(text)
    
    await context.bot.send_message(update.message.chat_id, text=f'Нажмите /start для нового перевода')
    

async def start(update, context):
    #await update.message.reply_text("Я бот-переводчик, выберите язык:", reply_markup=markup)
    
    await update.message.reply_text("Я бот-переводчик, выберите язык:")
    

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, answer)

    application.add_handler(text_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ru-en", ru_en))
    application.add_handler(CommandHandler("en-ru", en_ru))
    
    #reply_keyboard = [['/ru-en'], ['/en-ru']]
    #markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    

    application.run_polling()

# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
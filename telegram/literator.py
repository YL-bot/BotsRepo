#  @YLliteratorbot

import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler, ConversationHandler
import datetime
from sys import stdin

BOT_TOKEN = '5673367140:AAEfr4PbdXlFSuLcaj9LItfS7615uDDlcb4'

lines = ['Буря мглою небо кроет,', 'Вихри снежные крутя;', 'То, как зверь, она завоет,', 'То заплачет, как дитя,',
         'То по кровле обветшалой', 'Вдруг соломой зашумит,', 'То, как путник запоздалый,', 'К нам в окошко застучит.',
         'Наша ветхая лачужка', 'И печальна и темна.', 'Что же ты, моя старушка,', 'Приумолкла у окна?', 'Или бури завываньем',
         'Ты, мой друг, утомлена,', 'Или дремлешь под жужжаньем', 'Своего веретена?', 'Выпьем, добрая подружка', 'Бедной юности моей,',
         'Выпьем с горя; где же кружка?', 'Сердцу будет веселей.', 'Спой мне песню, как синица', 'Тихо за морем жила;',
         'Спой мне песню, как девица', 'За водой поутру шла.', 'Буря мглою небо кроет,', 'Вихри снежные крутя;',
         'То, как зверь, она завоет,', 'То заплачет, как дитя.', 'Выпьем, добрая подружка', 'Бедной юности моей,',
         'Выпьем с горя; где же кружка?', 'Сердцу будет веселей.']

count = 0
#for line in stdin:
#    lines.append(line.strip("\n"))
#print(lines)

async def start(update, context):
    global count
    await update.message.reply_text(
        f"Привет. Сейчас будем играть\nДля выхода введите /stop\n ПОЕХАЛИ!\n {lines[count]}")
    count += 1
    
    return 1


async def first_response(update, context):
    global count
    
    txt = update.message.text
    if txt == lines[count]:
        count += 1
        if count >= len(lines):
            await update.message.reply_text("Вы молодец! Ура ура ура")
            count = 0
            return ConversationHandler.END
        
        await update.message.reply_text(f"{lines[count]}")
        count += 1
        
        if count >= len(lines):
            await update.message.reply_text("Вы молодец! Ура ура ура")
            count = 0
            return ConversationHandler.END
        
        return 1
    
    await update.message.reply_text(f"нет, не так. Вот так:\n {lines[count]}")
    return 1


async def stop(update, context):
    global count
    await update.message.reply_text("Всего доброго!")
    count = 0
    return ConversationHandler.END


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('start', start)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],   
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

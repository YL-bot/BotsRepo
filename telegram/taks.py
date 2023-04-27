# @EchoYandexLyceumBot - тг бота
# 1 - 3 задачи

import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
import datetime

BOT_TOKEN = '6198517997:AAEYkDvuarlabnaXOGUA9JDe9i6A9Welyqc'

TIMER = 5


#logging.basicConfig(
#   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
#logger = logging.getLogger(__name__)



async def unset(update, context):
    """Удаляет задачу, если пользователь передумал"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text)
    

async def task(context):
    global TIMER
    """Выводит сообщение"""
    await context.bot.send_message(context.job.chat_id, text=f'КУКУ! {TIMER}c. прошли!')
    

def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


# Обычный обработчик, как и те, которыми мы пользовались раньше.
async def set_timer(update, context):
    global TIMER
    
    try:
        TIMER = int("".join(list(update.message.text)[list(update.message.text).index('r') + 2:]))
        if TIMER < 0:
            TIMER = 5
    except Exception:
        TIMER = 5
    
    """Добавляем задачу в очередь"""
    chat_id = update.effective_message.chat_id
    # Добавляем задачу в очередь
    # и останавливаем предыдущую (если она была)
    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_once(task, TIMER, chat_id=chat_id, name=str(chat_id), data=TIMER)

    text = f'Вернусь через {TIMER} с.!'
    if job_removed:
        text += ' Старая задача удалена.'
    await update.effective_message.reply_text(text)


async def echo(update, context):
    await update.message.reply_text(f'Я получил сообщение "{update.message.text}"')


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Укажи время для таймера, default=5)",
    )


async def time_command(update, context):
    answ = datetime.datetime.now().time()
    await update.message.reply_text(str(answ))
    

async def date_command(update, context):
    answ = datetime.date.today()
    await update.message.reply_text(str(answ))
    

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("time", time_command))
    application.add_handler(CommandHandler("date", date_command))
    
    application.add_handler(CommandHandler("set_timer", set_timer))
    application.add_handler(CommandHandler("unset", unset))

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
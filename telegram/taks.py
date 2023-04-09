# @EchoYandexLyceumBot - тг бота
import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
import datetime

BOT_TOKEN = '6198517997:AAEYkDvuarlabnaXOGUA9JDe9i6A9Welyqc'


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)


async def echo(update, context):
    await update.message.reply_text(f'Я получил сообщение "{update.message.text}"')


# Напишем соответствующие функции.
# Их сигнатура и поведение аналогичны обработчикам текстовых сообщений.
async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я жду проверки ;)",
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

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
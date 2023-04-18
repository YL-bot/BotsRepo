# @translatorYlbot
# задача про перевод
import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, Bot, ReplyKeyboardRemove
import requests


BOT_TOKEN = '5921422933:AAGSdehY8F2nXo2UuELxED0MqgCv02y6BzY'

logger = logging.getLogger(__name__)
bot = Bot(BOT_TOKEN)
API_KEY = 'AQVNzhfpiSw09Z_EBDWdUtal9XPJR_I5lVASpWlT'
FOLDER_ID = 'b1go7l39akkvmdgv9j16'


async def start(update, context):
    kbrd = ReplyKeyboardMarkup([['RU -> EN', 'EN -> RU']])
    await update.message.reply_text('Привет. Выбери направление перевода.', reply_markup=kbrd)
    context.user_data['way'] = -1


async def change_lang(update, context):
    txt = update.message.text
    if txt not in ['RU -> EN', 'EN -> RU']:
        if not context.user_data.get('way') or context.user_data['way'] == -1:
            await update.message.reply_text('Выберите направление перевода.')
            return
        elif context.user_data['way'] == 'RU -> EN':
            body = {"targetLanguageCode": "en", "languageCode": "ru", "texts": txt,
                    "folderId": FOLDER_ID}
            headers = {"Content-Type": "application/json", "Authorization": f"Api-Key {API_KEY}"}
            response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                                     json=body, headers=headers)
            res = response.json()['translations'][0]['text']
        else:
            body = {"targetLanguageCode": "ru", "languageCode": "en", "texts": txt,
                    "folderId": FOLDER_ID}
            headers = {"Content-Type": "application/json", "Authorization": f"Api-Key {API_KEY}"}
            response = requests.post(
                'https://translate.api.cloud.yandex.net/translate/v2/translate',
                json=body, headers=headers)
            res = response.json()['translations'][0]['text']
        await update.message.reply_text(f'Результат:\n{res}')
    else:
        context.user_data['way'] = txt


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    change_way = MessageHandler(filters.TEXT & ~filters.COMMAND, change_lang)
    st = CommandHandler('start', start)
    application.add_handler(st)
    application.add_handler(change_way)
    application.run_polling()


if __name__ == '__main__':
    main()
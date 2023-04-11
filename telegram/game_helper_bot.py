# @TranslYLbot
# бот помощник для игр

import logging
import datetime
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from random import randint


BOT_TOKEN = '6181021435:AAERJar6_wtLFDONNE8g0tITitWrGMlHlNE'


reply_keyboard = [['/dice', '/timer']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

reply_keyboard_dice = [['/gr6x1'], ['/gr6x2'], ['/gr20'], ['/cancel']]
markup_dice = ReplyKeyboardMarkup(reply_keyboard_dice, one_time_keyboard=False)

reply_keyboard_timer = [['/timer_30s'], ['/timer_1m'], ['/timer_5m'], ['/cancel']]
markup_timer = ReplyKeyboardMarkup(reply_keyboard_timer, one_time_keyboard=False)

reply_keyboard_close = [['/close']]
markup_close = ReplyKeyboardMarkup(reply_keyboard_close, one_time_keyboard=False)


async def dice(update, context):
    await update.message.reply_text(
        "Вы в /dice", reply_markup=markup_dice)


async def timer(update, context):
    await update.message.reply_text(
        "Вы в /timer", reply_markup=markup_timer)


async def gr6x1(update, context):
    await update.message.reply_text(randint(1, 6), reply_markup=markup_dice)


async def gr6x2(update, context):
    await update.message.reply_text(f"{randint(1, 6)}, {randint(1, 6)}", reply_markup=markup_dice)


async def gr20(update, context):
    await update.message.reply_text(randint(1, 20), reply_markup=markup_dice)


async def cancel(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Вы в меню!",
        reply_markup=markup
    )


async def close(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text, reply_markup=markup_timer)


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def timer30c(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.effective_message.chat_id
    # Добавляем задачу в очередь
    # и останавливаем предыдущую (если она была)
    time = 30
    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_once(task, time, chat_id=chat_id, name=str(chat_id), data=time)

    text = f'Засек 30 с.!'
    if job_removed:
        text += ' Старая задача удалена.'
    await update.message.reply_text(text, reply_markup=markup_close)


async def timer60c(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.effective_message.chat_id
    # Добавляем задачу в очередь
    # и останавливаем предыдущую (если она была)
    time = 60
    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_once(task, time, chat_id=chat_id, name=str(chat_id), data=time)

    text = f"Засек 60 с.!"
    if job_removed:
        text += ' Старая задача удалена.'
    await update.message.reply_text(text, reply_markup=markup_close)


async def timer300c(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.effective_message.chat_id
    # Добавляем задачу в очередь
    # и останавливаем предыдущую (если она была)
    time = 300
    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_once(task, time, chat_id=chat_id, name=str(chat_id), data=time)

    text = f"Засек 5мин!"
    if job_removed:
        text += ' Старая задача удалена.'
    await update.message.reply_text(text, reply_markup=markup_close)


async def task(context):
    """Выводит сообщение"""
    await context.bot.send_message(context.job.chat_id, text=f'{context.job.data}c. истекло!',
                                   reply_markup=markup_timer)


async def task2(context):
    """Выводит сообщение"""
    await context.bot.send_message(context.job.chat_id, text=f'КУКУ! {context.job.data}c. прошли!')


async def unset(update, context):
    """Удаляет задачу, если пользователь передумал"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text)


# Напишем соответствующие функции.
# Их сигнатура и поведение аналогичны обработчикам текстовых сообщений.
async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!",
        reply_markup=markup
    )


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


async def time(update, context):
    d = str(datetime.datetime.now()).split()[1].split('.')[0]
    d = d.split(':')
    d[0] = int(d[0]) + 3
    d = [str(i) for i in d]
    d = ':'.join(d)
    await update.message.reply_text(d)


async def date(update, context):
    await update.message.reply_text(str(datetime.datetime.now()).split()[0])


TIMER = 5  # таймер на 5 секунд


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
    """Добавляем задачу в очередь"""
    chat_id = update.effective_message.chat_id
    # Добавляем задачу в очередь
    # и останавливаем предыдущую (если она была)
    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_once(task2, TIMER, chat_id=chat_id, name=str(chat_id), data=TIMER)

    text = f'Вернусь через 5 с.!'
    if job_removed:
        text += ' Старая задача удалена.'
    await update.effective_message.reply_text(text)


async def set_timer2(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.effective_message.chat_id
    # Добавляем задачу в очередь
    # и останавливаем предыдущую (если она была)
    job_removed = remove_job_if_exists(str(chat_id), context)
    time = int(context.args[0])
    if time <= 0:
        text = f'Время должно быть больше 0с.!'
        if job_removed:
            text += ' Старая задача удалена.'
        await update.effective_message.reply_text(text)
    else:
        context.job_queue.run_once(task2, time, chat_id=chat_id, name=str(chat_id), data=time)

        text = f'Вернусь через {time} с.!'
        if job_removed:
            text += ' Старая задача удалена.'
        await update.effective_message.reply_text(text)


# Зарегистрируем их в приложении перед
# регистрацией обработчика текстовых сообщений.
# Первым параметром конструктора CommandHandler я
# вляется название команды.

# Определяем функцию-обработчик сообщений.
# У неё два параметра, updater, принявший сообщение и контекст - дополнительная информация о сообщении.
async def echo(update, context):
    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.
    await update.message.reply_text(f"Я получил сообщение: '{update.message.text}'")


def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token(BOT_TOKEN).build()

    # Создаём обработчик сообщений типа filters.TEXT
    # из описанной выше асинхронной функции echo()
    # После регистрации обработчика в приложении
    # эта асинхронная функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("time", time))
    application.add_handler(CommandHandler("date", date))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))
    application.add_handler(CommandHandler("set_timer", set_timer2))
    application.add_handler(CommandHandler("dice", dice))
    application.add_handler(CommandHandler("timer", timer))
    application.add_handler(CommandHandler("gr6", gr6x1))
    application.add_handler(CommandHandler("gr62", gr6x2))
    application.add_handler(CommandHandler("gr20", gr20))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CommandHandler("close", close))
    application.add_handler(CommandHandler("timer_30s", timer30c))
    application.add_handler(CommandHandler("timer_1m", timer60c))
    application.add_handler(CommandHandler("timer_5m", timer300c))

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()

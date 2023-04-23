import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random 
import datetime

count = 1

def func(txt):
    try:
        dictt = {0: "Понедельник", 1: "Вторник", 2: "Среда", 3: "Четверг", 4: "Пятница", 5: "Суббота", 6: "Воскресенье"}
        date = datetime.datetime.strptime(txt, '%Y-%m-%d')
        return dictt[datetime.datetime.weekday(date)]
    except Exception:
        return 'чет ошибка damn... попробуй ввести дату нормально, не?'


def main():
    global count
    vk_session = vk_api.VkApi(token='vk1.a.lhwzGcDCDlTAR8PIAQdwYb7eqP0KVs3T6LcqnlOJ0a58cq27HoVqGt4FKluOuIgu8Z9Mokx5A_Z8XZcV5ys3-o0OMmh-tOIRPz2Lge87yacgYtvx5sqVN7irfpLipyJh1XcLi6kSE3y5DpR0Z03Hx65qv3UypQcV0QKMNKegqu8fZv2UwQ2FWzYo3ak_I5alpBEpxAYYdmDpzMAXk1ViMA')

    longpoll = VkBotLongPoll(vk_session, 220073744)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:   
            #print('Текст:', event.obj.message['text'])
            
            vk = vk_session.get_api()
            id = event.obj.message['from_id']
            if count == 1:
                count += 1
                vk.messages.send(user_id=id, message=f"ЙОУ ЙОУ ХЕЛЛОУ! Я могу тебе вернуть день недели, если скинешь дату в таком формате: YYYY-MM-DD", random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=id, message=func(event.obj.message['text']), random_id=random.randint(0, 2 ** 64))
                     


if __name__ == '__main__':
    main()
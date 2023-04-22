import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import datetime


def date():
    dictt = {0: "Понедельник", 1: "Вторник", 2: "Среда", 3: "Четверг", 4: "Пятница", 5: "Суббота", 6: "Воскресенье"}
    now_date = datetime.datetime.now()
    answ = f'{now_date.day}-{now_date.month}-{now_date.year} (г) ; {now_date.hour}:{now_date.minute} ; день недели - {dictt[datetime.datetime.weekday(now_date)]}'
    
    return answ
    

def main():
    vk_session = vk_api.VkApi(token='vk1.a.lhwzGcDCDlTAR8PIAQdwYb7eqP0KVs3T6LcqnlOJ0a58cq27HoVqGt4FKluOuIgu8Z9Mokx5A_Z8XZcV5ys3-o0OMmh-tOIRPz2Lge87yacgYtvx5sqVN7irfpLipyJh1XcLi6kSE3y5DpR0Z03Hx65qv3UypQcV0QKMNKegqu8fZv2UwQ2FWzYo3ak_I5alpBEpxAYYdmDpzMAXk1ViMA')

    longpoll = VkBotLongPoll(vk_session, 220073744)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:   
            #print('Текст:', event.obj.message['text'])
            vk = vk_session.get_api()
            
            id = event.obj.message['from_id']
            text = event.obj.message['text']
            
            if 'день' in text or 'дата' in text or 'число' in text or 'время' in text:
                vk.messages.send(user_id=id, message=date(), random_id=random.randint(0, 2 ** 64))      
            else:
                vk.messages.send(user_id=id, message="Используйте дата, день, время или число в сообщение и получите интересный ответ!", random_id=random.randint(0, 2 ** 64))                         


if __name__ == '__main__':
    main()
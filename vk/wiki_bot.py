import wikipedia 
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random 
import datetime

count = 1

def func(txt):
    try:
        #wikipedia.set_lang('ru')
        return wikipedia.summary(txt)
    except Exception:
        return 'чет ошибка damn... попробуй ввести желаемое нормально, не?'


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
                vk.messages.send(user_id=id, message=f"Прив! Могу найти тебе инфу из вики, введи то, что хочешь узнать, в некст сообщении!", random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=id, message=func(event.obj.message['text']), random_id=random.randint(0, 2 ** 64))
                     


if __name__ == '__main__':
    main()
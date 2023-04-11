#3-4 
# Навык Бога

#https://dialogs.yandex.ru/


from flask import Flask, request, jsonify
import logging
import json
# импортируем функции из нашего второго файла geo
from geo import get_country, get_distance, get_coordinates, get_geo_info

app = Flask(__name__)

# Добавляем логирование в файл.
# Чтобы найти файл, перейдите на pythonwhere в раздел files,
# он лежит в корневой папке
logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

sessionStorage = {}
got_name = False


def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name',
            # то возвращаем ее значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)


#@app.route('/')
#def index():
#    return 'This is the main page. Welcome!'


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Request: %r', response)
    return jsonify(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # создаем словарь в который в будущем положим имя пользователя
        sessionStorage[user_id] = {
            'first_name': None
        }
        res['response'][
            'text'] = 'Привет! Я могу показать город или сказать расстояние между городами! Но для начала, представься, пожалуйста'
        return
    # Получаем города из нашего
    if sessionStorage[user_id]['first_name'] is None:
        # в последнем его сообщение ищем имя.
        first_name = get_first_name(req)
        # если не нашли, то сообщаем пользователю что не расслышали.
        if first_name is None:
            res['response']['text'] = \
                'Не расслышала имя. Повтори, пожалуйста!'
        # если нашли, то приветствуем пользователя.
        # И спрашиваем какой город он хочет увидеть.
        else:
            sessionStorage[user_id]['first_name'] = first_name
            res['response'][
                'text'] = f"Поняла, {first_name.title()}! Теперь можешь ввести один или несколько городов"

    else:
        cities = get_cities(req)
        if not cities:
            res['response']['text'] = 'Ты не написал название не одного города!'
        elif len(cities) == 1:
            res['response']['text'] = 'Этот город в стране - ' + get_geo_info(cities[0], "country")
        elif len(cities) == 2:
            distance = get_distance(get_geo_info(cities[0], "coordinates"),
                                    get_geo_info(cities[1], "coordinates"))
            res['response']['text'] = 'Расстояние между этими городами: ' + str(round(distance)) + ' км.'
        else:
            res['response']['text'] = 'Слишком много городов!'


def get_cities(req):
    cities = []
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.GEO':
            if 'city' in entity['value']:
                cities.append(entity['value']['city'])
    return cities


if __name__ == '__main__':
    app.run()
import vk_api
from RASPIS import TimeChecker, savelast, GetRaspis, important_checker
from flask import Flask, Response, request
import random

#TESTING включает режим тестироващика. При нем все ID, отличные от testerID будут получать оповещение о проведении технических работ.
TESTING = False
testerID = 366782296
app = Flask(__name__)

vk_session = vk_api.VkApi(token='2a85a114c3af837c332b88f804290e76ddf4f326025a20e352d897d41a3fd5c3c2e47bb56a1df0e226f83')
vk = vk_session.get_api()


def GetUsersId():
    user_id_items = vk.groups.getMembers(group_id='207336652')
    return user_id_items['items']


def sender(id, text):
    try:
        vk.messages.send(user_id=id, message=text, random_id=random.getrandbits(64))
    except: pass


##Функции для переконвертирования ответа с расписанием в формат сообщения
def RaspisForDay(id):
    sender(id, '\n'.join(filter(None, GetRaspis(0))))


helpDict = (
    'Понедельник:',
    'Вторник:',
    'Среда:',
    'Четверг:',
    'Пятница:'
)
reversedHelpDict = {
    'пн': 0,
    'вт': 1,
    'ср': 2,
    'чт': 3,
    'пт': 4,
}


def RaspisForWeek(id):
    sender(id, '\n'.join([helpDict[i] + '\n' + '\n'.join(filter(None, day))
                          for i, day in enumerate(GetRaspis(1))]))


def RaspisForWeekDay(id, weekDay):
    sender(id, '\n'.join(filter(None, GetRaspis(1)[weekDay])))


@app.route('/')
def Main():
    PushMessage = TimeChecker()
    if PushMessage:
        savelast()
        for i in GetUsersId():
            if (not TESTING) or (TESTING and i == testerID):
                sender(i, PushMessage)
        return "Я все отправил"
    return "Нечего отправлять "


@app.route('/reset')
def Reset():
    savelast(t=False)
    return 'Очистил!'


@app.route('/GetEvent', methods=['POST'])
def GetEvent():
    data = request.get_json()

    if data['type'] == 'group_join':
            sender(data['object']['user_id'], 'Добро пожаловать!✌🏻\nЭтот бот будет напоминать тебе о паре за 15 минут.\nСоветуем не отключай уведомления.\nСписок команд:\n“р” - расписание на текущий день\n“в” - расписание на всю неделю,\n“пн” - “пт” - расписание на определенный день')

    if data['type'] == 'message_new':
        msg = data['object']['message']['text'] # Я убрал lower тут потому, что иначе ссылка будет неверной.
        id = data['object']['message']['peer_id']
        check_id = data['object']['message']['from_id']
        if check_id != id:
            important_checker(msg)
        elif (not TESTING) or (TESTING and id == testerID):
            if id in GetUsersId():
                msg = msg.lower() # А вот тут я его вернул, так как тут ссылок уже никаких не ожидается.
                if msg == "р":
                    RaspisForDay(id)
                elif msg == "в":
                    RaspisForWeek(id)
                elif msg == 'с':
                    sender(id, 'Добро пожаловать!✌🏻\nЭтот бот будет напоминать тебе о паре за 15 минут.\nСоветуем не отключай уведомления.\nСписок команд:\n“р” - расписание на текущий день\n“в” - расписание на всю неделю,\n“пн” - “пт” - расписание на определенный день')
                elif msg in reversedHelpDict:
                    RaspisForWeekDay(id, reversedHelpDict[msg])
                else:
                    sender(id, 'Неверная команда. Напиши "С", чтобы узнать список команд.')
            else:
                sender(id, 'Ты не подписан! Я с такими не общаюсь.')
        elif check_id == id: sender(id, 'К сожалению, бесплатный сервер только один. Так что работа бота и его тестировка проходят на одном и том же сервере. Напишите позже.')

    return Response('ok'), 200

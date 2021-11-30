import vk_api
from RASPIS import TimeChecker, savelast, GetRaspis, important_checker, saveZoom, loadZoom
from flask import Flask, Response, request
from TeleScout import MessageFilter
import random
import telebot

with open('Token') as f:
    teleToken = f.readline().replace('\n', '', 1)
    token = f.readline()

bot = telebot.TeleBot(teleToken)
bot.set_webhook('https://Zeportuss.pythonanywhere.com/teleRequest')

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

app = Flask(__name__)


#TESTING включает режим тестироващика. При нем все ID, отличные от testerID будут получать оповещение о проведении технических работ.
TESTING = False
testerID = 366782296

def GetUsersId():
    user_id_items = vk.groups.getMembers(group_id='207336652')
    return user_id_items['items']


def sender(id, text, isTele):
    if isTele:
        return text
    else:
        try:
            vk.messages.send(user_id=id, message=text, random_id=random.getrandbits(64))
        except: pass


##Функции для переконвертирования ответа с расписанием в формат сообщения
def RaspisForDay(id, isTele):
    return sender(id, '\n'.join(filter(None, GetRaspis(0))), isTele)


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


def RaspisForWeek(id, isTele):
    return sender(id, '\n'.join([helpDict[i] + '\n' + '\n'.join(filter(None, day))
                          for i, day in enumerate(GetRaspis(1))]), isTele)


def RaspisForWeekDay(id, weekDay, isTele):
    return sender(id, '\n'.join(filter(None, GetRaspis(1)[weekDay])), isTele)


@app.route('/')
def Main():
    PushMessage = TimeChecker()
    if PushMessage:
        lessons_zoom_edit = loadZoom() # После того, как пара прошла, удаляем информацию о ссылке из соответствующего раздела.
        for i in lessons_zoom_edit:
            if i in PushMessage and i != '#аиг': lessons_zoom_edit[i] = 'Скорее всего занятие в ЭИОС. Но может и ссылку еще не скинули.'
        saveZoom(lessons_zoom_edit)

        savelast()
        for i in GetUsersId():
            if (not TESTING) or (TESTING and i == testerID):
                sender(i, PushMessage, False)
        return "Я все отправил"
    return "Нечего отправлять "


@app.route('/reset')
def Reset():
    savelast(t=False)
    return 'Очистил!'


def CommandFilter(id, msg, isTele):
    msg = msg.lower()  # А вот тут я его вернул, так как тут ссылок уже никаких не ожидается.
    if msg == "р":
        return RaspisForDay(id, isTele)
    elif msg == "в":
        return RaspisForWeek(id, isTele)
    elif msg == 'с':
        return sender(id, 'Добро пожаловать!✌🏻\nЭтот бот будет напоминать тебе о паре за 15 минут.\nСоветуем не отключай уведомления.\nСписок команд:\n“р” - расписание на текущий день\n“в” - расписание на всю неделю,\n“пн” - “пт” - расписание на определенный день', isTele)
    elif msg in reversedHelpDict:
        return RaspisForWeekDay(id, reversedHelpDict[msg], isTele)
    elif not isTele: # Тут стоит это условие, чтобы бот в телеге не отсылал это сообщение.
        return sender(id, 'Неверная команда. Напиши "С", чтобы узнать список команд.', isTele)

@app.route('/GetEvent', methods=['POST'])
def GetEvent():
    data = request.get_json()

    if data['type'] =='confirmation':
        return '52e326ff'

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
                CommandFilter(id, msg, False)
            else:
                sender(id, 'Ты не подписан! Я с такими не общаюсь.')
        elif check_id == id: sender(id, 'К сожалению, бесплатный сервер только один. Так что работа бота и его тестировка проходят на одном и том же сервере. Напишите позже.')

    return Response('ok'), 200


@app.route('/teleRequest', methods = ['POST']) # Тут начинается коваться телеграм скаут
def GetUpdates():
    data = request.get_json()

    if 'message' in data and 'title' in data['message']['chat'] and 'text' in data['message']:  # Так проверяем является наше событие сообщением из группы телеграмм.
        if data['message']['chat']['title'] == 'Поток БВТ21':
            important_checker('#вычтех ' + data['message']['text'])  # Добавляем хештег, так как скрипт внесет ссылку в память только если присутствует соответствующий хештег. То есть хештег это как путь.
        elif data['message']['chat']['title'] == 'Введение в ИТ БВТ21 04-06':
            important_checker('#инфтех ' + data['message']['text'])

    if 'message' in data and data['message']['chat']['type'] == 'private':
        msg = data['message']['text']
        userId = data['message']['from']['id']

        teleData = MessageFilter(msg)
        if teleData[1] == 2: teleData[0] = CommandFilter(0, teleData[0], True) # Присылается в teleData[0] р, в или день недели. После чего заменяется на расписание
        bot.send_message(userId, teleData[0])
    return ''
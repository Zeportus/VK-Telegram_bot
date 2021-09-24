import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from RASPIS import TimeChecker, GetRaspis



vk_session = vk_api.VkApi(token='2a85a114c3af837c332b88f804290e76ddf4f326025a20e352d897d41a3fd5c3c2e47bb56a1df0e226f83')
Botlongpoll = VkBotLongPoll(vk_session, 207336652)
session_api = vk_session.get_api()


def GetUsersId():
    user_id_items = vk_session.method('groups.getMembers', {'group_id': '207336652'})
    return user_id_items['items']


def sender(id, text):
    vk_session.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})

def Start():
    PushMessage = TimeChecker()
    if PushMessage != False:
        for i in GetUsersId():
            sender(i, PushMessage)


##Функции для переконвертирования ответа с расписанием в формат сообщения
def RaspisForDay(id):
    raspis = GetRaspis(0)
    message = ''
    for i in raspis:
        message += i + '\n'
    sender(id, message)


helpDict = {
    0 : 'Понедельник:\n',
    1 : 'Вторник:\n',
    2 : 'Среда:\n',
    3 : 'Четверг:\n',
    4 : 'Пятница:\n'
}
def RaspisForWeek(id):
    raspis = GetRaspis(1)
    message = ''
    for i in raspis:
        message += helpDict[i]
        for k in raspis[i]:
            if k != '':
                message += k + '\n'
        message += '\n'
    sender(id, message)

def RaspisForWeekDay(id, weekDay):
    raspis = GetRaspis(1)
    message = ''
    for i in raspis[weekDay]:
        message += i + '\n'
    sender(id, message)





for event in Botlongpoll.listen():
    if event.type == VkBotEventType.GROUP_JOIN:
        id = event.object['user_id']
        sender(id,
               'Добро пожаловать! Этот бот будет напоминать тебе куда идти за 15 минут до пары, так что не отключай уведомления от него. Еще он может:\n1. Выдать расписание на сегодня, для этого напиши "р"\n2. Узнать расписание на всю неделю "в"\n3. Узнать расписание на определенный день. Напиши "Пн", "Вт" и так далее')
    if event.type == VkBotEventType.MESSAGE_NEW:
        msg = event.object['message']['text'].lower()
        id = event.object['message']['peer_id']
        inList = False
        if id in GetUsersId(): inList = True
        if msg == "р" and inList:
            RaspisForDay(id)
        elif msg == "в" and inList:
            RaspisForWeek(id)
        elif msg == 'пн' and inList:
            RaspisForWeekDay(id, 0)
        elif msg == 'вт' and inList:
            RaspisForWeekDay(id, 1)
        elif msg == 'ср' and inList:
            RaspisForWeekDay(id, 2)
        elif msg == 'чт' and inList:
            RaspisForWeekDay(id, 3)
        elif msg == 'пт' and inList:
            RaspisForWeekDay(id, 4)
        elif not inList:
            sender(id, 'Ты не подписан! Я с такими не общаюсь.')

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from RASPIS import TimeChecker, GetRaspis, savelast, getlast
from flask import Flask

app = Flask(__name__)


@app.route('/')
def Main():
    vk_session = vk_api.VkApi(token='2a85a114c3af837c332b88f804290e76ddf4f326025a20e352d897d41a3fd5c3c2e47bb56a1df0e226f83')
    Botlongpoll = VkBotLongPoll(vk_session, 207336652)
    session_api = vk_session.get_api()

    def GetUsersId():
        user_id_items = vk_session.method('groups.getMembers', {'group_id': '207336652'})
        return user_id_items['items']


    def sender(id, text):
        vk_session.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})
    #savelast(t=False)
    PushMessage = TimeChecker()
    if PushMessage:
        savelast()
        for i in GetUsersId():
            sender(i, PushMessage)
        return "Я все отправил"
    return "Нечего отправлять "

@app.route('/reset')
def Reset():
    savelast(t=False)
    return 'Очистил!'



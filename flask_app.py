import vk_api
from RASPIS import TimeChecker, savelast
from flask import Flask

app = Flask(__name__)


@app.route('/')
def Main():
    vk_session = vk_api.VkApi(token='2a85a114c3af837c332b88f804290e76ddf4f326025a20e352d897d41a3fd5c3c2e47bb56a1df0e226f83')
    vk = vk_session.get_api()

    def GetUsersId():
        user_id_items = vk.groups.getMembers(group_id='207336652')
        return user_id_items['items']

    def sender(id, text):
        vk.messages.send(user_id=id, message=text, random_id=0)

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



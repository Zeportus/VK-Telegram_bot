from datetime import datetime, date, timezone, timedelta
import pickle
from functools import partial
import math
import psycopg2

conn = psycopg2.connect(database="d9tvhlu5hrq5n3",
                                     user="ivyzzlxvzrvlnd",
                                     password= 'varvara1',
                                     host="ec2-54-74-35-87.eu-west-1.compute.amazonaws.com",
                                     port="5432")

cursor = conn.cursor()


moscow = timezone(timedelta(hours=3))
now = partial(datetime.now, moscow)


#Ссылки в зум на предметы по хештегам
standart = 'Скорее всего занятие в ЭИОС. Но может и ссылку еще не скинули.'
lessons_zoom = {           # Да костыли пиздец, но я загорелся идеей. Это короче шаблон так сказать. Чтобы при первом запуске работало.
    '#иняз' : standart,
    '#философия' : standart,
    '#аиг' : standart,
    '#вышмат' : standart,
    '#инфэк': standart,
    '#компграф' : standart,
    '#физра' : standart,
    '#вычтех' : standart,
    '#инфтех' : standart
}

def important_checker(message):
    message_to_send = message
    message = message.lower()
    for i in lessons_zoom:
        if i in message and 'zoom' in message:
            message_to_send = message_to_send.replace(i, '', 1) # Удаляем хештег в сообщении. Для этого вообще подойдет регулярное выражение, но я почитал это чет сложно
            if i == '#аиг': message_to_send = message_to_send.replace('#АиГ', '', 1)

            lessons_zoom_edit = loadZoom() # А вот edit это уже то, с чем мы работаем.
            lessons_zoom_edit[i] = message_to_send
            saveZoom(lessons_zoom_edit)


def saveZoom(lessons_zoom):
    with open('zoomLessons.pickle', 'wb') as f:
        pickle.dump(lessons_zoom, f)

def loadZoom():
    try:
        with open('zoomLessons.pickle', 'rb') as f:
            return pickle.load(f)

    except: return lessons_zoom

#А теперь уже читаем из базы. txt отстой
WeekDayDict = {
            0: 'Понедельник',
            1: 'Вторник',
            2: 'Среда',
            3: 'Четверг',
            4: 'Пятница',
            5 : 'Суббота'
        }
TimeLessonDict = {
    0 : '09:30',
    1 : '11:20',
    2 : '13:10',
    3 : '15:25',
    4 : '17:15',
    5 : '19:00'
}

raspis =((([''] * 6), ([''] * 6), ([''] * 6), ([''] * 6), ([''] * 6), ([''] * 6)), (([''] * 6), ([''] * 6), ([''] * 6), ([''] * 6), ([''] * 6), ([''] * 6)))
print(raspis)
def refresh():
    global raspis
    chet = True
    for weekIndex, i in enumerate(raspis): # четная и нечетная
        if weekIndex == 0: chet = True
        else: chet = False
        for dayIndex, j in enumerate(i): # день недели
            weekDay = WeekDayDict[dayIndex]
            for subIndex, k in enumerate(j): # предметы
                    time = TimeLessonDict[subIndex]
                    subject = ''
                    try:
                        cursor.execute(f"SELECT subject, room_numb, start_time FROM timetable WHERE parity = {str(chet)} AND day = '{weekDay}' AND start_time = '{time}';")
                        push_item = list(cursor.fetchall())
                        push_item = list(push_item[0])
                        if push_item:
                            subject = ' '.join(push_item)
                            raspis[weekIndex][dayIndex][subIndex] = subject
                        else: raspis[weekIndex][dayIndex][subIndex] = ''
                    except:
                        raspis[weekIndex][dayIndex][subIndex] = ''
                        conn.rollback()
refresh()



def savelast(t=True):
    with open('data.pickle', 'wb') as f:
        pickle.dump(now() if t else datetime(1, 1, 1, tzinfo=moscow), f)


def getlast():
    try:
        with open('data.pickle', 'rb') as f:
            return pickle.load(f)

    except:
        return datetime(1, 1, 1, tzinfo=moscow)


def TimeChecker():
    nowTime = now()

    if nowTime.weekday() > 4: return None
    for i, timePair in enumerate(timePushPar):
        checkedTime = datetime(nowTime.year, nowTime.month, nowTime.day, timePair[0], timePair[1], tzinfo=moscow)
        if check(nowTime, checkedTime):

            href_zoom = ''
            lessons_zoom_edit = loadZoom()
            for k in lessons_zoom_edit:
                if k in raspis[TimeLogic(nowTime.date())][nowTime.weekday()][i]:
                    href_zoom = lessons_zoom_edit[k]
            return raspis[TimeLogic(nowTime.date())][nowTime.weekday()][i] + '\n\n' + href_zoom

# Четность недели
#В эту функцию мы передаем из Timechecker текущее время. Чтобы использовать ее во flask_app добавлена вот эта строчка.
def TimeLogic(nowTime):
    if not nowTime: nowTime = now().date()
    return ((nowTime - date(nowTime.year, 9, 6)).days // 7) % 2

def WeekCountLogic():
    print (now().date() - date(now().date().year, 9, 5)) #Высталвено 5, ибо с шестого числа недели считаются некорректно
    return str(math.ceil(((now().date() - date(now().date().year, 9, 5)).days / 7)) + 1)


# Функции для обработки запросов от пользователя
def GetRaspis(command):  # 0 - запрос на расписание дня, 1 - запрос на всю неделю
    nowTime = now().date()
    if nowTime.weekday() > 4: nowTime = nowTime.replace(day=nowTime.day + 7 - nowTime.weekday())
    if command == 0:
        return raspis[TimeLogic(nowTime)][nowTime.weekday()]
    elif command == 1:
        return raspis[TimeLogic(nowTime)]
    elif command == 2:
        if TimeLogic(nowTime) == 0: return raspis[1]
        else: return raspis[0]


# GMT+3 MOSCOW TIMEZONE
timePushPar = ((9, 25 +1), (11, 15 +1), (13, 5 +1), (15, 20 +1), (17, 10 +1), (18, 55 +1))


def check(nowtime, checkedtime, dopusk=0, dopuskLast=60):
    lastDataTime = getlast()

    deltaNowPush = max(nowtime, checkedtime) - min(nowtime, checkedtime)
    deltaTimeLast = max(nowtime, lastDataTime) - min(nowtime, lastDataTime)

    return deltaNowPush.seconds // 60 <= dopusk and deltaTimeLast.seconds // 60 >= dopuskLast
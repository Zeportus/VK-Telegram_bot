from datetime import datetime, date, timezone, timedelta
import pickle
from functools import partial

moscow = timezone(timedelta(hours=3))
now = partial(datetime.now, moscow)


#Ссылки в зум на предметы по хештегам
lessons_zoom = {           # Да костыли пиздец, но я загорелся идеей. Это короче шаблон так сказать. Чтобы при первом запуске работало.
    '#иняз' : None,
    '#философия' : None,
    '#аиг' : None,
    '#вышмат' : None,
    '#инфэк': None,
    '#компграф' : None,
    '#физра' : None,
    '#вычтех' : None,
    '#инфтех' : None
}

def important_checker(message):
    message_to_send = message
    message = message.lower()
    for i in lessons_zoom:
        if i in message and 'zoom' in message:
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

#Читаем файл с расписанием
raspis =((([''] * 5), ([''] * 5), ([''] * 5), ([''] * 5), ([''] * 5)), (([''] * 5), ([''] * 5), ([''] * 5), ([''] * 5), ([''] * 5)))
ChetDict = {
    'Четная:' : 0,
    'Нечетная:' : 1,
}
WeekDayDict = {
    'Понедельник:': 0,
    'Вторник:': 1,
    'Среда:': 2,
    'Четверг:': 3,
    'Пятница:': 4
}
TimeLessonDict = {
    '(09.30)' : 0,
    '(11.20)' : 1,
    '(13.10)' : 2,
    '(15.25)' : 3,
    '(17.15)' : 4
}
with open('RaspisInfo.txt', 'r') as f:
    Week = 0
    WeekDay = 0

    for i in f:
        i = i.replace('\n', '')
        if i in ChetDict: Week = ChetDict[i]
        elif i in WeekDayDict: WeekDay = WeekDayDict[i]
        else:
            for k in TimeLessonDict.keys():
                if k in i:
                    raspis[Week][WeekDay][TimeLessonDict[k]] = i



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
def TimeLogic(nowTime):
    return ((nowTime - date(nowTime.year, 9, 6)).days // 7) % 2


# Функции для обработки запросов от пользователя
def GetRaspis(command):  # 0 - запрос на расписание дня, 1 - запрос на всю неделю
    nowTime = now().date()
    if nowTime.weekday() > 4: nowTime = nowTime.replace(day=nowTime.day + 7 - nowTime.weekday())
    if command == 0:
        return raspis[TimeLogic(nowTime)][nowTime.weekday()]
    elif command == 1:
        return raspis[TimeLogic(nowTime)]


# GMT+3 MOSCOW TIMEZONE
timePushPar = ((9, 25), (11, 15), (13, 5), (15, 20), (17, 10))


def check(nowtime, checkedtime, dopusk=1, dopuskLast=60):
    lastDataTime = getlast()

    deltaNowPush = max(nowtime, checkedtime) - min(nowtime, checkedtime)
    deltaTimeLast = max(nowtime, lastDataTime) - min(nowtime, lastDataTime)

    return deltaNowPush.seconds // 60 <= dopusk and deltaTimeLast.seconds // 60 >= dopuskLast
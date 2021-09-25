from datetime import datetime, date, time
import pickle

def savelast(t=True):
    with open('data.pickle', 'wb') as f:
        pickle.dump(datetime.now() if t else datetime.combine(date(1, 1, 1), time(0, 0)), f)

def getlast():
    try:
        with open('data.pickle', 'rb') as f:
            return pickle.load(f)

    except: return datetime.combine(date(1, 1, 1), time(0, 0))


def TimeChecker():
    nowTime = datetime.now()
    if nowTime.weekday() > 4: return None
    for k, i in enumerate(timePushPar):
        checkedTime = datetime.combine(date(datetime.now().year, datetime.now().month, datetime.now().day), i)
        if check(nowTime, checkedTime):
            return raspis[TimeLogic(nowTime.date())][nowTime.weekday()][k]


def TimeLogic(nowTime):
    return ((nowTime - date(datetime.now().year, 9, 6)).days // 7) % 2



#Функции для обработки запросов от пользователя
def GetRaspis(command): # 0 - запрос на расписание дня, 1 - запрос на всю неделю
    nowTime = date(datetime.now().year, datetime.now().month, datetime.now().day)
    if nowTime.weekday() > 4: nowTime = nowTime.replace(day = nowTime.day + 7 - nowTime.weekday())
    if command == 0:
        return raspis[TimeLogic(nowTime)][nowTime.weekday()]
    elif command == 1:
        return raspis[TimeLogic(nowTime)]

raspis = ({
    0: ('(09.30) Введение в инф.тех. пр.з. ауд.ВЦ127','(11.20) Вычислительная техника лаб. ауд. 314', '(13.10) Иностранный язык ауд. 404, 301б',
        '(15.25) Комп.графика пр.з. ауд.223', ''),
    1: ('(09.30) Физкультура и спорт', '(11.20) Философия пр.з  ауд.318','','',''),
    2: ('','','','(15.25) Введение в инф.тех. пр.з. ауд.ВЦ116', '(17.15) Введение в инф.тех. пр.з. ауд.ВЦ116'),
    3: ('(09.30) Инф.экология лек. ауд.347', '(11.20) Вычислительная техника лек.ауд.310',
        '(13.10) Комп.графика лек. ауд.126','',''),
    4: ('','(11.20) Инф.экология лаб. ауд.339', '(13.10) Высшая математика пр.з. ауд.504а',
        '(15.00) Физкультура и спорт',
        '(17.15) Алгебра и геометрия пр.з. ауд.508'),
},
{
    0: ('(09.30) Введение в инф.тех. пр.з. ауд.ВЦ127', '(11.20) Вычислительная техника пр.з.. ауд. 314',
        '(13.10) Иностранный язык ауд. 404, 301б',
        '(15.25) Комп.графика пр.з. ауд.223', ''),
    1: ('(09.30) Физкультура и спорт', '(11.20) Философия пр.з  ауд.318', '', '', ''),
    2: ('(09.30) Высш.математика лек. ауд.522', '(11.20) Алгебра и геометрия лек.ауд.347', '(13.10) Введение в инф.тех.лек.ауд.517', '', ''),
    3: ('(09.30) Философия лек. ауд.514', '(11.20) Вычислительная техника лек.ауд.310', '', '', ''),
    4: ('', '', '(13.10) Высш.математика пр.з. ауд.504а', '(15.00) Физкультура и спорт', '(17.15) Алгебра и геометрия пр.з. ауд.508'),
}
)
timePushPar = (time(6, 15), time(8, 5), time(9, 55), time(12, 10), time(14, 0)) # Час выставляется на 3 меньше нужного, в связи с разницей серверного и московского времени

def check(nowtime,checkedtime,dopusk = 2, dopuskLast = 60):
    lastDataTime = getlast()

    deltaNowPush = max(nowtime, checkedtime) - min(nowtime, checkedtime)
    deltaTimeLast = max(nowtime, lastDataTime) - min(nowtime, lastDataTime)

    return deltaNowPush.seconds // 60 <= dopusk and deltaTimeLast.seconds // 60 >= dopuskLast
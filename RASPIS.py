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
    for k, i in enumerate(timePushPar):
        checkedTime = datetime.combine(date(datetime.now().year, datetime.now().month, datetime.now().day), i)
        if check(nowTime, checkedTime):
            return raspis[TimeLogic(nowTime.date())][nowTime.weekday()][k]


def TimeLogic(nowTime):
    return ((nowTime - date(datetime.now().year, 9, 6)).days // 7) % 2



#Функции для обработки запросов от пользователя
def GetRaspis(command): # 0 - запрос на расписание дня, 1 - запрос на всю неделю
    nowTime = date(datetime.now().year, datetime.now().month, datetime.now().day)
    if command == 0:
        return raspis[TimeLogic(nowTime)][nowTime.weekday()]
    elif command == 1:
        return raspis[TimeLogic(nowTime)]

raspis = ({
    0: ('','(11.20) Выч.тех. лаб. ауд. 314', '(13.10) Ин. яз. ауд. 404, 301б',
        '(15.25) Комп.графика пр.з. ауд.223 Ирина Ивановна Пискарёва', '(17.15) Вв.в инф.тех. пр.з. ауд.ВЦ127'),
    1: ('(09.30) Физ. культура и спорт Наталья Николаевна', '(11.20) Философия ауд.318 Андрей Владимирович Глинский','','',''),
    2: ('','','','(15.25) Вв. ssв инф.тех. пр.з.ауд.ВЦ116', '(17.15) Вв. в инф.тех. пр.з.ауд.ВЦ116'),
    3: ('(09.30) Инф.экология лек. ауд.347', '(11.20) Выч.тех. лек.ауд.310',
        '(13.10) Комп.графика лек.Рывлина А.А. ауд.126','',''),
    4: ('','(11.20) Инф.экология лаб. ауд.339', '(13.10) Высш.мат. пр.з. Ирина Васильевна Гетманская ауд.504а',
        '(15.25) Физ.культура и спорт Наталья Николаевна',
        '(17.15) Алг. и геом. пр.з. Андрей Валентинович Куприн ауд.508'),
},
{
  0: ('', '(11.20) Выч.тех. пр.з. ауд. 314', '(13.10) Ин. яз. ауд. 404, 301б',
      '(15.25) Комп.графика пр.з. ауд.223 Ирина Ивановна Пискарёва',
      '(17.15) Вв.в инф.тех. пр.з. ауд.ВЦ127'),
  1: ('(09.30) Физ. культура и спорт Наталья Николаевна',
      '(11.22) Философия ауд.318 Андрей Владимирович Глинский', '', '', ''),
  2: ('(09.30) "Высш.мат лек. Ирина Васильевна Гетманская ауд.522',
      '(11.20) Алг и геом лек. Андрей Валентинович Куприн Ауд.347', '(13.10) Вв. в инф.тех. лек. ауд.517',
      '', ''),
  3: ('(09.30) Философия лек. Андрей Владимирович Глинскийауд.514', '(11.20) Выч.тех. лек.ауд.310',
      '(13.10) Высш.мат. лек. Ирина Васильевна Гетманская ауд.347', '', ''),
  4: ('', '',
      '(13.10) Высш.мат. пр.з. Ирина Васильевна Гетманская ауд.504а',
      '(15.25) Физ.культура и спорт Наталья Николаевна',
      '(17.15) Алг. и геом. пр.з. Андрей Валентинович Куприн ауд.508'),
}
)
timePushPar = (time(6, 15), time(8, 5), time(9, 55), time(12, 10), time(14, 0)) # Час выставляется на 3 меньше нужного, в связи с разницей серверного и московского времени

def check(nowtime,checkedtime,dopusk = 2, dopuskLast = 60):
    lastDataTime = getlast()

    deltaNowPush = max(nowtime, checkedtime) - min(nowtime, checkedtime)
    deltaTimeLast = max(nowtime, lastDataTime) - min(nowtime, lastDataTime)

    return deltaNowPush.seconds // 60 <= dopusk and deltaTimeLast.seconds // 60 >= dopuskLast
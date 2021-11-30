import random

answers = ('Креативно', 'Находчиво', 'Классно', 'Может сменим тему?', 'Ты явно не в духе', 'Не оценил', 'Понимаю', 'Получается так',
           'Тебе так интересно?', 'Душновато стало', 'Я очень люблю расписания', 'Классный фильм недавно посмотрел', 'На это мне нечего ответить',
           'Ладно, сдаюсь', 'Ненавижу это место', 'Как же я рад быть именно тут!', 'Видимо, магнитные бури', 'Так, кто убил Марка?', 'Дистант', 'ГОСТ, переделать')
#Типы: 1 - передать текстовое сообщение, 2 - работа с расписанием
def MessageFilter(message):
    if message == '/today' or message == '/mon' or message == '/tue' or message == '/wed' or message == '/thu' or message == '/fri' or message == '/week':
        return [CommandFilter(message), 2]

    elif message == 'кто ты?':  return ['Я бот, а ты?', 1]
    elif message == '/start': return ['Привет! Я могу предоставить тебе твое расписание. Напиши /help, чтобы узнать команды.', 1]
    elif message == '/help': return ['/today - расписание на сегодня\n/mon, /tue, /wed, /thu, /fri - расписание на день недели\n/week - расписание на неделю', 1]
    else: return [answers[random.randint(0, 19)], 1]

def CommandFilter(message):
    text = ''
    if message == '/today': text = 'р'
    elif message == '/mon': text = 'пн'
    elif message == '/tue': text = 'вт'
    elif message == '/wed': text = 'ср'
    elif message == '/thu': text = 'чт'
    elif message == '/fri': text = 'пт'
    elif message == '/week': text = 'в'

    return text
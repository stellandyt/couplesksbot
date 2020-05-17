import telebot
from telebot import types
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime, date

# token = '1212598847:AAGeXxqtliVIM28IaluDH-ohrXIF2tGnGjg'
token = '1251055643:AAG8-sdJbarH15vOgHOqzWSVBmDicRMRTSc'
bot = telebot.TeleBot(token)

global days
days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
URL = 'https://www.ks54.ru/расписание-онлайн/?group=2-ИСП11-6'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36 OPR/67.0.3575.130'}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет!', reply_markup=keyboard())


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    text = message.text
    if text == 'Привет' or text == 'привет':
        bot.send_message(message.chat.id, 'Хааааай', reply_markup=keyboard())
    elif text == 'На завтра':
        get_content(message)
    elif text == 'Замены':
        bot.send_message(message.chat.id, 'Получаю ближайшие замены...\n')
        getInfoZamena(message)
    elif text == 'Сегодня':
        getInfoToday(message)
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю!', reply_markup=keyboard())

#--------------------------------------------------------------------------------
def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r


def getInfoToday(message):
    html = get_html(URL)

    if html.status_code == 200:
        html = html.text
    else:
        print("Error")

    a = getInfoSchedule(html)  # Словарь "День": [Пары]

    #Получение дня недели
    mydate = str(datetime.today().isoweekday())
    print(mydate)
    if mydate == '6' or mydate == '7':
        bot.send_message(message.chat.id, 'Сегодня нет пар :)', reply_markup=keyboard())
    else:
        dates = {'1': 'Понедельник', '2': 'Вторник', '3': 'Среда', '4': 'Четверг', '5': 'Пятница', '6': 'Суббота', '7': 'Воскресенье', }
        day = str(dates[mydate[0]])
        print(day)

        print(a)
        mass = []

        if day in a:
            mass.append('Сегодня: ' + str(day) + '\n\n')
            for i in a[day]:
                if i == '1' or i == '2' or i == '3' or i == '4':
                    if i == '1':
                        a = ('Номер пары: ' + str(i) + '\n')
                        mass.append(a)
                    else:
                        a = ('\nНомер пары: ' + str(i) + '\n')
                        mass.append(a)
                else:
                    try:
                        num = int(i)
                        mass.append('Кабинет: ' + str(num) + '\n')
                    except:
                        mass.append(str(i) + '\n')

        text = ''

        for line in mass:
            text += str(line)
        bot.send_message(message.chat.id, str(text), reply_markup=keyboard())


def get_content(message):
    html = get_html(URL)

    if html.status_code == 200:
        html = html.text
    else:
        print("Error")

    a = getInfoSchedule(html)  # Словарь "День": [Пары]

    # Получение дня недели
    mydate1 = int(datetime.today().isoweekday())
    mydate1 += 1
    mydate = str(mydate1)
    print(mydate)

    if mydate == '6' or mydate == '7':
        bot.send_message(message.chat.id, 'Завтра нет пар :)', reply_markup=keyboard())
    else:
        dates = {'1': 'Понедельник', '2': 'Вторник', '3': 'Среда', '4': 'Четверг', '5': 'Пятница', '6': 'Суббота',
                 '7': 'Воскресенье', '8': 'Понедельник'}
        day = str(dates[mydate[0]])
        print(day)

        print(a)
        mass = []

        if day in a:
            mass.append('Завтра: ' + str(day) + '\n\n')
            for i in a[day]:
                if i == '1' or i == '2' or i == '3' or i == '4':
                    if i == '1':
                        a = ('Номер пары: ' + str(i) + '\n')
                        mass.append(a)
                    else:
                        a = ('\nНомер пары: ' + str(i) + '\n')
                        mass.append(a)
                else:
                    try:
                        num = int(i)
                        mass.append('Кабинет: ' + str(num) + '\n')
                    except:
                        mass.append(str(i) + '\n')

        text = ''

        for line in mass:
            text += str(line)
        bot.send_message(message.chat.id, str(text), reply_markup=keyboard())


# Получение информации о расписании
def getInfoSchedule(html):
    day = ""
    pars = {"Понедельник": [], "Вторник": [], "Среда": [], "Четверг": [], "Пятница": []}

    soup = BeautifulSoup(html, "html.parser")
    Tabs = soup.findAll("table", {"class": "bcol w100"})

    mainTab = Tabs[0]
    tds = mainTab.findAll("td")

    for element in tds:
        if element.text in days:
            day = element.text
            continue
        if element.text == 'ОП6':
            continue
        else:
            pars[day].append(element.text)
    return pars


#Получение информации о заменах
def getInfoZamena(message):
    html = get_html(URL)

    if html.status_code == 200:
        html = html.text
    else:
        print("Error")

    soup = BeautifulSoup(html, "html.parser")
    Tabs = soup.findAll("table", {"class": "bcol w100"})

    mass = []
    try:
        mainTab = Tabs[1]
        tds = mainTab.findAll("td")
        for i in tds:
            print(i.text)
            if i.text == '1' or i.text == '2' or i.text == '3' or i.text == '4':
                para = ('Номер пары: ' + str(i.text))
                mass.append(para)
            if i.text == 'ЗАМЕНА':
                continue
            else:
                text = i.text
                if text == '1' or i.text == '2' or i.text == '3' or i.text == '4':
                    continue
                else:
                    mass.append(text)
        del mass[-1]
        print(mass)
    except:
        net_zam = 'Замен нет'
        print("Замен нет")

    if net_zam == 'Замен нет':
        bot.send_message(message.chat.id, 'Замен нет', reply_markup=keyboard())
    else:
        result = ''
        for i in mass:
            result += str(i + '\n')
        result = 'Дата: ' + result
        bot.send_message(message.chat.id, result, reply_markup=keyboard())


def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn_1 = types.KeyboardButton('Help')
    btn_2 = types.KeyboardButton('Сегодня')
    btn_3 = types.KeyboardButton('На завтра')
    btn_4 = types.KeyboardButton('Замены')
    markup.add(btn_3, btn_2)
    markup.add(btn_1, btn_4)
    return markup

while True:
    try:
        bot.polling(none_stop=True, timeout=123, interval=0)
    except Exception as E:
        print(E.args)
        time.sleep(2)

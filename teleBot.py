import telebot
import os.path
import datetime
import requests

bot = telebot.TeleBot('1413517685:AAEgYWUg70K5mn9LyfPPKhIBo6u9GnwHmNo')

Login = ''
projectName = ''


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Этот бот поможеть вам скачать проект из github.')
    bot.send_message(message.chat.id, 'Введите ваш логин на github:')
    bot.register_next_step_handler(message, getName)


def getName(message):
    global Login
    Login = message.text
    bot.send_message(message.chat.id, 'Привет ' + Login + '!', parse_mode='Markdown')
    bot.send_message(message.chat.id, 'Введите пожалуйста название проекта, который надо скачать:')
    bot.register_next_step_handler(message, getNameProject)


def getNameProject(message):
    global projectName
    projectName = message.text
    bot.send_message(message.chat.id, "Название вашего проекта - " + projectName + "!")

    check_file = os.path.exists(getFileName(projectName))
    if not check_file:
        status_code, result = downloadFile(Login, projectName)
        if status_code == 200:
            bot.send_document(message.chat.id, result)
        else:
            bot.send_message(message.chat.id, result)

    else:
        kun = os.path.getmtime(getFileName(projectName))
        kun1 = datetime.datetime.fromtimestamp(kun)
        a = datetime.datetime.today()
        if (a - kun1).days < 7:
            bot.send_document(message.chat.id, open(getFileName(projectName), "rb"))
        else:
            status_code, result = downloadFile(Login, projectName)
            if status_code == 200:
                bot.send_document(message.chat.id, result)
            else:
                bot.send_message(message.chat.id, result)


def downloadFile(Login, projectName):
    url = 'https://github.com/'
    download_url = url + Login + '/' + projectName + '/' + 'archive/master.zip'
    r = requests.get(download_url)
    print(r.status_code)

    if r.status_code == 200:
        with open(projectName + ".zip", "wb") as code:
            code.write(r.content)
        return 200, open(getFileName(projectName), "rb")
    else:
        return 404, "Проект таким названием не найден!"


def getFileName(projectName):
    base_path = "C:\\Users\\mjk29\\PycharmProjects\\bot\\"
    return base_path + projectName + ".zip"


bot.polling(none_stop=True, interval=0)

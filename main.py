from bs4 import BeautifulSoup
import requests
import telebot

TOKEN = 'TOKEN'
bot = telebot.TeleBot(TOKEN)

url = 'https://www.kp.ru/family/ecology/globalnoe-poteplenie/?ysclid=m59a1wivuh251661056'

response = requests.get(url)
response.encoding = 'utf-8'
bs = BeautifulSoup(response.text, "html.parser")
a1 = bs.find("div", class_="article__description")  
a2 = bs.find_all("h3", class_="wp-block-heading") 


if a1:
    intro_text = a1.text.strip()
else:
    intro_text = "Описание статьи не найдено."

filtered_a2r = []
start_collecting = False
for i in a2:
    text = i.text.strip()
    if text.startswith("1. Выработка электроэнергии"):
        start_collecting = True
    if start_collecting:
        filtered_a2r.append(text)
    if text.startswith("7. Избыточное потребление"):
        break

filtered_a2c = []
start_collecting = False
for i in a2:
    text = i.text.strip()
    if text.startswith("1. Резкое изменение климата"):
        start_collecting = True
    if start_collecting:
        filtered_a2c.append(text)
    if text.startswith("5. Исчезновение видов фауны и флоры"):
        break

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Здравствуйте, это телеграмм бот, который ознакомит вас с темой глобального потепления.")
    bot.send_message(message.chat.id, intro_text)
    bot.send_message(message.chat.id, """Список доступных команд:
/help
/reas
/cons""")

@bot.message_handler(commands=["help"])
def handle_help(message):
    bot.send_message(message.chat.id, """Список доступных команд:
/start - введение
/help - список команд
/reas - причины ГП
/cons - последствия""")

@bot.message_handler(commands=['reas'])
def handle_reas(message):
    if filtered_a2r:
        bot.send_message(message.chat.id, "Причины ГП:")
        for i in filtered_a2r:
            bot.send_message(message.chat.id, i)

@bot.message_handler(commands=['cons'])
def handle_cons(message):
    if filtered_a2c:
        bot.send_message(message.chat.id, "Последствия ГП:")
        for i in filtered_a2c:
            bot.send_message(message.chat.id, i)

bot.polling(none_stop=True)

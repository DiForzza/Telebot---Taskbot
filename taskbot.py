import telebot
from telebot import types
import openpyxl
# @test4456_bot

bot = telebot.TeleBot('1530619842:AAH20gD_rs72BX9HsXlef2avhbxMPXUiROk')
wb = openpyxl.load_workbook('sotr/auth.xlsx')
sheet = wb.active
rows = sheet.max_row
cols = sheet.max_column

def auth(phone_usm, chatid):
    global auth_ok
    for i in range(1, rows + 1):
        basenumber = sheet.cell(row=i, column=2)
        name_surname = sheet.cell(row=i, column=1)
        #bot.send_message(chatid, f'Доброго времени суток, {phone_usm}, {basenumber.value}, {name_surname.value}.')
        if int(phone_usm) == int(basenumber.value):
            auth_ok = 1
            bot.send_message(chatid, f'Доброго времени суток, {name_surname.value}.')
    return auth_ok

@bot.message_handler(commands=["start"])
def geophone(message):
    keyboard1 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    keyboard1.add(button_phone)
    bot.send_message(message.chat.id, "Пройдите авторизацию по номеру телефона", reply_markup=keyboard1)

@bot.message_handler(content_types=['contact'])
def read_contact_phone(message):
    global auth_ok
    auth_ok = 0
    phone_usm = message.contact.phone_number
    chatid = message.chat.id
    auth(phone_usm, chatid)
    if auth_ok == 0:
        bot.send_message(chatid, f'Авторизация не пройдена. Номера не существует. {auth_ok}')
    else:
        keyboard2 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_task = types.KeyboardButton(text="Просмотр своих задач")
        button_settask = types.KeyboardButton(text="Поставить задачу")
        keyboard2.add(button_task, button_settask)
        bot.send_message(message.chat.id, "Выберите интересующий пункт меню:", reply_markup=keyboard2)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == 'Просмотр своих задач':
        bot.send_message(message.chat.id, f'Привет')
    elif message.text.lower() == 'Поставить задачу':
        bot.send_message(message.chat.id, 'Поставить задачу')
    elif message.text.lower() == 'Мои задачи':
        bot.send_message(message.chat.id, 'Мои задачи')
    elif message.text.lower() == 'Отметить задачу':
        bot.send_message(message.chat.id, 'Отметить задачу')

bot.polling()

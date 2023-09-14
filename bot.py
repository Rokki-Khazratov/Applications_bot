import telebot
import sqlite3
from datetime import datetime
from telebot import types  


bot_token = '6385398548:AAE0I5NSCsFMIO5-Srol1KF3ssQcrPBVU-Y'

bot = telebot.TeleBot(bot_token)

db_path = 'bot_data.db'

channel_chat_id = '@studygram_applications'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS applications (
                user_id INTEGER,
                name TEXT,
                phone TEXT,
                date_time TEXT,
                voice_message BLOB)''')
conn.commit()

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Studygramga Hush kelibsiz! Arizani yaratishni boshlaymiz.\n"
                                      "Ism va familiyangizni yozing:")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    chat_id = message.chat.id
    name = message.text
    bot.send_message(chat_id, "Yahshi! Endi telefon raqamingizni:")
    bot.register_next_step_handler(message, get_phone, name)

def get_phone(message, name):
    chat_id = message.chat.id
    phone = message.text


    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')


    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()


    user_id = message.from_user.id
    cursor.execute("INSERT INTO applications (user_id, name, phone, date_time) VALUES (?, ?, ?, ?)",
                   (user_id, name, phone, current_time))
    conn.commit()


    conn.close()


    bot.send_message(channel_chat_id, f"Новая заявка:\n"
                                      f"Имя: {name}\n"
                                      f"Номер телефона: {phone}\n"
                                      f"Дата и время: {current_time}\n")


    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    item = types.KeyboardButton("Kontakt bilan ulashish", request_contact=True)
    markup.add(item)
    bot.send_message(chat_id, f"Rahamt! Sizning arizangiz muafaqiyatli qabul qilindi.\n"
                              f"Bizning adminstratorlarimiz 24 soat ichida siz bilan bog'lanishadi.\n"
                              f"Iltimos, Arizani tasdiqlash uchun kontaktingiz bilan ulashing.",
                     reply_markup=markup)
    bot.register_next_step_handler(message, confirm_contact, name, phone)

def confirm_contact(message, name, phone):
    chat_id = message.chat.id
    contact = message.contact


    bot.send_contact(channel_chat_id, contact.phone_number, contact.first_name, contact.last_name)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):

    pass

bot.polling(none_stop=True)
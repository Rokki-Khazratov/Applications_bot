import telebot
import sqlite3
from datetime import datetime
from telebot import types

bot_token = '6385398548:AAE0I5NSCsFMIO5-Srol1KF3ssQcrPBVU-Y'

bot = telebot.TeleBot(bot_token)

db_path = 'bot_data.db'

channel_chat_id = '-1001904523145'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS applications (
                application_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                name TEXT,
                phone TEXT,
                date_time TEXT)''')
conn.commit()

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Studygramga Hush kelibsiz! Arizani yaratishni boshlaymiz.\n"
                                      "Ism va familiyangizni yozing:")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    chat_id = message.chat.id
    name = message.text

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    user_id = message.from_user.id
    cursor.execute("INSERT INTO applications (user_id, name, date_time) VALUES (?, ?, ?)",
                   (user_id, name, current_time))
    conn.commit()

    conn.close()

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    item = types.KeyboardButton("Kontakt bilan ulashish", request_contact=True)
    markup.add(item)

    bot.send_message(chat_id, "Iltimos, Arizani tasdiqlash uchun kontaktingiz bilan ulashing.", reply_markup=markup)
    bot.register_next_step_handler(message, confirm_contact, name)

def confirm_contact(message, name):
    chat_id = message.chat.id

    bot.send_message(chat_id, f"Rahamt! Sizning arizangiz muafaqiyatli qabul qilindi.\n"
                            f"Bizning adminstratorlarimiz 24 soat ichida siz bilan bog'lanishadi.")

    application_id = cursor.lastrowid
    
    # Вызываем функцию для отправки контакта в канал с передачей application_id
    send_contact_to_channel(message, name, application_id)


def send_contact_to_channel(message, name, application_id):
    chat_id = channel_chat_id
    contact = message.contact

    bot.send_message(channel_chat_id, f"Новая заявка :\n"
                                    f"Имя: {name}\n"
                                    f"Номер телефона: ({contact.phone_number})\n")

    bot.send_contact(chat_id, contact.phone_number, contact.first_name, contact.last_name)


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    pass

bot.polling(none_stop=True)

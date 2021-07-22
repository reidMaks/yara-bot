import os
import telebot
from telebot import types
from dataBase import Event, session

bot = telebot.TeleBot(os.environ.get('TG_BOT_TOKEN', None))
OWNERS = os.environ.get('OWNER_ID', [])
EAT_BTN = '🍼Еда'
SLEEP_BTN = '😴 Сон'
WALK_BTN = '🚶 Прогулка'
SHIT_BTN = '💩 О мой б-г, это случилось'


def eat_btn_on_click(message):
    f = Event("eat")
    session.add(f)
    session.commit()


def sleep_btn_on_click(message):
    f = Event("sleep")
    session.add(f)
    session.commit()


def walk_btn_on_click(message):
    save_event(Event("walk"))


def shit_btn_on_click(message):
    save_event(Event("shit"))


def save_event(event):
    session.add(event)
    session.commit()


keyboard_mapper = {
    EAT_BTN: eat_btn_on_click,
    SLEEP_BTN: sleep_btn_on_click,
    WALK_BTN: walk_btn_on_click,
    SHIT_BTN: shit_btn_on_click
}


@bot.message_handler(func=lambda message: its_master(message.chat.id) and keyboard_mapper.get(message.text) is not None)
def keyboard_btn(message):
    keyboard_mapper[message.text](message)


@bot.message_handler(func=lambda message: its_master(message.chat.id))
def set_keyboard(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)

    btn1 = types.KeyboardButton(EAT_BTN)
    btn2 = types.KeyboardButton(SLEEP_BTN)
    btn3 = types.KeyboardButton(WALK_BTN)
    btn4 = types.KeyboardButton(SHIT_BTN)

    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.chat.id, reply_markup=markup)


def its_master(user_id):
    return OWNERS.find(str(user_id)) >= 0


if __name__ == 'bot':
    bot.polling(none_stop=True)

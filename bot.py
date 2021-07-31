import os
import re

from config import BOT_TOKEN, OWNERS
import datetime
import telebot
from telebot import types
from repository import EventManager, Event, statistic
from graphics import get_eat_graphic

EAT_BTN = '🍼Еда'
SLEEP_BTN = '😴 Сон'
WALK_BTN = '🚶 Прогулка'
SHIT_BTN = '💩 О мой б-г, это случилось'
BATH_BTN = '🛁 Купание'
STAT_BTN = '📈 Статистика'

PIN_MSG_EAT = None

bot = telebot.TeleBot(BOT_TOKEN)
EventManager = EventManager()
# Буфер используется для хранения данных от редактируемом событии
# на время ожидания пользовательского ввода
call_buffer = ''


def eat_btn_on_click(message):
    record = EventManager.save_event(Event("eat"))
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2

    markup.add(get_value_btn(record.id))
    markup.add(get_comment_btn(record.id))
    markup.add(get_remove_btn(record.id))

    bot.reply_to(message, text=record, reply_markup=markup)


def sleep_btn_on_click(message):
    record = EventManager.save_event(Event("sleep"))
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2

    markup.add(get_end_time_btn(record.id))
    markup.add(get_comment_btn(record.id))
    markup.add(get_remove_btn(record.id))

    bot.reply_to(message, text=f"""{record}\n
        Пора готовить следующий прием пищи ;)
        Бутылочка чистая? а воды кипяченой хватает?""", reply_markup=markup)


def walk_btn_on_click(message):
    record = EventManager.save_event(Event("walk"))
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2

    markup.add(get_end_time_btn(record.id))
    markup.add(get_comment_btn(record.id))
    markup.add(get_remove_btn(record.id))

    bot.reply_to(message, text=f"""{record}\n
        Хорошей прогулки! 
        Может в будущем я научусь рассказывать прогноз погоды?""", reply_markup=markup)


def shit_btn_on_click(message):
    record = EventManager.save_event(Event("shit"))

    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2

    markup.add(get_remove_btn(record.id))
    bot.reply_to(message, text=f"""{record}\n
        Это определенно успех!""", reply_markup=markup)


def bath_btn_on_click(message):
    record = EventManager.save_event(Event("bath"))

    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2

    markup.add(get_remove_btn(record.id))
    bot.reply_to(message, text=f"""{record}\n
        С легким паром!""", reply_markup=markup)


def stat_btn_on_click(message):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 3

    markup.add(types.InlineKeyboardButton("Как давно кушали?", callback_data='statistic,how-long-ago,,eat'))
    markup.add(types.InlineKeyboardButton("Сколько раз покакали?", callback_data='statistic,how-many,today,shit'))
    markup.add(types.InlineKeyboardButton("Сколько съели сегодня?", callback_data='statistic,how-much,today,eat'))
    markup.add(types.InlineKeyboardButton("Вчера купались?", callback_data='statistic,have,yesterday,bath'))
    markup.add(types.InlineKeyboardButton("График еды", callback_data='graphic,eat'))

    bot.reply_to(message, text='Что интересует?', reply_markup=markup)


def update_event_record(message):
    global call_buffer
    record_id, field_name = call_buffer.data.split(',')

    if field_name == 'value':
        value = int(message.text)  # todo: Добавить проверку пользовательского ввода
    elif field_name == 'comment':
        value = message.text
    elif field_name == 'end_time':
        value = datetime.datetime.now()
    else:
        raise Exception('Получено не корректное значение value для события')

    upd_event = EventManager.update_event(record_id, {field_name: value})
    bot.answer_callback_query(call_buffer.id, 'Событие обновлено')
    bot.edit_message_text(upd_event, chat_id=call_buffer.message.chat.id, message_id=call_buffer.message.id,
                          reply_markup=call_buffer.message.reply_markup)

    call_buffer = ''


def remove_event(call):
    global call_buffer
    record_id, _ = call_buffer.data.split(',')

    EventManager.remove_event(record_id)
    call_buffer = ''

    bot.answer_callback_query(call.id, "Событие удалено!", show_alert=True)
    bot.delete_message(call.message.chat.id, call.message.id)


def get_value_btn(record_id):
    return types.InlineKeyboardButton("Добавить объем", callback_data=f"{record_id},value")


def get_comment_btn(record_id):
    return types.InlineKeyboardButton("Добавить комментарий", callback_data=f"{record_id},comment")


def get_end_time_btn(record_id):
    return types.InlineKeyboardButton("Завершить", callback_data=f"{record_id},end_time")


def get_remove_btn(record_id):
    return types.InlineKeyboardButton("❌", callback_data=f"{record_id},remove")


def get_statistic(call_back):
    if 'statistic' in call_back.data:
        answer = statistic(call_back.data)

        if answer is None:
            answer = 'Не знаю ;('

        bot.send_message(call_back.message.chat.id, answer)


def get_graph(call_back):
    if 'graphic' in call_back.data:
        pic_path = get_eat_graphic()
        bot.send_photo(call_back.message.chat.id, open(pic_path, 'rb'))

        os.remove(pic_path)


keyboard_mapper = {
    EAT_BTN: eat_btn_on_click,
    SLEEP_BTN: sleep_btn_on_click,
    WALK_BTN: walk_btn_on_click,
    SHIT_BTN: shit_btn_on_click,
    STAT_BTN: stat_btn_on_click,
    BATH_BTN: bath_btn_on_click
}


def eat_time_switcher(time: str) -> str:
    time = datetime.datetime.strptime(time, '%H:%M:%S')
    m = time.hour * 60 + time.minute

    return {
        m < 60: '🙂',
        60 <= m < 90: '🤔',
        90 <= m < 120: '😕',
        120 <= m < 180: '😡',
        180 <= m: '🤬'
    }[True]


@bot.message_handler(commands=['event'])
def send_events(message):
    result = EventManager.query() \
        .filter(Event.time >= datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)) \
        .order_by(Event.time.desc()).all()
    answer = [str(i) for i in result]

    if answer.count() == 0:
        answer = ["Событий нет"]
    bot.reply_to(message, "\n".join(answer))


@bot.message_handler(commands=['pin-eat'])
def upd_pin_eat(message):
    # обновление возможно только в чате в котором команда вызвана в последний раз
    # прикрепленное сообщение не хранится в БД и будет сброшено при перезапуске
    global PIN_MSG_EAT

    time = statistic("statistic,how-long-ago,,eat")
    text = f'{eat_time_switcher(time)} последний прием пищи {time} назад'
    if PIN_MSG_EAT is None:

        if message is None:
            return True

        send = bot.reply_to(message, text)
        bot.pin_chat_message(message.chat.id, send.id)
        PIN_MSG_EAT = send
    else:
        bot.edit_message_text(text, message_id=PIN_MSG_EAT.id,
                              chat_id=PIN_MSG_EAT.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global call_buffer
    call_buffer = call
    if 'value' in call.data or 'comment' in call.data:
        send = bot.send_message(text=f"Пиши {'объем в мл.' if 'value' in call.data else 'комментарий'}",
                                chat_id=call.message.chat.id)
        bot.register_next_step_handler(send, update_event_record)
    elif 'remove' in call.data:
        remove_event(call)
    elif 'end_time' in call.data:
        update_event_record(call.message)
    elif 'statistic' in call.data:
        get_statistic(call)
    elif 'graphic' in call.data:
        get_graph(call)


@bot.message_handler(func=lambda message: is_masters_message(message) and keyboard_mapper.get(message.text) is not None)
def keyboard_btn(message):
    keyboard_mapper[message.text](message)


@bot.message_handler(regexp=r"(еда|прогулка|купание|покакали|сон)?\s\d{1,2}(-|:|;)\d{1,2}?\s\d{1,4}")
def add_event(message):
    rx = re.compile(r"(еда|прогулка|купание|покакали|сон)?\s(\d{1,2}([-:;])\d{1,2})?\s(\d{1,4})", flags=re.IGNORECASE)
    action, time, _, value = rx.findall(message.text)[0]

    event = EventManager.create_event(action, time, value)

    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2

    markup.add(get_remove_btn(event.id))

    bot.reply_to(message, f"✅  Создал событие {event}", reply_markup=markup)


@bot.message_handler(func=lambda message: is_masters_message(message))
def set_keyboard(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)

    markup.add(types.KeyboardButton(EAT_BTN))
    markup.add(types.KeyboardButton(SLEEP_BTN))
    markup.add(types.KeyboardButton(WALK_BTN))
    markup.add(types.KeyboardButton(SHIT_BTN))
    markup.add(types.KeyboardButton(BATH_BTN))
    markup.add(types.KeyboardButton(STAT_BTN))

    bot.reply_to(message, text='Здоров', reply_markup=markup)


def is_masters_message(message):
    return OWNERS.find(str(message.from_user.id)) >= 0

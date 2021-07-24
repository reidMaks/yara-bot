from config import BOT_TOKEN, OWNERS
import datetime
import telebot
from telebot import types
from repository import EventManager, Event

EAT_BTN = '🍼Еда'
SLEEP_BTN = '😴 Сон'
WALK_BTN = '🚶 Прогулка'
SHIT_BTN = '💩 О мой б-г, это случилось'
STAT_BTN = '📈 Статистика'

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

    bot.send_message(text=record, chat_id=message.chat.id, reply_markup=markup)


def sleep_btn_on_click(message):
    record = EventManager.save_event(Event("sleep"))
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2

    markup.add(get_end_time_btn(record.id))
    markup.add(get_comment_btn(record.id))

    bot.send_message(text=f"""{record}\n
        Пора готовить следующий прием пищи ;)
        Бутылочка чистая? а воды кипяченой хватает?""",
                     chat_id=message.chat.id, reply_markup=markup)


def walk_btn_on_click(message):
    record = EventManager.save_event(Event("walk"))
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2

    markup.add(get_end_time_btn(record.id))
    markup.add(get_comment_btn(record.id))

    bot.send_message(text=f"""{record}\n
        Хорошей прогулки! 
        Может в будущем я научусь рассказывать прогноз погоды?""",
                     chat_id=message.chat.id, reply_markup=markup)


def shit_btn_on_click(message):
    record = EventManager.save_event(Event("shit"))

    bot.send_message(text=f"""{record}\n
        Это определенно успех!""",
                     chat_id=message.chat.id)


def stat_btn_on_click(message):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2

    markup.add(types.InlineKeyboardButton("Когда кушать?", callback_data='statistic'))
    markup.add(types.InlineKeyboardButton("Сколько раз покакали?", callback_data='statistic,how-many-shit'))
    markup.add(types.InlineKeyboardButton("Сколько съели сегодня?", callback_data='statistic'))
    markup.add(types.InlineKeyboardButton("Вчера купались?", callback_data='statistic'))

    bot.send_message(text='Что интересует?',
                     chat_id=message.chat.id, reply_markup=markup)


def update_event_record(message):
    global call_buffer
    record_id, field_name = call_buffer.split(',')

    if field_name == 'value':
        value = int(message.text)  # todo: Добавить проверку пользовательского ввода
    elif field_name == 'comment':
        value = message.text
    elif field_name == 'end_time':
        value = datetime.datetime.now()
    else:
        raise Exception('Получено не корректное значение value для события')

    EventManager.update_event(record_id, {field_name: value})
    call_buffer = ''


def get_value_btn(record_id):
    return types.InlineKeyboardButton("Добавить объем", callback_data=f"{record_id},value")


def get_comment_btn(record_id):
    return types.InlineKeyboardButton("Добавить комментарий", callback_data=f"{record_id},comment")


def get_end_time_btn(record_id):
    return types.InlineKeyboardButton("Завершить", callback_data=f"{record_id},end_time")


def get_statistic(call_back):
    if 'how-many-shit' in call_back.data:
        result = EventManager.query(). \
            filter(Event.type == 'shit', Event.time <= datetime.datetime.today()) \
            .order_by(Event.time.desc())
        answer = ''
        if result is None:
            answer = \
                f"""За сегодня нет записей
                Последняя запись """
        else:
            answer = \
                f"""За сегодня {result.count()} раз(-а), Последний в {format(result[0].time, '%H:%M')}"""

        bot.send_message(call_back.message.chat.id, answer)


keyboard_mapper = {
    EAT_BTN: eat_btn_on_click,
    SLEEP_BTN: sleep_btn_on_click,
    WALK_BTN: walk_btn_on_click,
    SHIT_BTN: shit_btn_on_click,
    STAT_BTN: stat_btn_on_click
}


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global call_buffer
    call_buffer = call.data
    if 'value' in call.data or 'comment' in call.data:
        send = bot.send_message(text="Пиши", chat_id=call.message.chat.id)
        bot.register_next_step_handler(send, update_event_record)
    elif 'end_time' in call.data:
        update_event_record(call.message)
    elif 'statistic' in call.data:
        get_statistic(call)


@bot.message_handler(func=lambda message: is_master(message.chat.id) and keyboard_mapper.get(message.text) is not None)
def keyboard_btn(message):
    keyboard_mapper[message.text](message)


@bot.message_handler(func=lambda message: is_master(message.chat.id))
def set_keyboard(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)

    markup.add(types.KeyboardButton(EAT_BTN))
    markup.add(types.KeyboardButton(SLEEP_BTN))
    markup.add(types.KeyboardButton(WALK_BTN))
    markup.add(types.KeyboardButton(SHIT_BTN))
    markup.add(types.KeyboardButton(STAT_BTN))

    bot.send_message(text='Здоров', chat_id=message.chat.id, reply_markup=markup)


def is_master(user_id):
    return OWNERS.find(str(user_id)) >= 0


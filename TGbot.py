import os
import re

from config import BOT_TOKEN
import datetime
import telebot
from telebot import types
from repository import EventManager, EventModel, statistic
from graphics import get_eat_graphic
from Classes.AnswerStrategy import *

PIN_MSG_EAT = None

bot = telebot.TeleBot(BOT_TOKEN)


#
# EventManager = EventManager()
# # Буфер используется для хранения данных от редактируемом событии
# # на время ожидания пользовательского ввода
# call_buffer = ''
#
#
# def eat_btn_on_click(message):
#     record = EventManager.save_event(EventModel("eat"))
#     markup = types.InlineKeyboardMarkup()
#     markup.row_width = 2
#
#     markup.add(get_value_btn(record.id))
#     markup.add(get_comment_btn(record.id))
#     markup.add(get_remove_btn(record.id))
#
#     bot.reply_to(message, text=record, reply_markup=markup)
#
#
# def sleep_btn_on_click(message):
#     record = EventManager.save_event(EventModel("sleep"))
#     markup = types.InlineKeyboardMarkup()
#     markup.row_width = 2
#
#     markup.add(get_end_time_btn(record.id))
#     markup.add(get_comment_btn(record.id))
#     markup.add(get_remove_btn(record.id))
#
#     bot.reply_to(message, text=f"""{record}\n
#         Пора готовить следующий прием пищи ;)
#         Бутылочка чистая? а воды кипяченой хватает?""", reply_markup=markup)
#
#
# def walk_btn_on_click(message):
#     record = EventManager.save_event(EventModel("walk"))
#     markup = types.InlineKeyboardMarkup()
#     markup.row_width = 2
#
#     markup.add(get_end_time_btn(record.id))
#     markup.add(get_comment_btn(record.id))
#     markup.add(get_remove_btn(record.id))
#
#     bot.reply_to(message, text=f"""{record}\n
#         Хорошей прогулки!
#         Может в будущем я научусь рассказывать прогноз погоды?""", reply_markup=markup)
#
#
# def shit_btn_on_click(message):
#     record = EventManager.save_event(EventModel("shit"))
#
#     markup = types.InlineKeyboardMarkup()
#     markup.row_width = 2
#
#     markup.add(get_remove_btn(record.id))
#     bot.reply_to(message, text=f"""{record}\n
#         Это определенно успех!""", reply_markup=markup)
#
#
# def bath_btn_on_click(message):
#     record = EventManager.save_event(EventModel("bath"))
#
#     markup = types.InlineKeyboardMarkup()
#     markup.row_width = 2
#
#     markup.add(get_remove_btn(record.id))
#     bot.reply_to(message, text=f"""{record}\n
#         С легким паром!""", reply_markup=markup)
#
#
# def stat_btn_on_click(message):
#     markup = types.InlineKeyboardMarkup()
#     markup.row_width = 3
#
#     markup.add(types.InlineKeyboardButton("Как давно кушали?", callback_data='statistic,how-long-ago,,eat'))
#     markup.add(types.InlineKeyboardButton("Сколько раз покакали?", callback_data='statistic,how-many,today,shit'))
#     markup.add(types.InlineKeyboardButton("Сколько съели сегодня?", callback_data='statistic,how-much,today,eat'))
#     markup.add(types.InlineKeyboardButton("Вчера купались?", callback_data='statistic,have,yesterday,bath'))
#     markup.add(types.InlineKeyboardButton("График еды", callback_data='graphic,eat'))
#
#     bot.reply_to(message, text='Что интересует?', reply_markup=markup)
#
#
# def update_event_record(message):
#     global call_buffer
#     record_id, field_name = call_buffer.data.split(',')
#
#     if field_name == 'value':
#         value = int(message.text)  # todo: Добавить проверку пользовательского ввода
#     elif field_name == 'comment':
#         value = message.text
#     elif field_name == 'end_time':
#         value = datetime.datetime.now()
#     else:
#         raise Exception('Получено не корректное значение value для события')
#
#     upd_event = EventManager.update_event(record_id, {field_name: value})
#     bot.answer_callback_query(call_buffer.id, 'Событие обновлено')
#     bot.edit_message_text(upd_event, chat_id=call_buffer.message.chat.id, message_id=call_buffer.message.id,
#                           reply_markup=call_buffer.message.reply_markup)
#
#     call_buffer = ''
#
#
# def remove_event(call):
#     global call_buffer
#     record_id, _ = call_buffer.data.split(',')
#
#     EventManager.remove_event(record_id)
#     call_buffer = ''
#
#     bot.answer_callback_query(call.id, "Событие удалено!", show_alert=True)
#     bot.delete_message(call.message.chat.id, call.message.id)
#
#
# def get_value_btn(record_id):
#     return types.InlineKeyboardButton("Добавить объем", callback_data=f"{record_id},value")
#
#
# def get_comment_btn(record_id):
#     return types.InlineKeyboardButton("Добавить комментарий", callback_data=f"{record_id},comment")
#
#
# def get_end_time_btn(record_id):
#     return types.InlineKeyboardButton("Завершить", callback_data=f"{record_id},end_time")
#
#
# def get_remove_btn(record_id):
#     return types.InlineKeyboardButton("❌", callback_data=f"{record_id},remove")
#
#
# def get_statistic(call_back):
#     if 'statistic' in call_back.data:
#         answer = statistic(call_back.data)
#
#         if answer is None:
#             answer = 'Не знаю ;('
#
#         bot.send_message(call_back.message.chat.id, answer)
#
#
# def get_graph(call_back):
#     if 'graphic' in call_back.data:
#         pic_path = get_eat_graphic()
#         bot.send_photo(call_back.message.chat.id, open(pic_path, 'rb'))
#
#         os.remove(pic_path)
#
#
# keyboard_mapper = {
#     EAT_BTN: eat_btn_on_click,
#     SLEEP_BTN: sleep_btn_on_click,
#     WALK_BTN: walk_btn_on_click,
#     SHIT_BTN: shit_btn_on_click,
#     STAT_BTN: stat_btn_on_click,
#     BATH_BTN: bath_btn_on_click
# }
#
#
# def eat_time_switcher(time: str) -> str:
#     assert type(time) is str
#     regexp = r"(\d{1,2}):(\d{1,2}):(\d{1,2})"
#     assert re.fullmatch(regexp, time) is not None
#
#     h, m, s = re.findall(regexp, time)[0]
#     m = int(h) * 60 + int(m) + int(s) / 60
#
#     return {
#         m < 60: '🙂',
#         60 <= m < 90: '🤔',
#         90 <= m < 120: '😕',
#         120 <= m < 180: '😡',
#         180 <= m: '🤬'
#     }[True]
#

@bot.message_handler(commands=['start'])
def on_start(message):
    controller = MessageController(message, bot)
    controller.set_strategy(StartCommandStrategy)
    controller.send_answer()


@bot.message_handler(commands=['help'])
def on_help(message):
    controller = MessageController(message, bot)
    controller.set_strategy(HelpCommandStrategy)
    controller.send_answer()


@bot.message_handler(commands=['events'])
def send_events(message):
    controller = MessageController(message, bot)
    controller.set_strategy(EventsCommandStrategy)
    controller.send_answer()


@bot.message_handler(commands=['pin'])
def upd_pin_eat(message):
    controller = MessageController(message, bot)
    controller.set_strategy(PinCommandStrategy)
    controller.send_answer()

#
#
# @bot.callback_query_handler(func=lambda call: True)
# def callback_query(call):
#     global call_buffer
#     call_buffer = call
#     if 'value' in call.data or 'comment' in call.data:
#         send = bot.send_message(text=f"Пиши {'объем в мл.' if 'value' in call.data else 'комментарий'}",
#                                 chat_id=call.message.chat.id)
#         bot.register_next_step_handler(send, update_event_record)
#     elif 'remove' in call.data:
#         remove_event(call)
#     elif 'end_time' in call.data:
#         update_event_record(call.message)
#     elif 'statistic' in call.data:
#         get_statistic(call)
#     elif 'graphic' in call.data:
#         get_graph(call)
#     elif 'event_from_str' in call.data:
#         add_event_from_str_continue(call=call)
#
#
# @bot.message_handler(func=lambda message: is_masters_message(message) and keyboard_mapper.get(message.text) is not None)
# def keyboard_btn(message):
#     keyboard_mapper[message.text](message)
#
#
# @bot.message_handler(regexp=r"(еда|прогулка|купание|покакали|сон)?\s\d{1,2}(-|:|;)\d{1,2}?\s\d{1,4}")
# def add_event_from_str(message):
#     rx = re.compile(r"(еда|прогулка|купание|покакали|сон)?\s(\d{1,2}([-:;])\d{1,2})?\s(\d{1,4})", flags=re.IGNORECASE)
#     action, time, _, value = rx.findall(message.text)[0]
#
#     h, _, m = re.findall(r"(\d{1,2})([-:;])(\d{1,2})", time)[0]
#     h = int(h)
#     m = int(m)
#
#     if h > 23 or m > 59:
#         bot.reply_to(message, "Получено не правильное время. Не могу создать событие")
#         return
#
#     current_time = datetime.datetime.now()
#     time = f"{h}:{m}"
#
#     if current_time.hour * 60 + current_time.minute < h * 60 + m:
#         text = f'Переданное время {time} больше текущего {current_time.strftime("%H:%M")}' \
#                f'\nВыбери, что делать дальше:'
#
#         markup = types.InlineKeyboardMarkup()
#         markup.row_width = 2
#
#         time = current_time.replace(hour=h, minute=m, second=0, microsecond=0)
#         time = time - datetime.timedelta(days=1)
#
#         markup.add(types.InlineKeyboardButton("⏰ Внести вчерашней датой",
#                                               callback_data=f"event_from_str,{action},{time},{value}"))
#         markup.add(types.InlineKeyboardButton("❌ Это ошибка. Забудь", callback_data=f"event_from_str,error"))
#
#         bot.reply_to(message, text, reply_markup=markup)
#         return
#
#     add_event_from_str_continue(message=message, action=action, time=time, value=value)
#
#
# def add_event_from_str_continue(**kwargs) -> None:
#     if 'call' in kwargs:
#         call = kwargs['call']
#
#         if 'error' in call.data:
#             bot.answer_callback_query(call.id, "Событие удалено!", show_alert=True)
#             bot.delete_message(call.message.chat.id, call.message.id)
#             return
#         else:
#             _, action, time, value = call.data.split(',')
#             time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
#             message = call.message
#
#             bot.delete_message(call.message.chat.id, call.message.id)
#     else:
#         action = kwargs['action']
#         time = kwargs['time']
#         value = kwargs['value']
#         message = kwargs['message']
#
#     event = EventManager.create_event(action, time, value)
#
#     markup = types.InlineKeyboardMarkup()
#     markup.row_width = 2
#
#     markup.add(get_remove_btn(event.id))
#
#     bot.send_message(message.chat.id, f"✅  Создал событие {event}", reply_markup=markup)

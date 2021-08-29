import schedule
import time
from threading import Thread

from loguru import logger
import TGbot

from db import PinnedMessages, DB
from config import UPD_PIN_INTERVAL
from BotHelper import last_eat_time_message


@logger.catch
def upd_pin():
    text = last_eat_time_message()

    for pinned in DB().session.query(PinnedMessages).all():
        TGbot.bot.edit_message_text(text=text, chat_id=pinned.chat_id, message_id=pinned.msg_id)


def do_schedule():
    schedule.every(UPD_PIN_INTERVAL).seconds.do(upd_pin)

    while True:
        schedule.run_pending()
        time.sleep(1)


thread = Thread(target=do_schedule)

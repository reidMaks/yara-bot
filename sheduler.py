import schedule
import time
from threading import Thread
from bot import upd_pin_eat


def upd_pin():
    upd_pin_eat(None)


def do_schedule():
    schedule.every(60).seconds.do(upd_pin)

    while True:
        schedule.run_pending()
        time.sleep(1)


thread = Thread(target=do_schedule)

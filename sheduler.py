import schedule
import time
from threading import Thread
from bot import upd_pin_eat
from config import UPD_PIN_INTERVAL


def upd_pin():
    print(f"{time.strftime('%b %d %Y %H:%M:%S')} DO upd_pin_eat")
    upd_pin_eat(None)


def do_schedule():
    schedule.every(UPD_PIN_INTERVAL).seconds.do(upd_pin)

    while True:
        schedule.run_pending()
        time.sleep(1)


thread = Thread(target=do_schedule)

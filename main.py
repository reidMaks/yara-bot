from bot import bot
from db import Base, engine
from sheduler import thread

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    bot.polling(none_stop=True)

    thread.start()


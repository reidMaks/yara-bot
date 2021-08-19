from TGbot import bot
from db import Base, engine
from sheduler import thread

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # thread.start()

    bot.polling(none_stop=True)




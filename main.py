from bot import bot
from db import Base, engine

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    bot.polling(none_stop=True)


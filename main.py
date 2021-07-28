from bot import bot
from db import Base, engine
from alembic import command
from alembic.config import Config

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # alembic_cfg = Config("./alembic.ini")
    # command.stamp(alembic_cfg, "head")
    bot.polling(none_stop=True)


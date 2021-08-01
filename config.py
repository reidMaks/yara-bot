import os


def isProduction():
    return os.environ.get("DATABASE_URL", None) is not None


OWNERS = os.environ.get('OWNER_ID', [])
BOT_TOKEN = os.environ.get('TG_BOT_TOKEN', None)

PG_USER = os.environ.get('PG_USER', '')
PG_PWD = os.environ.get('PG_PWD', '')
PG_SRV = os.environ.get('PG_SRV', '')

if not isProduction():
    DB_URL = f"postgresql://{PG_USER}:{PG_PWD}@{PG_SRV}/yara-bd"
else:
    DB_URL = os.environ.get("DATABASE_URL", None).replace("postgres", "postgresql", 1)

UPD_PIN_INTERVAL = int(os.environ.get('UPD_PIN_INTERVAL', '300'))  # интревал обновление прикрепленного сообщения в секундах

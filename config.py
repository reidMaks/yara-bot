import os
from typing import Union
import logging

DATABASE_URL = os.environ.get("DATABASE_URL", '')
DEFAULT_UPD_PIN_INTERVAL = 300  # интревал обновление прикрепленного сообщения в секундах


def is_production() -> bool:
    return bool(DATABASE_URL) and bool(DATABASE_URL.strip())


OWNERS: Union[str, list] = os.environ.get('OWNER_ID', [])
BOT_TOKEN = os.environ.get('TG_BOT_TOKEN', None)

PG_USER = os.environ.get('PG_USER', '')
PG_PWD = os.environ.get('PG_PWD', '')
PG_SRV = os.environ.get('PG_SRV', '')

if not is_production():
    DB_URL = f"postgresql://{PG_USER}:{PG_PWD}@{PG_SRV}/yara-bd"
else:
    DB_URL = DATABASE_URL.replace("postgres", "postgresql", 1)

try:
    UPD_PIN_INTERVAL = int(
        os.environ.get('UPD_PIN_INTERVAL', DEFAULT_UPD_PIN_INTERVAL))
except ValueError as e:
    UPD_PIN_INTERVAL = DEFAULT_UPD_PIN_INTERVAL
    logging.exception(e)
except Exception as e:
    raise



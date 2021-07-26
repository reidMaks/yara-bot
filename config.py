import os

OWNERS = os.environ.get('OWNER_ID', [])
BOT_TOKEN = os.environ.get('TG_BOT_TOKEN', None)

PG_USER = os.environ.get('PG_USER', '')
PG_PWD = os.environ.get('PG_PWD', '')
PG_SRV = os.environ.get('PG_SRV', '')
DB_URL = f"postgresql://{PG_USER}:{PG_PWD}@{PG_SRV}/yara-bd"

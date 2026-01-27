# core/time.py
from datetime import datetime
from zoneinfo import ZoneInfo
from core.settings import settings

SERVER_TZ = ZoneInfo(settings.TIMEZONE)

def now():
    return datetime.now(tz=SERVER_TZ)
0
import re
from datetime import datetime
from typing import Optional

from ..core import DATETIME_FORMAT


def format_datetime(d: datetime) -> str:
    return d.strftime(DATETIME_FORMAT)


def parse_time(t: str) -> Optional[int]:
    if result := re.findall(r"^(\d*):(\d*)$", t):
        return int(result[0][0]) * 60 + int(result[0][1])
    return None

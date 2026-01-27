from datetime import time

def parse_hours(hours_str: str):
    """
    "09:00-12:00,16:00-19:00"
    → [(09:00, 12:00), (16:00, 19:00)]
    """
    ranges = []
    if not hours_str:
        return ranges

    for part in hours_str.split(","):
        start, end = part.split("-")
        h1, m1 = map(int, start.split(":"))
        h2, m2 = map(int, end.split(":"))
        ranges.append((time(h1, m1), time(h2, m2)))

    return ranges

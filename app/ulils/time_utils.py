from datetime import (
    datetime,
    time,
    timedelta,
)


def get_seconds_until_1411() -> int:
    now = datetime.now()
    clear_time = datetime.combine(now.date(), time(14, 11))

    if now >= clear_time:
        clear_time += timedelta(days=1)

    return int((clear_time - now).total_seconds())

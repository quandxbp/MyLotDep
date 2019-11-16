import schedule
import time


def run_job(period, func, amount=10, start=True):

    if period == 'second':
        schedule.every(amount).seconds.do(func)
    elif period == 'minute':
        schedule.every(amount).minutes.do(func)
    elif period == 'hour':
        schedule.every(amount).hours.do(func)
    elif period == 'day':
        schedule.every(amount).days.do(func)

    while start:
        schedule.run_pending()
        time.sleep(1)

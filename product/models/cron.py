import schedule
import time
import datetime
import logging


def run_scheduler(period, func, params={}, amount=10, start=True):
    logging.info("Run Scheduler at %s" % datetime.datetime.now())
    if period == 'second':
        schedule.every(amount).seconds.do(func, params)
    elif period == 'minute':
        schedule.every(amount).minutes.do(func, params)
    elif period == 'hour':
        schedule.every(amount).hours.do(func, params)
    elif period == 'day':
        schedule.every(amount).days.do(func, params)

    while start:
        schedule.run_pending()
        time.sleep(1)

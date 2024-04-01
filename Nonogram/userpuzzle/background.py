from apscheduler.schedulers.background import BackgroundScheduler
import os
import shutil
import time
from django.conf import settings

def job():
    print("Interval: Check temp folder.")
    if os.path.exists(settings.TEMP_MEDIA_ROOT):
        if os.listdir(settings.TEMP_MEDIA_ROOT):
            shutil.rmtree(settings.TEMP_MEDIA_ROOT)
            print("  Temp folder cleared.")

def start():
    sched = BackgroundScheduler()
    sched.add_job(job, 'interval', seconds=10)
    sched.start()
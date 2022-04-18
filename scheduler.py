import time
from threading import Thread

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


class Scheduler(Thread):
    def __init__(self, on_change_screen=None):
        super().__init__()
        self.on_change_screen = on_change_screen
        self.daemon = True

        self.scheduler = BackgroundScheduler()
        # self.scheduler.add_job(self.change_screen, CronTrigger.from_crontab('* 7-10 * * 0,2,4k'))
        self.scheduler.add_job(self.change_screen, CronTrigger.from_crontab('* * * * 0,2,4'))
        self.screens = ["weather", "gym_count", "clock"]
        self.idx = 0

    def run(self):
        print("starting scheduler")
        print(self.scheduler.get_jobs())
        self.scheduler.start()
        while True: # TODO make cancelable
            time.sleep(1)

    def change_screen(self):
        self.on_change_screen(self.screens[self.idx])
        self.idx = (self.idx + 1) % len(self.screens)



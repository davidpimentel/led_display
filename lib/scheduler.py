import time
from threading import Thread

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


class Scheduler(Thread):
    def __init__(self, schedule, on_change_screen=None):
        super().__init__()
        self.on_change_screen = on_change_screen
        self.daemon = True
        self.schedule = schedule

        self.scheduler = BackgroundScheduler({"apscheduler.timezone": "US/Eastern"})
        self.load_schedule()

    def load_schedule(self):
        for schedule in self.schedule:
            screens = schedule["screens_ids"]
            cron = schedule["cron"]
            scheduled_job = ScheduledJob(screens, self.on_change_screen)
            self.scheduler.add_job(scheduled_job.change_screen, CronTrigger.from_crontab(cron), coalesce=True)

    def run(self):
        self.scheduler.start()
        while True: # TODO make cancelable
            time.sleep(1)


class ScheduledJob:
    def __init__(self, screens, on_change_screen):
        self.screens = screens
        self.on_change_screen = on_change_screen
        self.idx = 0

    def change_screen(self):
        self.on_change_screen(self.screens[self.idx])
        self.idx = (self.idx + 1) % len(self.screens)

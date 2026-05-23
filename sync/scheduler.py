from apscheduler.schedulers.blocking import BlockingScheduler
from canvas_client import get_all_assignments
from notion_sync import sync_assignments
import time

scheduler = BlockingScheduler()

def sync_job():
    print("Starting sync...")
    assignments = get_all_assignments()
    sync_assignments(assignments)
    print("Sync finished.")

@scheduler.scheduled_job("interval", minutes=60)
def scheduled_sync():
    sync_job()

if __name__ == "__main__":
    print("Zaiper sync engine started. Running first sync now...")
    sync_job()
    scheduler.start()
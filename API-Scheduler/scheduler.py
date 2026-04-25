import datetime
import time
import threading
import logging
import requests
import webbrowser   

# ---------------- CONFIG ----------------
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

logging.basicConfig(
    filename='Log.txt',
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("Scheduler")

# ---------------- FUNCTIONS ----------------

def validate_time_format(time_str):
    try:
        datetime.datetime.strptime(time_str, "%H:%M:%S")
        return True
    except ValueError:
        return False


def format_time(time_str):
    today = datetime.datetime.now().date()
    t = datetime.datetime.strptime(time_str, "%H:%M:%S").time()
    target = datetime.datetime.combine(today, t)

    if target < datetime.datetime.now():
        target += datetime.timedelta(days=1)

    return target


def hit_url(url, time_stamp, open_browser=False):
    url = url.strip() 

    thread_name = threading.current_thread().name
    target_time = format_time(time_stamp)

    delay = (target_time - datetime.datetime.now()).total_seconds()

    if delay < 0:
        delay = 0

    print(f"[{thread_name}] Scheduled {url} at {time_stamp} (in {int(delay)} sec)")

    if delay > 0:
        time.sleep(delay)

    attempt = 0
    success = False

    while attempt < MAX_RETRIES and not success:
        try:
            start = time.time()
            response = requests.get(url)
            response_time = round((time.time() - start) * 1000, 2)

            if response.status_code == 200:
                print(f"[{thread_name}] SUCCESS: {url}")
                logger.info(f"{url} | SUCCESS | {response.status_code} | {response_time}ms")

                # Browser open feature
                if open_browser:
                    webbrowser.open(url)

                success = True
            else:
                print(f"[{thread_name}] FAILED: {url} | Status {response.status_code}")
                logger.warning(f"{url} | FAILED | {response.status_code}")

        except Exception as e:
            print(f"[{thread_name}] ERROR: {e}")
            logger.error(f"{url} | ERROR | {e}")

        attempt += 1

        if not success and attempt < MAX_RETRIES:
            print(f"[{thread_name}] Retrying... ({attempt})")
            time.sleep(RETRY_DELAY)

    if not success:
        print(f"[{thread_name}] FINAL FAILURE: {url}")


def start_scheduler(tasks, open_browser=False):
    threads = []

    for url, time_stamp in tasks:
        thread = threading.Thread(
            target=hit_url,
            args=(url, time_stamp, open_browser)
        )
        thread.start()
        threads.append(thread)

    return threads
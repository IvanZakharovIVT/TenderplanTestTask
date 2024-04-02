from celery import Celery

from consts import MAIN_ADDRESS, SEARCH_ADDRESS, PAGINATOR_SUFFIX, REDIS_HOST
from my_tasks.link_task import LinkTask
from my_tasks.page_task import PageTask


app = Celery('tasks', broker=REDIS_HOST)
app.conf.broker_url = REDIS_HOST
app.register_task(PageTask())
app.register_task(LinkTask())

if __name__ == "__main__":
    """
        celery run command
        celery -A main worker --loglevel=INFO --pool=solo
    """

    page_request_href = f"{MAIN_ADDRESS}{SEARCH_ADDRESS}{PAGINATOR_SUFFIX}{1}"

    for page_number in range(1, 3):
        page_request_href = f"{MAIN_ADDRESS}{SEARCH_ADDRESS}{PAGINATOR_SUFFIX}{page_number}"
        task = PageTask().delay(page_request_href)

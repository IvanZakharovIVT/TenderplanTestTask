import re
import time

from celery import Celery

from custom_request import CustomRequest
from my_tasks.link_task import LinkTask
from my_tasks.page_task import PageTask

main_address = "https://zakupki.gov.ru"
search_address = "/epz/order/extendedsearch/results.html"
paginator_suffix = "?fz44=on&pageNumber="

pattern = re.compile(r'/epz/.+printForm/view.html.+regNumber=\d+')


app = Celery('tasks', broker='redis://localhost:6379/0')
app.conf.broker_url = 'redis://localhost:6379/0'

app.register_task(PageTask())
app.register_task(LinkTask())

my_request = CustomRequest()

page_request_href = f"{main_address}{search_address}{paginator_suffix}{1}"

for page_number in range(1, 3):
    page_request_href = f"{main_address}{search_address}{paginator_suffix}{page_number}"
    task = PageTask().delay(page_request_href)
    time.sleep(10)
    # task.get()

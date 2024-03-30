import requests
from bs4 import BeautifulSoup, Tag
import re
import time
import xmltodict
import celery


class MyException(Exception):
    def __init__(self, message):
        super().__init__(message)


sess = requests.Session()
headers = {
    'Content-type': 'text/html;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
}
sess.headers.update(headers)

main_address = "https://zakupki.gov.ru"
search_address = "/epz/order/extendedsearch/results.html"
paginator_suffix = "?fz44=on&pageNumber="

pattern = re.compile(r'/epz/.+printForm/view.html.+regNumber=\d+')
# some_result = requests.get("https://zakupki.gov.ru/epz/order/extendedsearch/results.html")


def convert_url(inner_url: Tag) -> str:
    href = inner_url.attrs['href']
    href = href.replace("view.html", "viewXml.html")
    return f"{main_address}{href}"


def do_request(request_url: str) -> str:
    try_count = 0
    while try_count < 5:
        some_result = sess.get(request_url)
        if some_result.status_code == 200:
            return some_result.text
        try_count += 1
        time.sleep(2)
    raise MyException("Превышено количество запросов")


page_request_href = f"{main_address}{search_address}{paginator_suffix}{1}"

some_result = do_request(page_request_href)

soup = BeautifulSoup(some_result, 'html.parser')

test1 = soup.find_all(name="a", href=pattern)
test_arr = [convert_url(item) for item in test1]

reg1 = r"publishDTInEIS\>.+\<"
reg2 = r"\d.+\d"

for item in test_arr:
    request = do_request(item)
    btf = xmltodict.parse(request)
    publishDTInEIS = None
    level1 = btf.get('ns7:epNotificationEZT2020')
    if level1:
        level2 = level1.get('commonInfo')
        if level2:
            publishDTInEIS = level2.get('publishDTInEIS', None)
    print(f"publishDTInEIS: {publishDTInEIS}")
print(12)

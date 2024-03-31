from bs4 import BeautifulSoup, Tag
import re
import time
import xmltodict

from custom_exception import MyException
from custom_request import CustomRequest


main_address = "https://zakupki.gov.ru"
search_address = "/epz/order/extendedsearch/results.html"
paginator_suffix = "?fz44=on&pageNumber="

pattern = re.compile(r'/epz/.+printForm/view.html.+regNumber=\d+')


def convert_url(inner_url: Tag) -> str:
    href = inner_url.attrs['href']
    href = href.replace("view.html", "viewXml.html")
    return f"{main_address}{href}"


my_request = CustomRequest()

page_request_href = f"{main_address}{search_address}{paginator_suffix}{1}"

some_result = my_request.get(page_request_href)

soup = BeautifulSoup(some_result, 'html.parser')

test1 = soup.find_all(name="a", href=pattern)
test_arr = [convert_url(item) for item in test1]

reg1 = r"publishDTInEIS\>.+\<"
reg2 = r"\d.+\d"

for item in test_arr:
    request = my_request.get(item)
    btf = xmltodict.parse(request)
    publishDTInEIS = None
    level1 = btf.get('ns7:epNotificationEZT2020')
    if level1:
        level2 = level1.get('commonInfo')
        if level2:
            publishDTInEIS = level2.get('publishDTInEIS', None)
    print(f"publishDTInEIS: {publishDTInEIS}")
print(12)

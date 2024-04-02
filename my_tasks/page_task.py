from bs4 import BeautifulSoup, Tag
from celery import Task

from consts import SEARCH_PATTERN, MAIN_ADDRESS
from custom_request import CustomRequest
from my_tasks.link_task import LinkTask


class PageTask(Task):
    name = 'page_task'

    def _convert_url(self, inner_url: Tag) -> str:
        href = inner_url.attrs['href']
        href = href.replace("view.html", "viewXml.html")
        return f"{MAIN_ADDRESS}{href}"

    def run(self, page_url: str):
        print(page_url)
        request = CustomRequest()
        response = request.get(page_url)

        soup = BeautifulSoup(response.text, 'html.parser')

        all_tags = soup.find_all(name="a", href=SEARCH_PATTERN)
        converted_ult_list = [self._convert_url(item) for item in all_tags]

        for item in converted_ult_list:
            LinkTask().delay(item)
        return True


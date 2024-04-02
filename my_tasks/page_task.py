import re

from bs4 import BeautifulSoup, Tag
from celery import Task

from custom_request import CustomRequest
from my_tasks.link_task import LinkTask


class PageTask(Task):
    name = 'page_task'
    main_address = "https://zakupki.gov.ru"
    pattern = re.compile(r'/epz/.+printForm/view.html.+regNumber=\d+')

    def _convert_url(self, inner_url: Tag) -> str:
        href = inner_url.attrs['href']
        href = href.replace("view.html", "viewXml.html")
        return f"{self.main_address}{href}"

    def run(self, page_url: str):
        request = CustomRequest()
        response = request.get(page_url)

        soup = BeautifulSoup(response.text, 'html.parser')

        all_tags = soup.find_all(name="a", href=self.pattern)
        converted_ult_list = [self._convert_url(item) for item in all_tags]

        for item in converted_ult_list:
            LinkTask().delay(item)
        return True


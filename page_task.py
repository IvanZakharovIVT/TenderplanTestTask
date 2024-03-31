import re

from bs4 import BeautifulSoup, Tag
from celery import Celery, Task

from custom_request import CustomRequest


class PageTask(Task):
    name = 'parent_task'
    main_address = "https://zakupki.gov.ru"
    pattern = re.compile(r'/epz/.+printForm/view.html.+regNumber=\d+')

    def _convert_url(self, inner_url: Tag) -> str:
        href = inner_url.attrs['href']
        href = href.replace("view.html", "viewXml.html")
        return f"{self.main_address}{href}"

    def run(self, page_url: str, request: CustomRequest):
        response = request.get(page_url)

        soup = BeautifulSoup(response.text, 'html.parser')

        all_tags = soup.find_all(name="a", href=self.pattern)
        converted_ult_list = [self.convert_url(item) for item in all_tags]

        for item in converted_ult_list:
            pass
        # Execute subtask 1
        # result1 = SubTask1().delay(x, y)

        # Execute subtask 2
        # result2 = SubTask2().delay(x, y)
        #
        # # Wait for subtasks to complete and retrieve results
        # result1_value = result1.get()
        # result2_value = result2.get()
        #
        # # Perform some operation with subtask results
        # return result1_value + result2_value
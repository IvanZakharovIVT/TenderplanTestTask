import re

import xmltodict
from bs4 import BeautifulSoup, Tag
from celery import Celery, Task

from custom_request import CustomRequest


class LinkTask(Task):
    name = 'link_task'

    def run(self, link_url: str, request: CustomRequest):
        response = request.get(link_url)
        btf = xmltodict.parse(response.text)
        publishDTInEIS = None
        level1 = btf.get('ns7:epNotificationEZT2020')
        if level1:
            level2 = level1.get('commonInfo')
            if level2:
                publishDTInEIS = level2.get('publishDTInEIS', None)
        print(f"publishDTInEIS: {publishDTInEIS}")
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

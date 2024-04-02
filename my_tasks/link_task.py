import xmltodict
from celery import Task

from custom_request import CustomRequest


class LinkTask(Task):
    name = 'link_task'

    def run(self, link_url: str):
        request = CustomRequest()
        response = request.get(link_url)
        btf = xmltodict.parse(response.text)
        publishDTInEIS = None
        level1 = btf.get('ns7:epNotificationEZT2020')
        if level1:
            level2 = level1.get('commonInfo')
            if level2:
                publishDTInEIS = level2.get('publishDTInEIS', None)
        print(f"publishDTInEIS: {publishDTInEIS}")
        return True

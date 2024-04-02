import re

MAIN_ADDRESS = "https://zakupki.gov.ru"
SEARCH_ADDRESS = "/epz/order/extendedsearch/results.html"
PAGINATOR_SUFFIX = "?fz44=on&pageNumber="

SEARCH_PATTERN = re.compile(r'/epz/.+printForm/view.html.+regNumber=\d+')

REDIS_HOST = 'redis://localhost:6379/0'

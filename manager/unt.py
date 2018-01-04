from bs4 import BeautifulSoup
from helper.unt.category import Category
import urllib


def scrape():
    initial_url = 'https://digital.library.unt.edu/search/?q=&t=fulltext&sort=added_d&fq=dc_type%3A'

    for cat in Category:
        url = initial_url + cat.value
        print(url)

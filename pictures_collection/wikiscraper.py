import requests
from bs4 import BeautifulSoup
import urllib.request
from urllib.error import HTTPError
import contextlib


class PeanutsWikiScraper:
    def __init__(self):
        self.url = "https://peanuts.fandom.com/wiki"

    def find_major_characters(self):
        url_source = f"{self.url}/List_of_Peanuts_characters"
        source = requests.get(url_source).text
        soup = BeautifulSoup(source, 'lxml')
        soup.prettify()
        results = soup.find('div', id='mw-content-text')
        major_characters = []
        for result in results.find_all('a')[:15]:
            try:
                major_characters.append(result['title'])
            except KeyError:
                pass
        return major_characters

    def get_image_link(self, page_name):
        url_source = f"{self.url}/{page_name}"
        source = requests.get(url_source).text
        soup = BeautifulSoup(source, 'lxml')
        image = soup.find('div', class_='wds-tab__content')
        try:
            return image.find('img')['src']
        except AttributeError:
            pass

    def get_image(self, page_name, directory):
        image_link = self.get_image_link(page_name)
        if image_link is not None:
            with contextlib.suppress(HTTPError):
                filename = f'{directory}/{page_name}.png'
                opener = urllib.request.URLopener()
                opener.addheader('User-Agent', 'whatever')
                opener.retrieve(image_link, filename)

    def get_all_images(self, directory):
        for page in self.find_major_characters():
            self.get_image(page, directory)

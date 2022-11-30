import requests
from bs4 import BeautifulSoup
import urllib.request
from urllib.error import HTTPError
import contextlib


class Scraper:
    def __init__(self):
        self.url_stardewvalleywiki = 'https://stardewvalleywiki.com'

    def find_all_villagers(self):
        url_source = f"{self.url_stardewvalleywiki}/Villagers"
        source = requests.get(url_source).text
        soup = BeautifulSoup(source, 'lxml')
        all_results = soup.find_all('li', class_='gallerybox')
        return [result.find('a')['href'].lstrip('/')
                for result in all_results]

    def scrape_stardewvalley_page(self, page_name):
        url_source = f"{self.url_stardewvalleywiki}/{page_name}"
        source = requests.get(url_source).text
        soup = BeautifulSoup(source, 'lxml')
        image = soup.find('div', class_='floatnone')
        return image.find('img')['src']

    def get_image(self, page_name, directory):
        image_link = self.scrape_stardewvalley_page(page_name)
        url = f"{self.url_stardewvalleywiki}{image_link}"

        with contextlib.suppress(HTTPError):
            filename = f'{directory}/{page_name}.png'
            opener = urllib.request.URLopener()
            opener.addheader('User-Agent', 'whatever')
            opener.retrieve(url, filename)

    def get_all_images(self, directory):
        for page in self.find_all_villagers():
            self.get_image(page, directory)

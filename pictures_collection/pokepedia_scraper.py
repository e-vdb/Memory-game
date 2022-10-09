import requests
from bs4 import BeautifulSoup
import urllib.request
from urllib.error import HTTPError
import contextlib


class Scraper:
    def __init__(self):
        self.url_pokepedia = 'https://www.pokepedia.fr'
        self.url_first_gen = "https://www.pokepedia.fr/Liste_des_Pok%C3%A9mon_de_la_premi%C3%A8re_g%C3%A9n%C3%A9ration"  # noqa: E501
        self.all_pokemon = self.get_all_pokemon()

    def get_all_pokemon(self):
        source = requests.get(self.url_first_gen).text
        soup = BeautifulSoup(source, 'lxml')
        results = soup.find('table', class_='tableaustandard')
        results.prettify()
        all_pkm = results.find_all('td')
        all_pkm_names = []
        for item in all_pkm:
            try:
                pkm = item['id']
                all_pkm_names.append(pkm)
            except KeyError:
                pass
        return all_pkm_names

    def scrape_pokemon_page(self, pokemon_name):
        url_source = f"{self.url_pokepedia}/{pokemon_name}"
        print(url_source)
        source = requests.get(url_source).text
        soup = BeautifulSoup(source, 'lxml')
        results = soup.find('table', class_='tableaustandard')
        return results.find('img')['src']

    def get_image_pokemon(self, pokemon_name, directory):
        image_link = self.scrape_pokemon_page(pokemon_name)
        with contextlib.suppress(HTTPError):
            filename = f'{directory}/{pokemon_name}.png'
            urllib.request.urlretrieve(
                url=f"{self.url_pokepedia}{image_link}",
                filename=filename
            )

    def get_all_images(self, directory):
        for pokemon in self.all_pokemon:
            self.get_image_pokemon(pokemon, directory)

from pictures_collection.pokepedia_scraper import Scraper

data_dir = 'images_collection/Pokemon'
pkm_scraper = Scraper()
pkm_scraper.get_all_images(directory=data_dir)

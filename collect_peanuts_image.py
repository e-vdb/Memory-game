from pictures_collection.wikiscraper import PeanutsWikiScraper
from os import makedirs

output_dir = 'images_collection/Peanuts'
makedirs(output_dir, exist_ok=True)

scraper = PeanutsWikiScraper()
scraper.get_all_images(directory=output_dir)

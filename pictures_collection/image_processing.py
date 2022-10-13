from PIL import Image
from typing import List
from os import listdir


class ImageProcessor:
    """ Class to format images for MemoryGame """
    def __init__(self):
        pass

    def read_image(self, path):
        with Image.open(path) as img:
            img.load()
        return img

    @staticmethod
    def find_all_images_files_in_directory(
            directory: str,
            extension: str = 'png') -> List[str]:
        return [file
                for file in listdir(directory)
                if file.endswith(extension)]

    @staticmethod
    def expand_to_square(pil_img, background_color=(200, 54, 54, 0)):
        width, height = pil_img.size
        if width == height:
            return pil_img
        elif width > height:
            result = Image.new(pil_img.mode, (width, width), background_color)
            result.paste(pil_img, (0, (width - height) // 2))
            return result
        else:
            result = Image.new(
                pil_img.mode,
                (height, height),
                background_color
            )
            result.paste(pil_img, ((height - width) // 2, 0))
            return result

    @staticmethod
    def resize_image(pil_img, output_size):
        return pil_img.resize(output_size)

    def save_image(self, pil_img, output_path):
        pil_img.save(output_path)

    def process_image(self, filepath, output_size, output_path):
        pil_img = self.read_image(filepath)
        pil_img_processed = self.expand_to_square(pil_img)
        pil_img_processed = self.resize_image(pil_img_processed, output_size)
        self.save_image(pil_img_processed, output_path)

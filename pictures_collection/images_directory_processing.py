from pictures_collection.image_processing import ImageProcessor
from os import makedirs


def create_formatted_gif_images_from_png(data_dir, output_dir):
    makedirs(output_dir, exist_ok=True)
    img_processor = ImageProcessor()
    all_images = img_processor.find_all_images_files_in_directory(data_dir)
    all_images.sort()

    for count, image in enumerate(all_images):
        img_processor.process_image(
            filepath=f'{data_dir}/{image}',
            output_size=(102, 102),
            output_path=f'{output_dir}/carte-{count}.gif')

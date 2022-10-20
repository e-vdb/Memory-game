from pictures_collection.image_processing import ImageProcessor
from os import makedirs, getcwd, rename
from os.path import join
from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser()
parser.add_argument("input_folder", type=Path)

args = parser.parse_args()

if args.input_folder.exists():
    input_dir = args.input_folder
    theme = str(args.input_folder).split("/")[-1]
    output_dir = join('Images', theme)
    makedirs(output_dir, exist_ok=True)

    processor = ImageProcessor()
    all_images = processor.find_all_images_files_in_directory(input_dir)
    all_images.sort()

    for count, image in enumerate(all_images):
        processor.process_image(
            filepath=f'{input_dir}/{image}',
            output_size=(150, 150),
            output_path=f'{output_dir}/carte-{count}.gif')

    last_image = f'carte-{len(all_images) -1}.gif'
    filepath = join(getcwd(), output_dir, last_image)
    rename(filepath, join(getcwd(), output_dir, 'blankCard.gif'))
    print(f'All images processed and saved in {output_dir}.')

else:
    print(f'Folder {args.input_folder} does not exist.')

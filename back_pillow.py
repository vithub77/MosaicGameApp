from PIL import Image
import random

from center_img import ImageDATA


def create_img_mosaic():
    dt_img = ImageDATA()
    dt_img.data_dict['extra_name'] = chr(random.choice(range(97, 120)))
    path_img = dt_img.get_path()
    image = Image.open(path_img)
    dt_img.set_size(image.size)
    grid_size = dt_img.get_grid_size()

    width_img, height_img = dt_img.get_image_size()
    image = image.resize((width_img, height_img))
    image.save(path_img)
    image = Image.open(path_img)

    cell_width = width_img // grid_size[0]
    cell_height = height_img // grid_size[1]
    value_list = []
    exn = dt_img.data_dict['extra_name']

    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            box_ = (j * cell_width, i * cell_height, (j + 1) * cell_width, (i + 1) * cell_height)
            grid_image = image.crop(box_)
            grid_image.save(f'./assets/{dt_img.data_dict["name_dir"]}/{exn}{i}-{j}.png')
            value_list.append(f'{i}-{j}')
    return value_list

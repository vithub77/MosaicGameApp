import numpy as np
import os

from center_img import ImageDATA
from back_pillow import create_img_mosaic


class GamePlay:
    _imd = ImageDATA()
    valid_value: np.array
    game_fild: np.array

    def __init__(self):
        self.valid_value = np.array(create_img_mosaic()).reshape(*self._imd.get_grid_size())
        self.row, self.col = self._imd.get_grid_size()

    def __str__(self):
        return f'{self.valid_value}'

    def shuffled(self):
        sh_matrix = np.copy(self.valid_value)
        np.random.shuffle(sh_matrix)
        for row in sh_matrix:
            np.random.shuffle(row)
        self.game_fild = sh_matrix

    def set_img_mosaic(self):
        _res = create_img_mosaic()
        self.valid_value = np.array(_res).reshape(*self._imd.get_grid_size())
        self.row, self.col = self._imd.get_grid_size()

    def change_position(self, f, t):
        index_from = np.where(self.game_fild == f)
        index_to = np.where(self.game_fild == t)
        self.game_fild[index_from[0], index_from[1]] = t
        self.game_fild[index_to[0], index_to[1]] = f
        return np.array_equal(self.game_fild, self.valid_value)

    def clear_folder(self):
        name_dir = self._imd.data_dict["name_dir"]
        r = os.listdir(f'./assets/{name_dir}')
        for name in r:
            if name.split('.')[0] == name_dir:
                continue
            else:
                os.remove(f'./assets/{name_dir}/{name}')


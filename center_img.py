# MONO-STATE CLASS
class ImageDATA:
    data_dict = {
        'name_dir': '0',
        'name_img': '0',
        'extra_name': '',
        'col_items_w': 2,
        'col_items_h': 2,
        '_w': 1,
        '_h': 1
    }

    def __init__(self):
        self.__dict__ = self.data_dict

    def get_grid_size(self):
        return self.data_dict['col_items_w'], self.data_dict['col_items_h']

    def get_aspect_ratio(self):
        return self.data_dict['_w'] / self.data_dict['_h']

    def get_path(self):
        # f"./assets/{self.data_dict['name_dir']}/{self.data_dict['name_img']}.png"
        return f"./assets/{self.data_dict['name_dir']}/{self.data_dict['name_img']}.png"

    def set_size(self, size):
        self.data_dict['_w'] = size[0]
        self.data_dict['_h'] = size[1]

    def get_cell_size(self):
        _w, _h = self.get_image_size()
        return _w // self.data_dict['col_items_w'], _h // self.data_dict['col_items_h']

    def get_image_size(self):
        return 680, int(680 // self.get_aspect_ratio())

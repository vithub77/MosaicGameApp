import flet as ft
import shutil
from backend import GamePlay
from main_page import MainViewPage
from center_img import ImageDATA


class MosaicGameApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.mvp = MainViewPage(page)
        self.gp = GamePlay()
        self.dt_img = ImageDATA()
        self.file_picker = self.create_file_picker()
        self.setup_ui()

    def setup_ui(self):
        self.page.add(self.create_top_menu(), self.create_center_view(True), self.create_bottom_images())

    def create_top_menu(self):
        but_download = ft.ElevatedButton('Choose Image', bgcolor=ft.colors.CYAN, icon="add", color=ft.colors.WHITE,
                                         on_click=lambda _: self.file_picker.pick_files(allow_multiple=False),
                                         expand=True)
        t = ft.Text(value='Amount of elements: W x H', theme_style=ft.TextThemeStyle.BODY_LARGE,
                    offset=(0.05, 0),
                    color='white')
        count_items = [ft.PopupMenuItem(text='2x2', on_click=self.choose_items),
                       ft.PopupMenuItem(text='3x3', on_click=self.choose_items),
                       ft.PopupMenuItem(text='4x4', on_click=self.choose_items)]
        pb_w = ft.PopupMenuButton(items=count_items)

        contain_top_t = ft.Container(bgcolor=ft.colors.CYAN_200, border_radius=9,
                                     content=ft.Row([t, pb_w]))
        but_start = ft.ElevatedButton('START GAME', bgcolor=ft.colors.CYAN, icon=ft.icons.START,
                                      color=ft.colors.WHITE, expand=True, on_click=self.start_game)

        top_menu = ft.Row(controls=[ft.Row(height=100), but_download, contain_top_t, but_start], offset=(-0.01, -0.1))
        return top_menu

    def create_center_view(self, b: bool):
        if b:
            val = self.gp.valid_value
        else:
            val = self.gp.game_fild
        exn = self.dt_img.data_dict['extra_name']
        cell_x, cell_y = self.dt_img.get_cell_size()

        center = ft.Column(
            spacing=0, alignment=ft.alignment.center,
            controls=[
                ft.Row(
                    width=720,
                    alignment=ft.alignment.center,
                    spacing=0,
                    controls=[ft.Draggable(
                        group='cell',
                        content=ft.DragTarget(group='cell',
                                              on_accept=self.accept_move,
                                              content=ft.Container(
                                                  width=cell_x,
                                                  height=cell_y,
                                                  margin=1,
                                                  padding=1,
                                                  border_radius=1,
                                                  image_src=f'{self.dt_img.data_dict["name_dir"]}/{exn}{val[_][j]}.png'))
                    ) for j in
                        range(
                            self.dt_img.data_dict['col_items_w'])])
                for _ in range(self.dt_img.data_dict['col_items_h'])])

        return center

    def create_bottom_images(self):
        contain_list = []
        for i in range(0, 5):
            contain_list.append(
                ft.Container(width=200, height=200,
                             margin=3,
                             border=ft.border.only(),
                             ink=True,
                             on_click=self.change_img,
                             key=f'{i}',
                             content=ft.Image(src=f"{i}/{i}.png",
                                              width=200,
                                              height=200,
                                              fit=ft.ImageFit.CONTAIN,
                                              repeat=ft.ImageRepeat.NO_REPEAT,
                                              border_radius=ft.border_radius.all(10))
                             ))
        images = ft.Row(controls=contain_list, scroll=ft.ScrollMode.ALWAYS, spacing=5)
        container_view_img = ft.Container(width=720, clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                          bgcolor=ft.colors.CYAN_100,
                                          border_radius=10, content=images)
        return container_view_img

    def create_file_picker(self):
        file_picker = ft.FilePicker(on_result=self.on_download_result)
        self.page.overlay.append(file_picker)
        return file_picker

    def on_download_result(self, e: ft.FilePickerResultEvent):
        try:
            shutil.copy(e.files[0].path, f'assets/user/user.png')

            self.dt_img.data_dict['name_dir'] = self.dt_img.data_dict['name_img'] = 'user'
            self.gp.set_img_mosaic()
            self.update_center(True)
        except TypeError:
            pass

    def choose_items(self, e):
        self.gp.clear_folder()
        self.page.update()
        if e.control.text == '3x3':
            self.dt_img.data_dict['col_items_w'], self.dt_img.data_dict['col_items_h'] = 3, 3
        elif e.control.text == '4x4':
            self.dt_img.data_dict['col_items_w'], self.dt_img.data_dict['col_items_h'] = 4, 4
        else:
            self.dt_img.data_dict['col_items_w'], self.dt_img.data_dict['col_items_h'] = 2, 2
        self.gp.set_img_mosaic()
        self.update_center(True)

    def change_img(self, e):
        self.gp.clear_folder()
        self.dt_img.data_dict['name_dir'] = self.dt_img.data_dict['name_img'] = e.control.key
        self.gp.set_img_mosaic()
        self.update_center(True)

    def accept_move(self, e):
        src_from = self.page.get_control(e.src_id)
        scr_to = self.page.get_control(e.target)

        f = str(src_from.content.content.image_src).split('/')[-1].split('.')[0][1:]
        t = str(scr_to.content.image_src).split('/')[-1].split('.')[0][1:]

        res = self.gp.change_position(f=f, t=t)
        if res:
            self.text_victory()

        else:
            self.update_center(False)

    def start_game(self, e):
        self.gp.shuffled()
        self.update_center(False)

    def text_victory(self):
        self.page.controls.pop(1)
        p = self.dt_img.get_path().split('/')[2:]
        path = '/'.join(p)
        ctr = ft.Stack(controls=[ft.Image(src=path), ft.Container(width=720,
                                                                  height=720 // self.dt_img.get_aspect_ratio(),
                                                                  alignment=ft.alignment.center,
                                                                  content=ft.Text('COMPLETED',
                                                                                  color=ft.colors.BLUE_600,
                                                                                  # bgcolor=ft.colors.BLUE_600,
                                                                                  size=70,
                                                                                  weight=ft.FontWeight.W_100,
                                                                                  opacity=0.7))])
        self.page.controls.insert(1, ctr)
        self.page.update()

    def update_center(self, b: bool):
        self.page.controls.pop(1)
        self.page.controls.insert(1, self.create_center_view(b))
        self.page.update()


def main_gui(page: ft.Page):
    MosaicGameApp(page)


if __name__ == "__main__":
    ft.app(target=main_gui, upload_dir='./assets/')

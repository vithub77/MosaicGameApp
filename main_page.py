import flet as ft


class MainViewPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = 'Game "Collect Image"'
        self.page.window_width = 720
        self.page.window_height = 860
        self.page.bgcolor = ft.colors.BLUE_GREY_100
        self.page.theme = ft.Theme(
            scrollbar_theme=ft.ScrollbarTheme(
                track_visibility=False,
                thumb_visibility=True,
                thumb_color={
                    ft.MaterialState.HOVERED: ft.colors.GREY_500,
                    ft.MaterialState.DEFAULT: ft.colors.GREY_400,
                },
                thickness=10,
                radius=5,
                main_axis_margin=2,
                cross_axis_margin=5,
            )
        )
        self.page.scroll = True

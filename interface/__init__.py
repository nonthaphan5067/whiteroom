import os
import dearpygui.dearpygui as dpg
from tkinter import filedialog
from . import _theme

VIEWPORT_MIN_HEIGHT = 600
VIEWPORT_MIN_WIDTH = 800


def show_interface():
    dpg.create_context()
    dpg.create_viewport(
        title="WhiteRoom", min_height=VIEWPORT_MIN_HEIGHT, min_width=VIEWPORT_MIN_WIDTH
    )
    dpg.set_global_font_scale(1.25)

    file_path: str | None = None

    with dpg.window(tag="window-home"):

        def select_file():
            initial_dir = os.path.expanduser("~/Pictures")
            file_path = filedialog.askopenfilename(
                initialdir=initial_dir, title="Select a File"
            )
            width, height, channels, data = dpg.load_image(file_path)
            dpg.add_static_texture(
                width=width, height=height, default_value=data, tag="texture_tag"
            )
            dpg.set_primary_window("window-home", False)
            dpg.hide_item("window-home")
            dpg.show_item("window-image")

        dpg.add_button(label="Select image file.", callback=select_file)

    with dpg.window(tag="window-main"):

        def print_me(sender):
            print(f"Menu Item: {sender}")
            dpg.set_primary_window("Main", False)

        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Save", tag="menu_save_file", callback=print_me)
                dpg.add_menu_item(
                    label="Save As", tag="menu_save_file_as", callback=print_me
                )

                with dpg.menu(label="Settings"):
                    dpg.add_menu_item(label="Setting 1", callback=print_me, check=True)
                    dpg.add_menu_item(label="Setting 2", callback=print_me)

            dpg.add_menu_item(label="Help", callback=print_me)

            with dpg.menu(label="Widget Items"):
                dpg.add_checkbox(label="Pick Me", callback=print_me)
                dpg.add_button(label="Press Me", callback=print_me)
                dpg.add_color_picker(label="Color Me", callback=print_me)

        # _theme.apply_theme()
        dpg.add_text("Hello world")
        # dpg.add_button(label="Save", callback=save_callback)
        dpg.add_input_text(label="string")
        dpg.add_slider_float(label="float")

    with dpg.window(tag="window-image", show=False):
        # dpg.add_image("texture_tag", show=file_path != None)
        dpg.add_text(label="as")

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("window-home", True)

    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()

    dpg.start_dearpygui()
    dpg.destroy_context()

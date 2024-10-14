import os
import cv2
import numpy as np
import dearpygui.dearpygui as dpg
from tkinter import filedialog
from ._window import (
    WINDOW_TAG_HOME,
    WINDOW_TAG_PROCESSOR,
    WINDOW_TAG_IMAGE,
    WINDOW_TAG_ORIGINAL_IMAGE,
)

VIEWPORT_MIN_HEIGHT = 600
VIEWPORT_MIN_WIDTH = 800


# Initialize globals
original_image = None
modified_image = None


def show():
    dpg.create_context()
    dpg.create_viewport(
        title="WhiteRoom",
        min_height=VIEWPORT_MIN_HEIGHT,
        min_width=VIEWPORT_MIN_WIDTH,
    )

    texture_registry = dpg.add_texture_registry(tag="image-registry", show=False)

    def select_file():
        global original_image, modified_image

        # initial_dir = os.path.expanduser("~/Pictures")
        # file_path = filedialog.askopenfilename(
        #     initialdir=initial_dir,
        #     title="Select an Image",
        #     filetypes=[
        #         ("Image file", ["*.png", "*.jpg", "*.jpeg"]),
        #     ],
        # )

        # if len(file_path) <= 0:
        #     print("Select file cancel.")
        #     return

        file_path = (
            "C:/Users/taoka/Pictures/Screenshots/Screenshot 2024-04-29 163941.png"
        )

        print("Load image from path {}.".format(file_path))

        original_image = cv2.imread(file_path)
        modified_image = original_image.copy()

        img_rgb = cv2.cvtColor(modified_image, cv2.COLOR_BGR2RGB)

        img_data = np.flip(img_rgb, axis=0)
        width, height, _ = img_data.shape

        # data = np.flip(img_data.data, 2)
        data = img_data.ravel()
        data = np.asarray(data, dtype="f")
        texture_data = np.true_divide(data, 255.0)

        print(texture_data)
        # return
        print("Add image to registry ({}).".format(texture_registry))
        dpg.add_dynamic_texture(
            width=width,
            height=height,
            default_value=texture_data,
            tag="texture_tag",
            parent=texture_registry,
        )

        dpg.hide_item(WINDOW_TAG_HOME)
        dpg.show_item(WINDOW_TAG_IMAGE)
        dpg.add_image("texture_tag", parent=WINDOW_TAG_IMAGE)
        dpg.add_image("texture_tag", parent=WINDOW_TAG_ORIGINAL_IMAGE)

        _, tail = os.path.split(file_path)
        dpg.set_item_label(item=WINDOW_TAG_IMAGE, label=tail)
        dpg.set_item_label(item=WINDOW_TAG_ORIGINAL_IMAGE, label=tail)

        dpg.show_item(WINDOW_TAG_PROCESSOR)
        dpg.set_primary_window(WINDOW_TAG_PROCESSOR, True)

    def update_texture():
        global modified_image
        img_rgb = cv2.cvtColor(modified_image, cv2.COLOR_BGR2RGB)
        img_data = np.flip(img_rgb, axis=0)
        width, height = img_data.shape
        dpg.set_item_width("image_texture_tag", width)
        dpg.set_item_height("image_texture_tag", height)
        dpg.set_value("image_texture_tag", img_data)

    with dpg.window(tag=WINDOW_TAG_HOME, no_close=True):
        dpg.add_button(
            label="Select image file.",
            pos=(500, 500),
            callback=select_file,
            height=30,
        )

    dpg.add_window(
        tag=WINDOW_TAG_IMAGE,
        show=False,
        no_scrollbar=True,
        no_close=True,
        no_scroll_with_mouse=True,
        min_size=(500, 500),
        height=500,
        width=500,
    )

    dpg.add_window(
        tag=WINDOW_TAG_ORIGINAL_IMAGE,
        show=False,
        no_scrollbar=True,
        no_close=True,
        no_scroll_with_mouse=True,
        min_size=(500, 500),
        height=500,
        width=500,
    )

    def on_change_brightness(sender, brightness):
        print(sender, brightness)

    def on_change_contrast(sender, contrast):
        print(sender, contrast)

    with dpg.window(
        tag=WINDOW_TAG_PROCESSOR,
        show=False,
        pos=(0, 0),
        no_close=True,
        no_resize=True,
        no_scrollbar=True,
    ):
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Open file")
                dpg.add_menu_item(label="Save file")
                dpg.add_menu_item(label="Save file as")
                dpg.add_menu_item(label="Close file")

            with dpg.menu(label="Window"):
                dpg.add_menu_item(label="Reset window")

            dpg.add_menu_item(label="Help")

        with dpg.tab_bar():
            with dpg.tab(label="Filtering"):
                with dpg.group(horizontal=True):
                    with dpg.child_window(width=300):
                        # with dpg.group(horizontal=True):
                        #     dpg.add_checkbox()
                        #     dpg.add_text("Histogram Equalization")

                        # dpg.add_separator()

                        with dpg.group(horizontal=True):
                            dpg.add_checkbox()
                            dpg.add_text("Brightness and Contrast")
                        dpg.add_text("Brightness")
                        dpg.add_slider_int(
                            default_value=0,
                            min_value=-100,
                            max_value=100,
                            width=-1,
                            tag="brightnessSlider",
                            callback=on_change_brightness,
                        )
                        dpg.add_text("Contrast")
                        dpg.add_slider_float(
                            default_value=1.0,
                            min_value=0.0,
                            max_value=3.0,
                            width=-1,
                            tag="contrastSlider",
                            callback=on_change_contrast,
                        )
                        dpg.add_separator()

                    with dpg.child_window(tag="FilteringParent"):
                        with dpg.group(horizontal=True):

                            def on_show_original_image(sender, checked):
                                if checked:
                                    dpg.show_item(WINDOW_TAG_ORIGINAL_IMAGE)
                                else:
                                    dpg.hide_item(WINDOW_TAG_ORIGINAL_IMAGE)

                            dpg.add_checkbox(callback=on_show_original_image)
                            dpg.add_text("Show original")

    def on_image_window_resize():
        window_width = dpg.get_item_width(WINDOW_TAG_IMAGE)
        # window_height = dpg.get_item_height(WINDOW_TAG_IMAGE)

        dpg.set_item_width("texture_tag", window_width)
        # dpg.set_item_height("texture_tag", window_height)
        print(window_width)

    with dpg.item_handler_registry(tag="handler-window"):
        dpg.add_item_resize_handler(callback=on_image_window_resize)

    dpg.bind_item_handler_registry(WINDOW_TAG_IMAGE, "handler-window")

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window(WINDOW_TAG_HOME, True)

    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()

    dpg.start_dearpygui()
    dpg.destroy_context()

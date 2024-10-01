import dearpygui.dearpygui as dpg

MIN_VIEWPORT_HEIGHT = 600
MIN_VIEWPORT_WIDTH = 800

viewport_height = 0
viewport_width = 0


def show_viewport():
    def save_callback():
        print("Save Clicked")

    with dpg.window(
        label="Example Window",
        no_collapse=True,
        collapsed=False,
        no_move=True,
        pos=(0, 0),
        no_close=True,
        height=viewport_height,
    ):
        with dpg.menu_bar(label="Menu"):
            dpg.add_text("This menu is just for show!")
            dpg.add_menu_item(label="New")
            dpg.add_menu_item(label="Open")

        dpg.add_text("Hello world")
        dpg.add_button(label="Save", callback=save_callback)
        dpg.add_input_text(label="string")
        dpg.add_slider_float(label="float")


if __name__ == "__main__":
    dpg.create_context()
    dpg.create_viewport(
        title="WhiteRoom", min_height=MIN_VIEWPORT_HEIGHT, min_width=MIN_VIEWPORT_WIDTH
    )

    show_viewport()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()

    while dpg.is_dearpygui_running():
        viewport_height = dpg.get_viewport_height()
        viewport_width = dpg.get_viewport_height()

        print("this will run every frame")
        dpg.render_dearpygui_frame()

    dpg.destroy_context()

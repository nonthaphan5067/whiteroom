import dearpygui._dearpygui as dpg
from PIL import ImageGrab

with dpg.add_window("Main Window"):
    dpg.set_main_window_size(800, 800)
    dpg.set_main_window_title("Pixel selector")

    dpg.add_drawing("drawing", width=400, height=350)

    img = ImageGrab.grab(bbox=[0, 0, 100, 100])

    dpg_image = []
    for i in range(0, img.height):
        for j in range(0, img.width):
            pixel = img.getpixel((j, i))
            dpg_image.append(pixel[0])
            dpg_image.append(pixel[1])
            dpg_image.append(pixel[2])
            dpg_image.append(255)

    # something like this would be great
    dpg.add_texture("texture id", dpg_image, img.width, img.height)
    dpg.draw_image("drawing", "texture id", [0, 0], [100, 100])

dpg.start_dearpygui()

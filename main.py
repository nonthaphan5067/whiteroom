import os
import cv2
from tkinter import filedialog
from matplotlib import pyplot as plt

contrast = 0
brightness = 0
mosaic = 0

if __name__ == "__main__":
    print("type (help) for show help menu.")

    plt.ion()
    plt.axis("off")

    original_image = None
    edit_mode = False
    image = None
    image_buf = image

    def set_mosaic(v):
        global mosaic
        mosaic = v

    def set_brightness(v):
        global brightness
        brightness = v

    def set_contrast(v):
        global contrast
        contrast = v

    def get_filename(file_path: str):
        return os.path.split(file_path)[1]

    def update_image(contrast=None, brightness=None, mosaic=None):
        global original_image, image
        buf = image
        if original_image is None:
            return

        if image is None:
            return

        if contrast is not None and contrast > 0:
            f = 131 * (contrast + 127) / (127 * (131 - contrast))
            alpha_c = f
            gamma_c = 127 * (1 - f)

            buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

        if brightness is not None and brightness > 0:
            hsv = cv2.cvtColor(buf, code=cv2.COLOR_RGB2HSV)
            h, s, v = cv2.split(hsv)

            lim = 255 - brightness
            v[v > lim] = 255
            v[v <= lim] += brightness

            buf = cv2.cvtColor(cv2.merge((h, s, v)), code=cv2.COLOR_HSV2RGB)

        if mosaic is not None and mosaic > 0:
            size = buf.shape
            level = mosaic
            h = int(size[0] / level)
            w = int(size[1] / level)
            buf = cv2.resize(buf, (w, h), interpolation=cv2.INTER_LINEAR)
            buf = cv2.resize(buf, (size[1], size[0]), interpolation=cv2.INTER_NEAREST)

        plt.imshow(buf)

        return buf

    def reset_image():
        image_buf = image
        plt.imshow(image_buf)

    def contrast_mode():
        global image, image_buf, contrast, brightness, mosaic
        local_contrast = contrast
        while True:
            contrast_level = str(input("select contrast level 0-255: "))

            if contrast_level in ["help", "?"]:
                print("- save\t\tfor save value")
                continue

            if contrast_level in ["exit", "cancel"]:
                break

            if contrast_level in ["confirm", "save"]:
                set_contrast(local_contrast)
                break

            if contrast_level == "reset":
                continue

            if not contrast_level.isdecimal():
                print("contrast level invalid!")
                continue

            contrast_level = abs(int(contrast_level))
            if contrast_level > 255:
                print("contrast level invalid!")
                continue

            local_contrast = contrast_level
            print("set contrast level to", contrast_level)
            update_image(brightness=brightness, contrast=local_contrast, mosaic=mosaic)

    def brightness_mode():
        global image, image_buf, mosaic, contrast, brightness
        local_brightness = brightness
        while True:
            brightness_level = str(input("select brightness level 0-255: "))
            if brightness_level in ["help", "?"]:
                print("- save\t\tfor save value")
                continue

            if brightness_level in ["exit", "cancel"]:
                break

            if brightness_level in ["confirm", "save"]:
                # brightness = local_brightness
                set_brightness(local_brightness)
                break

            if brightness_level == "reset":
                local_brightness = brightness
                continue

            if not brightness_level.isdecimal():
                print("brightness level invalid!")
                continue

            brightness_level = abs(int(brightness_level))
            if brightness_level > 255:
                print("brightness level invalid!")
                continue

            local_brightness = brightness_level
            print("set brightness level to", brightness_level)
            update_image(brightness=local_brightness, contrast=contrast, mosaic=mosaic)

    def mosaic_mode():
        global image, image_buf, mosaic, contrast, brightness
        local_mosaic = mosaic
        while True:
            mosaic_level = str(input("select mosaic level 0-255: "))
            if mosaic_level in ["help", "?"]:
                print("- save\t\tfor save value")
                continue

            if mosaic_level in ["exit", "cancel"]:
                break

            if mosaic_level in ["confirm", "save"]:
                set_mosaic(local_mosaic)
                break

            if mosaic_level == "reset":
                set_mosaic(0)
                continue

            if not mosaic_level.isdecimal():
                print("mosaic level invalid!")
                continue

            mosaic_level = abs(int(mosaic_level))
            if mosaic_level > 255:
                print("mosaic level invalid!")
                continue

            print("set mosaic level to", mosaic_level)

            if mosaic_level <= 0:
                continue

            local_mosaic = mosaic_level
            update_image(brightness=brightness, contrast=contrast, mosaic=local_mosaic)

    while True:
        user_input = str(
            input(
                "> "
                if original_image is None
                else "({}){} > ".format(
                    get_filename(original_image), "(edit)" if edit_mode else ""
                )
            )
        )

        if user_input == "help":
            if edit_mode:
                print("- contrast,con,c\t\tfor edit contrast image.")
                print("- brightness,bright,b\t\tfor edit brightness image.")
                print("- mosaic,mos,m\t\tfor edit mosaic image.")
                continue

            if original_image is not None:
                print("- edit\tfor toggle edit mode.")
                print("- save\tfor save image file to disk.")
                continue

            print("- select,open\tfor select image file for edit.")
            continue

        if user_input == "exit":
            if original_image is None:
                exit()

            user_input = str(
                input(
                    "Do you want to save ({})? (N/y) > ".format(
                        get_filename(get_filename(original_image))
                    )
                )
            ).lower()
            if user_input in ["Y", "y", "yes", "true"]:
                file_path = filedialog.asksaveasfilename()
                if file_path is None:
                    continue

                print("Save file to ({})".format(file_path))
                cv2.imwrite(
                    file_path,
                    update_image(
                        contrast=contrast, brightness=brightness, mosaic=mosaic
                    ),
                )
                exit()
            else:
                exit()

        if user_input in ["select", "open"]:
            if original_image is not None:
                print("Image is currently select.")
                continue
            initial_dir = os.path.expanduser("~/Pictures")
            file_path = filedialog.askopenfilename(
                initialdir=initial_dir,
                title="Select an Image",
                filetypes=[
                    ("Image file", ["*.png", "*.jpg", "*.jpeg"]),
                ],
            )

            if len(file_path) <= 0:
                print("Select file cancel.")
                continue

            original_image = file_path

            image = cv2.imread(original_image)
            image = cv2.cvtColor(image, code=cv2.COLOR_BGR2RGB)

            plt.imshow(image)
            plt.show()

        if user_input == "edit":
            if original_image is None:
                print("Can't use edit mode, Please select file first!")
                continue

            edit_mode = not edit_mode

        if user_input == "save":
            file_path = filedialog.asksaveasfilename()
            if file_path == () or file_path is None:
                print("cancel save file.")
                continue

            print("Save file to ({})".format(file_path))
            img = update_image(contrast=contrast, brightness=brightness, mosaic=mosaic)
            cv2.imwrite(file_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

        if edit_mode:
            if user_input in ["contrast", "c", "con"]:
                contrast_mode()

            if user_input in ["brightness", "b", "bright"]:
                brightness_mode()

            if user_input in ["mosaic", "m", "mos"]:
                mosaic_mode()

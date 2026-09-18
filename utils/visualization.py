import cv2
from PIL import Image, ImageTk


def cv2_to_tk(image, max_width=350, max_height=350):
    if len(image.shape) == 2:
        rgb_image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    pil_image = Image.fromarray(rgb_image)
    pil_image.thumbnail((max_width, max_height))
    tk_image = ImageTk.PhotoImage(pil_image)
    return tk_image


def save_result_image(image, output_path):
    cv2.imwrite(output_path, image)

import os
from PIL import Image
from datetime import date

def is_image_file(filename):
    return any(filename.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png"])

def create_image_directories() -> str:
    today = date.today().strftime("%Y-%m-%d")
    image_directory = os.path.join(os.getcwd(), "static/images")
    today_image_directory = os.path.join(image_directory, today)

    if not os.path.exists(image_directory):
        os.makedirs(image_directory)
    if not os.path.exists(today_image_directory):
        os.makedirs(today_image_directory)

    return today_image_directory

def get_image_data():
    data = {}
    create_image_directories()
    image_directory = os.path.join(os.getcwd(), "static/images")
    for item in os.listdir(image_directory):
        path = os.path.join(image_directory, item)
        if os.path.isdir(path):
            data[item] = []
            for subitem in os.listdir(path):
                subitem_path = os.path.join(path, subitem)
                if os.path.isfile(subitem_path) and is_image_file(subitem):
                    data[item].append(subitem)
    return data
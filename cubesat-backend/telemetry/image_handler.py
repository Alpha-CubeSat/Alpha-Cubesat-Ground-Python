import os

import databases.image_database as img_db
import util.binary.hex_string as hex


def get_image_data(image_file):
    with open(image_file, 'rb') as image:
        bin_img = bytearray(image.read())
    return {
        'name': os.path.basename(image_file),
        'timestamp': os.path.getmtime(image_file),
        'base64': hex.bytes_to_b64(bin_img)
    }

def get_image_at(idx):
    return get_image_data(img_db.get_recent_images(idx + 1)[idx])

def get_image_by_name(name):
    return get_image_data(img_db.get_image_by_name(name))

def get_recent_image_names(n):
    return img_db.get_recent_images(n)

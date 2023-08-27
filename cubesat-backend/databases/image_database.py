import os
from os.path import exists

import config as cfg
import util.binary.hex_string as hex

# TODO: will not work if multiple images received
# list of all image fragment numbers received
fragment_list = []
# keeps track of various stats regarding the received image fragments
img_display_info = {'image_serial': 0, 'latest_fragment': 0, 'missing_fragments': [],
                    'fragment_count': '?/?', 'highest_fragment': 0}


def save_fragment(image_sn: int, fragment_number: int, binary_fragment_data: bytearray):
    """
    Saves an image fragment. Creates one if it doesn't exist using the following policy:
        - new file is created under the directory with the serial number of the image
        - the name of the file will be the fragment number with the .csfrag extension
    Example:
        - Fragment 7 of image 23 will be saved as '7.csfrag' under the directory named "23".
    :param image_sn: serial number of the image the fragment belongs to
    :param fragment_number: id number of the fragment
    :param binary_fragment_data: byte array containing the image fragment data
    """
    if not exists(cfg.image_root_dir):
        os.makedirs(cfg.image_root_dir)

    if not exists(f'{cfg.image_root_dir}/{image_sn}'):
        os.makedirs(f'{cfg.image_root_dir}/{image_sn}')

    with open(f'{cfg.image_root_dir}/{image_sn}/{fragment_number}.csfrag', 'wb') as frag_file:
        frag_file.write(binary_fragment_data)

    global img_display_info, fragment_list
    img_display_info['image_serial'] = image_sn
    img_display_info['latest_fragment'] = fragment_number
    img_display_info['missing_fragments'] = []
    fragment_list = []


def sort_files_numeric(files: list) -> list:
    """
    Sorts fragment files by name, stripping the extensions.
    They are numerically named, but '2.csfrag' comes before '10.csfrag'
    :param files: list of all image fragment files
    """
    return sorted(files, key=lambda x: int(os.path.basename(x).split('.')[0]))


def generate_missing_fragments(frag_list: list):
    """
    Finds the missing fragments and the highest fragment received for an image.
    Counts through all already-received fragments every time because fragments could be received in random order.
    :param frag_list: list of previously received fragments
    """
    max_frag = max(frag_list)
    img_display_info['missing_fragments'] = []
    img_display_info['highest_fragment'] = max_frag
    for x in range(max_frag):
        if frag_list.count(x) == 0:
            img_display_info['missing_fragments'].append(x)

def get_saved_fragments(image_sn: int) -> list:
    """
    Generates a list of the fragments received for a particular image as a list of numbers.
    """
    fragment_files = []
    for dir_path, _, file_names in os.walk(f'{cfg.image_root_dir}/{image_sn}'):
        for file in file_names:
            if '.csfrag' in file:
                fragment_files.append(os.path.join(dir_path, file))
    return fragment_files

def try_save_image(image_sn: int, total_fragments: int):
    """
    Tries to assemble an image out of fragments. If the total # of fragments currently received
    equals the total # of fragments, the completed image is saved to the directory 'img' as a
    jpeg file with the serial number as a name. \n
    Example: If image 23 is complete when this function is called, the completed image will
    be saved as '23.jpg' under 'img', and assembled out of the fragment files in the directory '23'
    :param image_sn: serial number of the image to be assembled
    :param total_fragments: the total # of fragments needed to assemble the image
    """
    # Get all currently received fragments
    fragment_map = {}
    for file in sort_files_numeric(get_saved_fragments(image_sn)):
        fragment_map[int(os.path.splitext(os.path.basename(file))[0])] = file

    global fragment_list
    fragment_list = list(fragment_map.keys())

    # Generate blank fragments if a fragment is missing and update counters
    generate_missing_fragments(fragment_list)
    img_display_info['fragment_count'] = f'{len(fragment_list)}/' + str(
        total_fragments) if total_fragments != 1 else '?'

    # Build final image with currently received fragments (filling in missing ones with blanks)
    if not exists(f'{cfg.image_root_dir}/img'):
        os.makedirs(f'{cfg.image_root_dir}/img')

    with open(f'{cfg.image_root_dir}/img/{image_sn}.jpg', 'wb') as image_file:
        for i in range(fragment_list[-1] + 1):
            if i in fragment_list:
                image_file.write(open(fragment_map[i], 'rb').read())
            else: # generate a blank 64 byte fragment if a fragment is missing
                print(f'fragment {i} missing')
                image_file.write(bytearray.fromhex('f'*128))


def get_img_display_info() -> dict:
    """Returns the contents of img_display_info"""
    return img_display_info


def get_images() -> list:
    """
    Returns a list of image paths, sorted by serial # (so that they are chronological)
    """
    return sort_files_numeric(os.listdir(f'{cfg.image_root_dir}/img'))


def get_recent_images(n: int) -> list:
    """
    Gets the paths of the n most recently taken images (whose fragments have been fully downlinked)
    """
    return get_images()[:n]


def get_image_data(image_file_name: str) -> dict:
    """
    Given the file name of a fully downlinked image, returns a dict containing the image's
    name, timestamp, and data (as a base64 string)
    """
    image_path = f'{cfg.image_root_dir}/img/{image_file_name}'
    with open(image_path, 'rb') as image:
        bin_img = bytearray(image.read())
    return {
        'name': os.path.basename(image_path),
        'timestamp': os.path.getmtime(image_path),
        'base64': hex.bytes_to_b64(bin_img)
    }

# try_save_image(10, 57)

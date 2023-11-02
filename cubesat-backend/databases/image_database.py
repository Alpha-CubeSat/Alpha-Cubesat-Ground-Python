import base64
import os
import shutil
from os.path import exists

import config as cfg

# keeps track of various stats regarding the received image fragments
img_fragment_downlink_info = {'image_serial': 0, 'latest_fragment': 0, 'missing_fragments': [],
                              'fragment_count': '?/?', 'highest_fragment': 0}


def save_fragment(imei: int, image_sn: int, fragment_number: int, fragment_data: str):
    """
    Saves an image fragment. Creates one if it doesn't exist using the following policy:
        - new file is created under the directory with the serial number of the image
        - the name of the file will be the fragment number with the .csfrag extension
    Example:
        - Fragment 7 of image 23 will be saved as '7.csfrag' under the directory named "23".
    :param image_sn: serial number of the image the fragment belongs to
    :param fragment_number: id number of the fragment
    :param fragment_data: hex string containing the image fragment data
    """
    # create folders if they don't exist
    if not exists(f'{cfg.image_root_dir}/{imei}/{image_sn}'):
        os.makedirs(f'{cfg.image_root_dir}/{imei}/{image_sn}')

    with open(f'{cfg.image_root_dir}/{imei}/{image_sn}/{fragment_number}.csfrag', 'wb') as frag_file:
        frag_file.write(bytearray.fromhex(fragment_data))

    global img_fragment_downlink_info
    img_fragment_downlink_info['image_serial'] = image_sn
    img_fragment_downlink_info['latest_fragment'] = fragment_number
    img_fragment_downlink_info['missing_fragments'] = []


def sort_files(files: list) -> list:
    """
    Sorts fragment files by name, stripping the extensions.
    They are numerically named, but '2.csfrag' comes before '10.csfrag'
    :param files: list of all image fragment files
    """
    return sorted(files, key=lambda x: os.path.basename(x).split('.')[0])


def generate_missing_fragments(frag_list: list):
    """
    Finds the missing fragments and the highest fragment received for an image.
    Counts through all already-received fragments every time because fragments could be received in random order.
    :param frag_list: list of previously received fragments
    """
    max_frag = max(frag_list)
    img_fragment_downlink_info['missing_fragments'] = []
    img_fragment_downlink_info['highest_fragment'] = max_frag
    for x in range(max_frag):
        if frag_list.count(x) == 0:
            img_fragment_downlink_info['missing_fragments'].append(x)


def get_saved_fragments(imei: int, image_sn: int) -> list:
    """
    Generates a list of the fragments received for a particular image as a list of numbers.
    """
    fragment_files = []
    for dir_path, _, file_names in os.walk(f'{cfg.image_root_dir}/{imei}/{image_sn}'):
        for file in file_names:
            if '.csfrag' in file:
                fragment_files.append(os.path.join(dir_path, file))
    return fragment_files


def try_save_image(imei: int, image_sn: int, total_fragments: int):
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
    fragment_map = {}  # maps fragment file path to fragment #
    for file in sort_files(get_saved_fragments(imei, image_sn)):
        fragment_map[int(os.path.splitext(os.path.basename(file))[0])] = file

    # Update fragment status dictionary
    fragment_list = list(fragment_map.keys())
    generate_missing_fragments(fragment_list)
    img_fragment_downlink_info['fragment_count'] = \
        f'{len(fragment_list)-1}/{total_fragments if total_fragments != -1 else "?"}'

    # Build final image with currently received fragments (filling in missing ones with blanks)
    if not exists(f'{cfg.image_root_dir}/{imei}/img'):
        os.makedirs(f'{cfg.image_root_dir}/{imei}/img')

    with open(f'{cfg.image_root_dir}/{imei}/img/{image_sn}.jpg', 'wb') as image_file:
        for i in range(fragment_list[-1] + 1):
            if i in fragment_list:
                image_file.write(open(fragment_map[i], 'rb').read())
            else:  # generate a blank 64 byte fragment if a fragment is missing
                print(f'fragment {i} missing')
                image_file.write(bytearray.fromhex('f' * 128))

    # if last received fragment has end flag, the image is complete so we can delete its fragments folder
    if total_fragments != -1:
        shutil.rmtree(f'{cfg.image_root_dir}/{imei}/{image_sn}')


def get_recent_images(imei: str, n: int) -> list:
    """
    Gets the paths of the n most recently taken images (whose fragments have been fully downlinked)
    Images are sorted by serial # (so that they are chronological)
    """
    if not exists(f'{cfg.image_root_dir}/{imei}'):
        return []
    return sort_files(os.listdir(f'{cfg.image_root_dir}/{imei}/img'))[:n]


def get_image_data(imei: str, image_file_name: str) -> dict:
    """
    Given the file name of a fully downlinked image, returns a dict containing the image's
    name, timestamp, and data (as a base64 string)
    """
    image_path = f'{cfg.image_root_dir}/{imei}/img/{image_file_name}'
    with open(image_path, 'rb') as image:
        bin_img = bytearray(image.read())
    return {
        'name': os.path.basename(image_path),
        'timestamp': os.path.getmtime(image_path),
        'base64': base64.b64encode(bin_img)
    }

def replace_image_fragment(imei: str, image_file_name: str, fragment_number: int, fragment_data: str):
    """
    Given the file_name of an existing image file, replaces the fragment with the 0-indexed
    fragment_number with the provided 64 byte hex fragment_data. Creates empty fragments
    if fragment_number > # fragments currently in the image
    """
    assert len(fragment_data) == 128 # each fragment is 64 bytes => 128 bits
    with open(f'{cfg.image_root_dir}/{imei}/img/{image_file_name}.jpg', 'rb') as image_file:
        current_img = image_file.read().hex()

    # if fragment already exists in image
    if fragment_number <= len(current_img) // 128:
        # splice in new fragment data: all fragments before + new fragment data + all fragments after
        new_img = current_img[:fragment_number * 128] + fragment_data + current_img[(fragment_number+1) * 128:]
    else:
        # add empty fragments to fill gap between new and existing fragments
        diff = fragment_number - len(current_img) // 128
        print(f'needed to create {diff} empty fragments')
        new_img = current_img + ('f' * 128 * diff) + fragment_data

    with open(f'{cfg.image_root_dir}/{imei}/img/{image_file_name}.jpg', 'wb') as image_file:
        image_file.write(bytearray.fromhex(new_img))
    print(f'replaced fragment {str(fragment_number)}')

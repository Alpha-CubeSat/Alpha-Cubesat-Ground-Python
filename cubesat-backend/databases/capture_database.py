import base64
import os
import shutil
from os.path import exists

import config as cfg

# keeps track of various stats regarding the received capture fragments
capture_fragment_downlink_info = {'capture_serial': 0, 'latest_fragment': 0, 'missing_fragments': [],
                              'fragment_count': '?/?', 'highest_fragment': 0}


def save_fragment(imei: int, capture_sn: int, fragment_number: int, fragment_data: str):
    """
    Saves an capture fragment. Creates one if it doesn't exist using the following policy:
        - new file is created under the directory with the serial number of the capture
        - the name of the file will be the fragment number with the .csfrag extension
    Example:
        - Fragment 7 of capture 23 will be saved as '7.csfrag' under the directory named "23".
    :param capture_sn: serial number of the capture the fragment belongs to
    :param fragment_number: id number of the fragment
    :param fragment_data: hex string containing the capture fragment data
    """
    # create folders if they don't exist
    if not exists(f'{cfg.capture_root_dir}/{imei}/{capture_sn}'):
        os.makedirs(f'{cfg.capture_root_dir}/{imei}/{capture_sn}')

    with open(f'{cfg.capture_root_dir}/{imei}/{capture_sn}/{fragment_number}.csfrag', 'wb') as frag_file:
        frag_file.write(bytearray.fromhex(fragment_data))

    global capture_fragment_downlink_info
    capture_fragment_downlink_info['capture_serial'] = capture_sn
    capture_fragment_downlink_info['latest_fragment'] = fragment_number
    capture_fragment_downlink_info['missing_fragments'] = []


def generate_missing_fragments(frag_list: list):
    """
    Finds the missing fragments and the highest fragment received for an capture.
    Counts through all already-received fragments every time because fragments could be received in random order.
    :param frag_list: list of previously received fragments
    """
    max_frag = max(frag_list)
    capture_fragment_downlink_info['missing_fragments'] = []
    capture_fragment_downlink_info['highest_fragment'] = max_frag
    for x in range(max_frag):
        if frag_list.count(x) == 0:
            capture_fragment_downlink_info['missing_fragments'].append(x)


def get_saved_fragments(imei: int, capture_sn: int) -> list:
    """
    Generates a list of the fragments received for a particular capture as a list of numbers.
    """
    fragment_files = []
    for dir_path, _, file_names in os.walk(f'{cfg.capture_root_dir}/{imei}/{capture_sn}'):
        for file in file_names:
            if '.csfrag' in file:
                fragment_files.append(os.path.join(dir_path, file))
    return fragment_files


def try_save_capture(imei: int, capture_sn: int, total_fragments: int):
    """
    Tries to assemble an capture out of fragments. If the total # of fragments currently received
    equals the total # of fragments, the completed capture is saved to the directory 'capture' as a
    jpeg file with the serial number as a name.

    Example: If capture 23 is complete when this function is called, the completed capture will
    be saved as '23.jpg' under 'capture', and assembled out of the fragment files in the directory '23'
    :param capture_sn: serial number of the capture to be assembled
    :param total_fragments: the total # of fragments needed to assemble the capture
    """
    # Get all currently received fragments
    fragment_map = {}  # maps fragment file path to fragment #
    sorted_frag_files = sorted(get_saved_fragments(imei, capture_sn),
                               key=lambda x: int(os.path.basename(x).split('.')[0]))
    for file in sorted_frag_files:
        fragment_map[int(os.path.splitext(os.path.basename(file))[0])] = file

    # Update fragment status dictionary
    fragment_list = list(fragment_map.keys())
    generate_missing_fragments(fragment_list)
    capture_fragment_downlink_info['fragment_count'] = \
        f'{len(fragment_list)-1}/{total_fragments if total_fragments != -1 else "?"}'

    # Build final capture with currently received fragments (filling in missing ones with blanks)
    if not exists(f'{cfg.capture_root_dir}/{imei}/capture'):
        os.makedirs(f'{cfg.capture_root_dir}/{imei}/capture')

    with open(f'{cfg.capture_root_dir}/{imei}/capture/{capture_sn}.jpg', 'wb') as capture_file:
        for i in range(fragment_list[-1] + 1):
            if i in fragment_list:
                capture_file.write(open(fragment_map[i], 'rb').read())
            else:  # generate a blank 64 byte fragment if a fragment is missing
                print(f'fragment {i} missing')
                capture_file.write(bytearray.fromhex('f' * 128))

    # if last received fragment has end flag, the capture is complete so we can delete its fragments folder
    if total_fragments != -1:
        shutil.rmtree(f'{cfg.capture_root_dir}/{imei}/{capture_sn}')


def replace_capture_fragment(imei: str, capture_file_name: str, fragment_number: int, fragment_data: str):
    """
    Given the file_name of an existing capture file, replaces the fragment with the 0-indexed
    fragment_number with the provided 64 byte hex fragment_data. Creates empty fragments
    if fragment_number > # fragments currently in the capture
    """
    assert len(fragment_data) == 128 # each fragment is 64 bytes => 128 bits
    with open(f'{cfg.capture_root_dir}/{imei}/capture/{capture_file_name}.jpg', 'rb') as capture_file:
        current_capture = capture_file.read().hex()

    # if fragment already exists in capture
    if fragment_number <= len(current_capture) // 128:
        # splice in new fragment data: all fragments before + new fragment data + all fragments after
        new_capture = current_capture[:fragment_number * 128] + fragment_data + current_capture[(fragment_number+1) * 128:]
    else:
        # add empty fragments to fill gap between new and existing fragments
        diff = fragment_number - len(current_capture) // 128
        print(f'needed to create {diff} empty fragments')
        new_capture = current_capture + ('f' * 128 * diff) + fragment_data

    with open(f'{cfg.capture_root_dir}/{imei}/capture/{capture_file_name}.jpg', 'wb') as capture_file:
        capture_file.write(bytearray.fromhex(new_capture))
    print(f'replaced fragment {str(fragment_number)}')

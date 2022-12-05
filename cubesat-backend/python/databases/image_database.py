import config as cfg

img_display_info =  {'image-serial': 0, 'latest-fragment': 0, 'missing_fragments': "None", 'fragment-count': '?/?', "highest-fragment": 0}
fragment_list = {'list': []}

"Gets the root directory of the image database as given in the config file"
def get_root_path():
    return cfg.get_config(cfg.image_root_dir())

"""Finds the missing fragments and the highest fragment received for an image. 
  It counts through all already-received fragments every time because fragments could be receieived in random order."""
def generate_missing_fragments(frag_list):
    max_frag = max(frag_list)
    img_display_info['missing_fragments'] = ''
    img_display_info['highest_fragment'] = max_frag
    for x in range(max_frag):
        missing_frags = img_display_info['missing_fragments']
        missing_fra
        
    if img_display_info['missing_fragments'] == '':
        img_display_info['missing_fragments'] = None

def save_fragment(image_sn, fragment_number, binary_fragment_data):
    pass

def try_save_image(image_sn, total_fragment_number):
    pass

# def get_img_display_info():
#     return {}

"""Returns a seq of images, sorted by id (so that they're chronological -
   rockblock may send data out of order, using the serial number is
   the only way to be sure of ordering)"""
def get_images():
    pass

def get_recent_images(n):
    pass

def get_image_by_name(name):
    pass
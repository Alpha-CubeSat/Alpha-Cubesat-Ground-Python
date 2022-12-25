import config as cfg

img_display_info =  {'image-serial': 0, 'latest-fragment': 0, 'missing_fragments': "None", 'fragment-count': '?/?', "highest-fragment": 0}
fragment_list = {'list': []}

"Gets the root directory of the image database as given in the config file"
def get_root_path():
    return cfg.image_root_dir

"""Finds the missing fragments and the highest fragment received for an image. 
  It counts through all already-received fragments every time because fragments could be receieived in random order."""
def generate_missing_fragments(frag_list):
    max_frag = max(frag_list)
    img_display_info['missing_fragments'] = ''
    img_display_info['highest_fragment'] = max_frag
    for x in range(max_frag):
        missing_frags = img_display_info['missing_fragments']
        #missing_fra
        
    if img_display_info['missing_fragments'] == '':
        img_display_info['missing_fragments'] = None

"""Saves an image fragment. Creates one if it doesn't exist using the following policy:
- new file is created under the directory with the serial number of the image
- the name of the file will be the fragment number with the .csfrag extension
Example:
If fragment 7 of image 23 is saved,
then it will be saved as '7.csfrag' in the directory named '23'.
Note: binary-fragment-data accepts a JAVA BYTE ARRAY, byte[], not a ByteBuffer or clojure vector"""
def save_fragment(image_sn, fragment_number, binary_fragment_data):
    pass

"Generates a list of the fragments receieved for a particular image as a list of numbers."
def generate_fragment_list(fragment_files):
    pass

"""Sorts fragment files by name, stripping the extensions. They are numerically named,
but '2.csfrag' should come before '10.csfrag'"""
def sort_numeric_files(files, extension):
    pass

"""Tries to assemble an image out of fragments. If there are enough, saves the image
to the directory 'img' as a jpeg file with the serial number as a name. Returns nil
otherwise.
Example:
If image 23 is complete and try-save-image is called, the completed image will
be saved as '23.png' under 'img', and assembled out of the fragment files in the directory '23'"""
def try_save_image(image_sn, total_fragment_number):
    pass

"Returns the contents of the atom img-display-info"
def get_img_display_info():
    return {}

"""Returns a seq of images, sorted by id (so that they're chronological -
   rockblock may send data out of order, using the serial number is
   the only way to be sure of ordering)"""
def get_images():
    pass

"Gets the n most recently taken images (whose data has been fully received by ground)"
def get_recent_images(n):
    pass

"Gets the most recent complete image"
def get_most_recent():
    pass

def get_image_by_name(name):
    pass
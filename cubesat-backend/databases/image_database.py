import config as cfg
import os
import binascii

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
        if not frag_list.contains(x):
            missing_frags = img_display_info['missing_fragments']
            img_display_info['missing_fragments'] = missing_frags + x
        
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
    db_root_dir = get_root_path()
    frag_file = open(db_root_dir + '/' + image_sn + '/' + fragment_number + '.csfrag')
    try:
        os.makedirs('../' + image_sn)
    except FileExistsError:      
        pass 

    img_display_info['image_serial'] = image_sn
    img_display_info['latest_fragment'] = fragment_number
    img_display_info['missing_fragments'] = ""
    fragment_list['list'] = []

    frag_file.write(binary_fragment_data)
    frag_file.flush()
    frag_file.close()


"Generates a list of the fragments receieved for a particular image as a list of numbers."
def generate_fragment_list(fragment_files):
    for fragment in fragment_files:
        newlist = os.path.splitext(os.path.basename(fragment))[0]
        fragment_list['list'].append(newlist)

"""Sorts fragment files by name, stripping the extensions. They are numerically named,
but '2.csfrag' should come before '10.csfrag'"""
def sort_numeric_files(files, extension):
    return sorted(files, key=lambda x: int(os.path.splitext(x)[0]))


"""Tries to assemble an image out of fragments. If there are enough, saves the image
to the directory 'img' as a jpeg file with the serial number as a name. Returns nil
otherwise.
Example:
If image 23 is complete and try-save-image is called, the completed image will
be saved as '23.png' under 'img', and assembled out of the fragment files in the directory '23'"""
def try_save_image(image_sn, total_fragment_number):
    db_root_dir = get_root_path()
    fragment_dir = str(db_root_dir) + '/' + str(image_sn)

    fragment_files = []
    for r, d, f in os.walk(fragment_dir):
        for file in f:
            if '.csfrag' in file:
                fragment_files.append(os.path.join(r, file))

    num_fragments = 0
    for root_dir, cur_dir, files in os.walk(fragment_dir):
        num_fragments += len(files)

    if total_fragment_number == -1:
        string_total = str(num_fragments) + '/?'
    else:
        string_total = num_fragments + '/' + total_fragment_number

    img_dir = str(db_root_dir) + '/img'
    img_file_path = str(img_dir) + '/img' + image_sn + '.jpeg'

    generate_fragment_list(fragment_files)
    generate_missing_fragments(fragment_list['list'])
    img_display_info['fragment-count'] = string_total
    try:
        os.makedirs('../' + img_dir)
    except FileExistsError:      
        pass 

    if num_fragments == total_fragment_number:
        sorted_fragments = sort_numeric_files(fragment_files, ".csfrag")
        image_file = open(img_file_path)
        for fragment in sorted_fragments:
            frag = fragment.read(fragment.open(fragment_dir))
            image_file.write(frag)

        image_file.flush()
        image_file.close()
            
"Returns the contents of the atom img-display-info"
def get_img_display_info():
    return img_display_info

"""Returns a seq of images, sorted by id (so that they're chronological -
   rockblock may send data out of order, using the serial number is
   the only way to be sure of ordering)"""
def get_images():
    unsorted_files = os.listdir(str(get_root_path) + '/img')
    return sort_numeric_files(unsorted_files, '.jpeg')

"Gets the n most recently taken images (whose data has been fully received by ground)"
def get_recent_images(n):
    return get_images()[:n]


"Gets the most recent complete image"
def get_most_recent():
    return get_recent_images(1)


def get_image_by_name(name):
    return str(get_root_path) + '/img/' + name



import json


PATH_TO_KEY = "set_path_to_your_key_file_here_or_set_AKEY_below"

AKEY = None

if AKEY is None:
    with open(PATH_TO_KEY) as json_in:
        AKEY = json.load(json_in)['key']

PATH_TO_FOLDER_TO_INDEX = "./test_folder"
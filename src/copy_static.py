import shutil

import os


def copy_static_files(source, destination):
    if not os.path.exists(source):
        os.mkdir(source)  
    if os.path.exists(destination):
        shutil.rmtree(destination)
        os.mkdir(destination)
    else:
        os.mkdir(destination)
    get_all_items(source, destination)
    

def get_all_items(source, destination):
    source_items = os.listdir(source)
    for item in source_items:
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        if os.path.isdir(source_path):
            if not os.path.exists(destination_path):
                os.mkdir(destination_path)
            get_all_items(source_path, destination_path)
        elif os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
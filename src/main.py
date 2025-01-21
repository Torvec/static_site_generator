import shutil
import os

def main():
    source_dir = "./static"
    dest_dir = "./public"
    copy_static_files(source_dir, dest_dir)


def copy_static_files(source, destination):
    if not os.path.exists(source):
        os.mkdir(source)
        print(f"{source} Created")
        
    if os.path.exists(destination):
        shutil.rmtree(destination)
        print(f"Deleted all from {destination}")
        os.mkdir(destination)
        print(f"Re-created {destination}")
    else:
        os.mkdir(destination)
        print(f"{destination} created")

    get_all_items(source, destination)
    

def get_all_items(source, destination):
    source_items = os.listdir(source)
    for item in source_items:
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        if os.path.isdir(source_path):
            if not os.path.exists(destination_path):
                os.mkdir(destination_path)
                print(f"Sub-directory: {destination_path} Created")
            get_all_items(source_path, destination_path)
        elif os.path.isfile(source_path):
            print(f"File found: {item}")
            shutil.copy(source_path, destination_path)

if __name__ == "__main__":
    main()
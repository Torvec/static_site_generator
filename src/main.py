import os

from copy_static import copy_static_files

from generate_content import generate_pages_recursive


source_dir = "./static"
dest_dir = "./public"
content_dir = "./content"
template_path = "./template.html"


def main():    
    copy_static_files(source_dir, dest_dir)
    generate_pages_recursive(content_dir, template_path, dest_dir)


if __name__ == "__main__":
    main()
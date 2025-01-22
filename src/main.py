import os

from copy_static import copy_static_files

from generate_content import generate_page


source_dir = "./static"
dest_dir = "./public"
content_dir = "./content"
template_path = "./template.html"


def main():    
    copy_static_files(source_dir, dest_dir)
    generate_page(
        os.path.join(content_dir, "index.md"),
        template_path,
        os.path.join(dest_dir, "index.html"),
    )


if __name__ == "__main__":
    main()
import os
import shutil

from copystatic import copy_to_public
from generate_page import generate_pages_recursive

def main():

    dir_path_static = "./static"
    dir_path_public = "./public"
    dir_path_content = "./content"
    template_path = "./template.html"

    try:
        copy_to_public(dir_path_static, dir_path_public)
        print("Static files successfully copied to public directory!")
    except Exception as e:
        print(f"Error copying static files: {e}")

    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)

main()
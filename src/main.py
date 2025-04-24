import os
import shutil
import sys

from copystatic import copy_to_public
from generate_page import generate_pages_recursive

def main():

    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    dir_path_static = "./static"
    dir_path_public = "./docs"
    dir_path_content = "./content"
    template_path = "./template.html"

    try:
        copy_to_public(dir_path_static, dir_path_public)
        print("Static files successfully copied to public directory!")
    except Exception as e:
        print(f"Error copying static files: {e}")

    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)

main()
from textnode import TextType
from textnode import TextNode
from htmlnode import HTMLNode
from copystatic import copy_to_public

def main():

    source_dir = "static"
    destination_dir = "public"

    try:
        copy_to_public(source_dir, destination_dir)
        print("Static files successfully copied to public directory!")
    except Exception as e:
        print(f"Error copying static files: {e}")

main()
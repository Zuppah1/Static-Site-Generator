import os
from block_markdown import markdown_to_html_node
from htmlnode import HTMLNode

def extract_title(markdown):
    if markdown.startswith("# "):
        return markdown.lstrip("# ").strip()
    else:
        raise Exception("missing title")

def generate_page(from_path, template_path, dest_path):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown_file = f.read()
    
    with open(template_path) as f:
        template_file = f.read()

    html_node = markdown_to_html_node(markdown_file)
    html_string = html_node.to_html()

    title = extract_title(markdown_file)

    template_file = template_file.replace("{{ Title }}", title)
    template_file = template_file.replace("{{ Content }}", html_string)
    
    dest_dir = os.path.dirname(dest_path)

    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, 'w') as f:
        f.write(template_file)
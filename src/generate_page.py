import os
from pathlib import Path
from block_markdown import markdown_to_html_node


def extract_title(markdown):
    if markdown.startswith("# "):
        return markdown.lstrip("# ").strip()
    else:
        raise Exception("missing title")

def generate_page(from_path, template_path, dest_path, basepath):

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
    template = template_file.replace('href="/', 'href="' + basepath)
    template = template_file.replace('src="/', 'src="' + basepath)
    
    dest_dir = os.path.dirname(dest_path)

    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, 'w') as f:
        f.write(template_file)

def generate_pages_recursive(from_path_content, template_path, dest_dir_path, basepath):

    directory_list = os.listdir(from_path_content)

    for item in directory_list:

        source_path = os.path.join(from_path_content, item)
        destination_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(source_path):
            destination_path = Path(destination_path).with_suffix(".html")
            generate_page(source_path, template_path, destination_path, basepath)

        else:
            generate_pages_recursive(source_path, template_path, destination_path, basepath)
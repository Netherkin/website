import shutil
import os
from markdown_to_html import *

def delete_and_copy(source_dir="static", dest_dir="public"):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir, exist_ok=True)
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            print(f"Copied file: {source_path} to {dest_path}")
        else:
            os.makedirs(dest_path, exist_ok=True)
            delete_and_copy(source_path, dest_path)

def generate_page(from_path="content/index.md", template_path="template.html", dest_path="public/index.html"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as read_from_path:
        markdown_content = read_from_path.read()
    with open(template_path, "r") as read_template_path:
        template_content = read_template_path.read()
    html_string = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    full_html_page = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    with open(dest_path, "w") as new_html_file:
        new_html_file.write(full_html_page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    




def main():
    delete_and_copy()
    generate_page()


if __name__ == "__main__":
    main()
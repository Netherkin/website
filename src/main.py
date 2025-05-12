import shutil
import os
from markdown_to_html import *
import sys

def delete_and_copy(source_dir="static", dest_dir="docs"):
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

def generate_pages_recursive(dir_path_content="content", template_path="template.html", dest_dir_path="docs", basepath="/"):
    for file in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(source_path) and os.path.splitext(source_path)[1] == ".md":
            html_file_name = os.path.splitext(dest_path)[0] + ".html"
            with open(source_path, "r") as read_from_path:
                markdown_content = read_from_path.read()
            with open(template_path, "r") as read_template_path:
                template_content = read_template_path.read()
            html_string = markdown_to_html_node(markdown_content).to_html()
            try:
                title = extract_title(markdown_content)
            except Exception as e:
                print(f"Warning: Could not extract title from {source_path}: {e}")
                title = "Untitled Page"
            full_html_page = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_string).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
            parent_dir = os.path.dirname(html_file_name)
            os.makedirs(parent_dir, exist_ok=True)
            with open(html_file_name, "w") as new_html_file:
                new_html_file.write(full_html_page)
        elif os.path.isdir(source_path):
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(source_path, template_path, dest_path)

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    delete_and_copy()
    generate_pages_recursive(basepath=basepath)

if __name__ == "__main__":
    main()
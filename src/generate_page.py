from blocks import markdown_to_html_node
from extract_title import extract_title
import os

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        from_path_content = f.read()
    with open(template_path) as f:
        html_template = f.read()


    content_to_html = markdown_to_html_node(from_path_content).to_html()
    extracted_title = extract_title(from_path_content)
    if "{{ Title }}" not in html_template or "{{ Content }}" not in html_template:
        raise Exception("Template is missing '{{ Title }}' or '{{ Content }}' placeholder.")
    updated_template = html_template.replace("{{ Title }}", extracted_title).replace("{{ Content }}", content_to_html)
    updated_template = updated_template.replace('href="/', f'href="{basepath}')
    updated_template = updated_template.replace('src="/', f'src="{basepath}')


    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(updated_template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/", content_root=None):
    
    if content_root is None:
        content_root = dir_path_content

    files = os.listdir(dir_path_content)

    for thing in files:
        path_to_thing = os.path.join(dir_path_content, thing)
        if os.path.isfile(path_to_thing) and thing.endswith(".md"):
            with open(path_to_thing) as f:
                file_content = f.read()
            relative_path = os.path.relpath(path_to_thing, start = content_root)
            root, ext = os.path.splitext(relative_path)
            dest_path = os.path.join(dest_dir_path, root + '.html')
            generate_page(path_to_thing, template_path, dest_path, basepath)

        if os.path.isdir(path_to_thing):
            new_dir_path = os.path.join(dir_path_content, thing)
            generate_pages_recursive(new_dir_path, template_path, dest_dir_path, basepath, content_root)

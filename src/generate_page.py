from blocks import markdown_to_html_node
from extract_title import extract_title
import os

def generate_page(from_path, template_path, dest_path):
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


    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(updated_template)


from static_copy import copy_files
from generate_page import generate_pages_recursive

def main():
    copy_files("static", "public")
    generate_pages_recursive("content", "template.html", "public")
    return


if __name__ == "__main__":
    main()






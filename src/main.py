from static_copy import copy_files
from generate_page import generate_pages_recursive
import sys

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    copy_files("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)
    return


if __name__ == "__main__":
    main()






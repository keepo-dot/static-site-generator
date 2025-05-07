


def extract_title(markdown):
    markdown_copy = markdown
    markdowen_lines = markdown_copy.split("\n")
    for line in markdowen_lines:
        if line.startswith('# '):
            stripped_line = line[2:].strip()
            return stripped_line
    raise Exception("No header found.")

import os

from block_markdown import markdown_to_htmlnode


def generate_page(from_path, template_path, dest_path):
    print(f"\n\nGenerating page from {from_path} to {dest_path} using {template_path}\n\n")
    with open(from_path, 'r') as mf, open(template_path, 'r') as tf:
        content = mf.read()
        title = extract_title(content)
        content_to_htmlnodes = markdown_to_htmlnode(content)
        content_to_html = content_to_htmlnodes.to_html()
        template_file = tf.read()
        final = template_file.replace("{{ Title }}", title).replace("{{ Content }}", content_to_html)

        if os.path.exists(dest_path):
            with open(dest_path, 'w') as df:
                df.write(final)
        else:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path, 'w') as df:
                df.write(final)


def extract_title(markdown):
    split_markdown = markdown.split("\n")
    for line in split_markdown:
        if line.startswith("# "):
            return line[1:].strip()
    raise Exception("No Title Found!")
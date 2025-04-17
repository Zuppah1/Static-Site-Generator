def markdown_to_blocks(markdown):
    markdown_list = []
    split_list = markdown.split("\n\n")
    for block in split_list:
        block = block.strip()
        if not block:
            continue
        markdown_list.append(block)
    return markdown_list


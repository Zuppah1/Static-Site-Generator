import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH= "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    markdown_list = []
    split_list = markdown.split("\n\n")
    for block in split_list:
        block = block.strip()
        if not block:
            continue
        markdown_list.append(block)
    return markdown_list



def block_to_block_type(block):
    if block.startswith("#") and " " in block and len(block.split(" ")[0]) <= 6:
        return BlockType.HEADING
    
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    elif all(line.startswith(">") for line in block.splitlines()):
        return BlockType.QUOTE
    
    elif all(line.startswith("- ") for line in block.splitlines()):
        return BlockType.UNORDERED_LIST
    
    elif all(line.split(". ")[0].isdigit() and int(line.split(". ")[0]) == i + 1 for i, line in enumerate(block.splitlines())):
        return BlockType.ORDERED_LIST
    
    else:
        return BlockType.PARAGRAPH

       

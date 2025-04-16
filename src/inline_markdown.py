import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, text_node_to_html_node, ParentNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes_list.append(node)
            continue
            
        current_text = node.text
        
        while True:
            start_pos = current_text.find(delimiter)
            if start_pos == -1:
                
                if current_text:  
                    new_nodes_list.append(TextNode(current_text, TextType.TEXT))
                break
                
            end_pos = current_text.find(delimiter, start_pos + len(delimiter))
            if end_pos == -1:
               
                raise ValueError(f"Closing delimiter not found for '{delimiter}'")
                
            if start_pos > 0:
                new_nodes_list.append(TextNode(current_text[:start_pos], TextType.TEXT))
                
            delimited_text = current_text[start_pos + len(delimiter):end_pos]
            new_nodes_list.append(TextNode(delimited_text, text_type))
            
            current_text = current_text[end_pos + len(delimiter):]

    return new_nodes_list

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):

    new_nodes_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes_list.append(node)
            continue

        remaining_text = node.text
        
        while True:
            match = extract_markdown_images(remaining_text)
            if not match:
                if remaining_text:
                    new_nodes_list.append(TextNode(remaining_text, TextType.TEXT))
                break
                               
            alt_text = match[0][0]
            url_text = match[0][1]
            full_match_text = f"![{alt_text}]({url_text})"

            parts = remaining_text.split(full_match_text, 1)
            before = parts[0]
            after = parts[1] if len(parts) > 1 else ""

            if before:
                new_nodes_list.append(TextNode(before, TextType.TEXT))

            new_nodes_list.append(TextNode(alt_text, TextType.IMAGE, url_text))

            remaining_text = after

    return new_nodes_list


def split_nodes_link(old_nodes):

    new_nodes_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes_list.append(node)
            continue

        remaining_text = node.text
        
        while True:
            match = extract_markdown_links(remaining_text)
            if not match:
                if remaining_text:
                    new_nodes_list.append(TextNode(remaining_text, TextType.TEXT))
                break
                               
            alt_text = match[0][0]
            url_text = match[0][1]
            full_match_text = f"[{alt_text}]({url_text})"

            parts = remaining_text.split(full_match_text, 1)
            before = parts[0]
            after = parts[1] if len(parts) > 1 else ""

            if before:
                new_nodes_list.append(TextNode(before, TextType.TEXT))

            new_nodes_list.append(TextNode(alt_text, TextType.LINK, url_text))

            remaining_text = after

    return new_nodes_list
                                      
                                    
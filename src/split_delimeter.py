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
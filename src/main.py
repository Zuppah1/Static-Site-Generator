from textnode import TextType
from textnode import TextNode
from htmlnode import HTMLNode

def main():

    test = TextNode("This is a test", TextType.BOLD, "https://www.boot.dev")
    test_html = HTMLNode("This", "Is", "A", "Test")

    print(test, test_html)

main()
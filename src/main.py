from textnode import TextType
from textnode import TextNode

def main():

    test = TextNode("This is a test", TextType.BOLD, "https://www.boot.dev")

    print(test)

main()
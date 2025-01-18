from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    textnode = TextNode("Some Text", TextType.BOLD, "https://www.boot.dev")
    print(textnode)
    htmlnode = HTMLNode("p", "hi", None, None)
    print(htmlnode)

if __name__ == "__main__":
    main()
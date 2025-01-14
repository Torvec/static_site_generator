from textnode import TextNode
from htmlnode import HTMLNode

def main():
    text = TextNode("Testing", "bold", "https://www.boot.dev")
    print(text)
    html = HTMLNode(tag="p", value="Some Value", children=[], props={"id":"test"})
    print(html)

if __name__ == "__main__":
    main()
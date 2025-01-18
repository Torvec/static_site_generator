from textnode import TextNode, TextType

def main():
    textnode = TextNode("Some Text", TextType.BOLD, "https://www.boot.dev")
    print(textnode)

if __name__ == "__main__":
    main()
import unittest

from generate_content import extract_title


class TestGenerateContent(unittest.TestCase):
    def test_extract_title_output(self):
        input_markdown = '''# Tolkien Fan Club

**I like Tolkien**. Read my [first post here](/majesty) (sorry the link doesn't work yet)

> All that is gold does not glitter

## Reasons I like Tolkien

- You can spend years studying the legendarium and still not understand its depths
- It can be enjoyed by children and adults alike
- Disney _didn't ruin it_
- It created an entirely new genre of fantasy'''
        expected_output = "Tolkien Fan Club"
        self.assertEqual(extract_title(input_markdown), expected_output)

    def test_extract_title_error(self):
        input_markdown = '''## Tolkien Fan Club

**I like Tolkien**. Read my [first post here](/majesty) (sorry the link doesn't work yet)

> All that is gold does not glitter

## Reasons I like Tolkien

- You can spend years studying the legendarium and still not understand its depths
- It can be enjoyed by children and adults alike
- Disney _didn't ruin it_
- It created an entirely new genre of fantasy'''
        expected_output = "No Title Found!"
        with self.assertRaises(Exception) as context:
            extract_title(input_markdown)
        self.assertEqual(str(context.exception), expected_output)
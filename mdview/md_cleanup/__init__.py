"""
A script to strip formatting from Pandoc's markdown that slows done reading of
the Markdown source.

This script would be better written as a pandoc filter with proper Pandoc
AST parsing. For lack of time, it is regex-based. Patches welcome :)."""

import re
import sys

REPLACE_PATTERNS = [
        # strip formatting from inline code blocks, i.e. `foo`{.bar .baz}
        re.compile(r"(`[^`]+`)\{\..+?\}", re.DOTALL),
        # strip formatting from images or links
        re.compile(r"(!?\[.+?\]\(.+?\))\{.+?\}", re.DOTALL)
]

def strip_divs(contents):
    """Strip all lines start with a :::"""
    return '\n'.join(line
            for line in contents.split("\n")
                     if not line.lstrip().startswith(":::")
    )

def strip_nonbreaking_space(text):
    return text.replace("\xa0", " ")

def strip_unwanted_css_from_elements(contents):
    """In Pandoc's Markdown, additional attributes, including CSS-classes for
    visual formatting, can be attached. They are not useful if the document is
    not meant to be exported with a specific style sheet and are hence
    stripped."""
    for pattern in REPLACE_PATTERNS:
        contents = pattern.sub(r"\1", contents)
    return contents


def md_cleanup(document):
    """Take a document a s a string and perform all formatting changes defined
    in this module."""
    document = strip_nonbreaking_space(document)
    document = strip_unwanted_css_from_elements(document)
    document = strip_divs(document)
    return document

def main():
    if len(sys.argv) != 2:
        print("E: requires one argument, file name or `-` for stdin")
        sys.exit(1)
    text = None
    input_file = sys.argv[1]
    if input_file == "-":
        text = sys.stdin.read()
    else:
        with open(input_file, encoding="UTF-8") as fhandle:
            text = fhandle.read()
    text = md_cleanup(text)
    if input_file == "-":
        print(text)
    else:
        with open(input_file, "w", encoding="UTF-8") as fhandle:
            fhandle.write(text)

if __name__ == '__main__':
    main()

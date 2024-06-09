**View files in Markdown**

Pandoc's Markdown is a universal pivot format from and into many formats. It
can also be used to read documents on the command-line, with a certain amount of
markup and a high degree of accessibility for screen reader users.

This package contains various helper scripts to convert from and into markdown,
as well as to work with Markdown


Install
======

    $ pipx install .

mdview
=======


This script uses Libreoffice and Pandoc to convert any format that Libreoffice
can open and converts it to Markdown to view it in Vim. It uses Pandoc to
preserve the formatting as much as possible.

Dependencies
------------

Python 3, Libreoffice and Pandoc.

-  Debian: `sudo apt install libreoffice-common pandoc python3`
    -   Install `libre-office-calc` (or impress or writer) for the corresponding
        file format support.

Example Usage
-------------

    $ mdview important_letter.docx
    $ mdview boring_presentation.odp

Configuration
-------------

mdview can be configured by environment variables:

### `EDITOR`

Set the editor to use. If not set, the editor for viewing the Markdown file will
be guessed.

### `MDVIEW_CONF`

Set mdview-specific configuration. Keys and values are separated by a colon,
multiple key/value pairs are separated by commas.

| Key       | Value                         |
| --------- | ----------------------------- |
| linewidth | Number of columns per line    |


`md_cleanup`
========

However, some features not strictly required for human readers can interfere,
for instance, CSS selectors for individual cinline code examples, e.g.:

    This can be achieved with the `foo()`{.code .style_bold} function.

In this case, the CSS formatting is useless. The script in this directory strips
these instructions that prevent continuous reading.

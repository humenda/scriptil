LOview — view a document in any LibreOffice-openable document in vim using pandoc
====================================================================================

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

    $ loview important_letter.docx
    $ loview boring_presentation.odp

Configuration
-------------

LOview can be configured by environment variables:

### `EDITOR`

Set the editor to use. If not set, the editor for viewing the Markdown file will
be guessed.

### `LOVIEW_CONF`

Set LOview-specific configuration. Keys and values are separated by a colon,
multiple key/value pairs are separated by commas.

| Key       | Value                         |
| --------- | ----------------------------- |
| linewidth | Number of columns per line    |

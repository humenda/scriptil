LOview — view a document in any LibreOffice-openable document in vim using pandoc
====================================================================================

This script uses Libreoffice and Pandoc to convert any format that Libreoffice
can open and converts it to Markdown to view it in Vim. It uses Pandoc to
preserve the formatting as much as possible.

Dependencies
------------

Python 3, Libreoffice and Pandoc.

i-  Debian: `sudo apt install libreoffice-common pandoc python3`
    -   Install `libre-office-calc` (or impress or writer) for the corresponding
        file format support.

Example Usage
-------------

    $ loview important_letter.docx
    $ loview boring_presentation.odp

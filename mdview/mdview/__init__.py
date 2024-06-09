#!/usr/bin/env python3
"""Usage: mdview <FILE> -- view a document in any LibreOffice-openable document in vim using pandoc
for Markup preservation.

Author: Sebastian Humenda
Licence: 2020-2024, LGPL-3

This script uses Libreoffice and Pandoc to convert any format that Libreoffice
converts to Markdown and views it in Vim.

By setting the environment variable $EDITOR, you can select your favourite
editor. Defaults to vim.

There is also a rudimentary configuration (environment) variable called `MDVIEW_CONF`. At the
moment, the only value that can be specified is `linewidth`. The configuration could look like this:

        MDVIEW_CONF=linewidth:80

ToDo:

-   allow to view the HTML file straight in a (text) browser to preserve tables
"""

import argparse
import atexit
import os
import shlex
import subprocess
import sys

import md_cleanup

# This is not thread-safe
TEMPORARY_FILES = []
DEFAULT_CONF = {
        "linewidth": "80",
    }

def read_config():
    """Read the configuration from the MDVIEW_CONF variable. Return a dictionary with the parsed
    values."""
    conf_vals = dict(DEFAULT_CONF)
    if "MDVIEW_CONF" in os.environ:
        for item in os.environ["MDVIEW_CONF"].split(","):
            try:
                key, val = item.split(":")
            except ValueError:
                print("Invalid configuration syntax in MDVIEW_CONF environment variable: {item}")
                print("Expected KEY:VALUE")
                sys.exit(82)
            conf_vals[key] = val
    return conf_vals


def remove_temporary_files():
    """Remove temporary files in case of a crash or premature termination. This is not
    thread-safe.
    This is a callback function intended to be registered with atexit."""
    for file in TEMPORARY_FILES:
        try:
            os.remove(file)
            # Try to remove any images. LO puts them usually right next to the converted files.
            basename = os.path.splitext(os.path.basename(file))[0]
            images = [img for img in os.listdir('.')
                  if img.startswith(basename) and img.endswith('jpg')]
            for image in images:
                os.remove(image)
        except OSError:
            pass

def execute(command, communication=True, scan_out_for_err=False):
    """Execute a command, a thin wrapper around subprocess.call().
    If `communication=True`, stdout will be returned.
    Some programs like libreoffice do not use exit codes properly. The switch
    `scan_out_for_err` scans the captured output for an error indication,
    instead."""
    text = ''
    if communication:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Libreoffice does not use error codes properly, look for "error"
        text = '\n'.join([t.decode(sys.getdefaultencoding())
            for t in proc.communicate() if t])
    else:
        proc = subprocess.Popen(command)
    ret = proc.wait()
    if ret > 0 or (scan_out_for_err and ('error' in text or 'Error' in text)):
        print(f"Error while executing: {command}")
        if text:
            print('   ', text.replace('\n', '\n    ').rstrip())
        sys.exit(38)
    return text

def spawn_libreoffice(input_file):
    """Convert the given input file to HTML output."""
    execute(["libreoffice", "--convert-to", "html", input_file],
            scan_out_for_err=True)

def spawn_pdftohtml(pdf_file):
    """Convert the given input file to HTML output using pdftohtml."""
    # -s: single page
    # -i: ignore images
    execute(["pdftohtml", "-s", "-i", "-noframes", "-enc", "UTF-8", "-nodrm", pdf_file])

def get_editor():
    if os.environ.get('EDITOR'):
        return os.environ['EDITOR']
    if not shutil.which('vim'): # Nano is the de-facto standard these days
        return 'nano'
    return 'vim'

def parse_args():
    """Parse command-line args, returning a argument object."""
    parser = argparse.ArgumentParser(prog=sys.argv[0])
    parser.add_argument(
        '-p',
        "--pdftohtml",
        dest="pdftohtml",
        action="store_true",
        default=False,
        help=
        'if given, use pdftohtml for better markup preservation of PDF documents'
    )
    parser.add_argument('input_file', help='input file name')
    return parser.parse_args()

def main():
    """Script entry point."""
    args = parse_args()
    atexit.register(remove_temporary_files)

    conf = read_config()

    #    ToDo: probably merge with argument parser
    document_path = args.input_file
    document_dir = os.path.dirname(document_path)
    if document_dir:
        # libreoffice has strange --output-dir rules, change cwd
        os.chdir(document_dir)
    document_path = os.path.basename(document_path)

    basename, extension = os.path.splitext(document_path)
    intermediate_html = f'{basename}.html'

    TEMPORARY_FILES.append(intermediate_html)
    # both programs just add the HTML extension and accept no out parameter
    if args.pdftohtml:
        spawn_pdftohtml(document_path)
    else:
        spawn_libreoffice(document_path)
    markdown_doc = execute(["pandoc", "--columns", conf["linewidth"], "-t", "markdown", intermediate_html])
    markdown_doc = md_cleanup.md_cleanup(markdown_doc)
    intermediate_md = intermediate_html + '.md'
    TEMPORARY_FILES.append(intermediate_md)

    with open(intermediate_md, 'w') as file:
        file.write(markdown_doc)
    execute([get_editor(), intermediate_md], communication=False)

if __name__ == '__main__':
    main()

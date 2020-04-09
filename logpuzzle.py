#!/usr/bin/env python3
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""

import os
import re
import sys
import urllib.request as urllib
import argparse


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    lit = re.compile(r"GET (/[\S]*/puzzle/[\S]*)")
    url_list = []
    with open(filename, 'r') as f:
        for l in f:
            get_string = re.search(lit, l)
            if get_string:
                g_string = get_string.group(1)
                f_name = filename[filename.index('_') + 1:]
                url_string = f_name + g_string
                if url_string not in url_list:
                    url_list.append(url_string)
    url_list = sorted(url_list, key=lambda u: u[-8:])
    return url_list



def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for i, url in enumerate(img_urls):
        url = "http://" + url
        print(url)
        dest = os.path.join(dest_dir, "img" + str(i) + ".jpg")
        urllib.urlretrieve(url, dest)
    with open(os.path.join(dest_dir, "index.html"), "w") as w:
        w.write("<html>\n<body>\n")
        for i in range(len(img_urls)):
            w.write("<img src='img{}.jpg' />".format(i))
        w.write("</body>\n</html>")

def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser

def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])

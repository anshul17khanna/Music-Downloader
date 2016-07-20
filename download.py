import socket
import sys
import argparse
import os
import urllib
import re

REMOTE_SERVER = "www.google.com"

def is_connected():
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False

def check_connection():
    if is_connected() is False:
        print "\nInternet Connection Required!\n"
        sys.exit(1)

def parse_args():
    parser = argparse.ArgumentParser(
        description = 'Download all the songs of a tv show or a movie.'
    )
    args = parser.parse_args()

def get_music_show(show_name):
    show_page = str(urllib.urlopen("http://www.tunefind.com/show/"+show_name.lower().replace(" ","-")).read())
    //seasons = list(re.findall(r'/season-', show_page))


def get_music(show_name):
    get_music_show(show_name)

def main():
    print "Download all the songs of a tv show or movie.\n"

    while True:
        print "Enter movie/show name :"
        show_name = raw_input('> ')

        directory = os.path.join(show_name)
        if not os.path.exists(directory):
            os.makedirs(directory)

        get_music(show_name)

if __name__ == '__main__':
    check_connection()
    parse_args()
    main()

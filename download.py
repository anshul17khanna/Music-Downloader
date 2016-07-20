import socket
import sys
import argparse

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

if __name__ == '__main__':
    check_connection()
    parse_args()

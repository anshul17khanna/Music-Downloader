import socket
import sys

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

if __name__ == '__main__':
    check_connection()

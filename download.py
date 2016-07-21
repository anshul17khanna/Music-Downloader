import socket
import sys
import argparse
import os
import urllib2
import re
from bs4 import BeautifulSoup

REMOTE_SERVER = "www.google.com"

hdrs = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'
}

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

url = "http://www.tunefind.com/"

def get_season_songs(season, songs):
    season_link = url + season
    request = urllib2.Request(season_link, headers=hdrs);
    episodes_page = str(urllib2.urlopen(request).read())
    episode_links = list(set(re.findall(season + '/\d+#songs', episodes_page)))
    for episode_link in episode_links:
        request = urllib2.Request(url + episode_link, headers=hdrs);
        songs_page = str(urllib2.urlopen(request).read())
        soup = BeautifulSoup(songs_page, "html.parser")
        for link in soup.findAll('a', attrs={'class': 'SongTitle__link___2OQHD'}):
            songs.add(link.text)

def get_music_show(show_name):
    request = urllib2.Request(url + 'show/' + show_name.lower().replace(" ", "-"), headers=hdrs)
    show_page = str(urllib2.urlopen(request).read())
    seasons = list(set(re.findall(r'show/' + show_name.lower().replace(" ", "-") + r'/season-[0-9]', show_page)))
    seasons.sort()
    songs = set()
    for season in seasons:
        get_season_songs(season, songs)
    songs = list(songs)
    #print songs

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

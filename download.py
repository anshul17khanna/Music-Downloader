# -*- coding: utf-8 -*-
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

def get_movie_songs(show_name, songs):
    movie_link = url + show_name
    request = urllib2.Request(movie_link, headers=hdrs)
    songs_page = str(urllib2.urlopen(request).read())
    soup = BeautifulSoup(songs_page, "html.parser")
    for link in soup.findAll('a', attrs={'class': 'SongTitle__link___2OQHD'}):
        songs.add(link.text)

def get_song_links(songs, query_links):
    for song in songs:
        search_query = song + " soundtrack"
        query_links.append("https://www.youtube.com/results?search_query=" + search_query.replace(" ","+"))

def get_yt_links(query_links, yt_links):
    for each_link in query_links:
        request = urllib2.Request(each_link, headers=hdrs)
        page = str(urllib2.urlopen(request).read())
        link = re.findall(r'data-context-item-id="(.*?)"', page)[0]
        if link != '__video_id__':
            yt_links.append(link)

def download(name, yt_ids):
    for id in yt_ids:
        url = "https://www.youtube.com/watch?v=" + id
        print 'id = ' + id
        curr_dir = os.getcwd()
        os.chdir(name.split('/')[1].title())
        os.system('youtube-dl -x --audio-format mp3 --prefer-ffmpeg %s' % url)
        os.chdir(curr_dir)
        print ''

def get_music_show(show_name):
    request = urllib2.Request(url + show_name, headers=hdrs)
    show_page = str(urllib2.urlopen(request).read())
    seasons = list(set(re.findall(show_name + r'/season-\d+', show_page)))
    seasons.sort()
    songs = set()
    for season in seasons:
        print 'Fetching songs of ' + show_name.split('/')[1] + ' ' + season.split('/')[2] + ' .. '
        get_season_songs(season, songs)
    print ''
    songs = list(songs)
    query_links =[]
    get_song_links(songs, query_links)
    yt_links = []
    get_yt_links(query_links, yt_links)
    download(show_name, yt_links)

def get_music_movie(show_name):
    print 'Fetching songs of ' + show_name.split('/')[1] + ' .. '
    songs = set()
    get_movie_songs(show_name, songs)
    songs = list(songs)
    query_links = []
    get_song_links(songs, query_links)
    yt_links = []
    get_yt_links(query_links, yt_links)
    download(show_name, yt_links)

def get_music(show_name):
    if show_name.split('/')[0] == 'show':
        get_music_show(show_name)
    elif show_name.split('/')[0] == 'movie':
        get_music_movie(show_name)

def main():
    print "Download songs of a tv show or a movie.\n"

    while True:
        print "Search Movie / Show : (Ctrl+z to exit)"
        show_name = raw_input('\n> ')
        print ''

        if show_name is '':
            print "Some Recommendations :\n"
        else:
            print "Search Results :\n"

        index = int(1)
        flag = int(0)
        search_results = []
        num_songs = []
        request = urllib2.Request(url + "search/site?q=" + show_name.replace(" ", "+"), headers=hdrs);
        search_page = str(urllib2.urlopen(request).read())
        soup = BeautifulSoup(search_page, "html.parser")
        for div in soup.findAll('div', attrs={'class': 'tf-search-results'}):
            for link in div.findAll('a'):
                search_results.append(link['href'].replace('/', '', 1))
                index += 1

            index = int(1)
            for songs in div.findAll('p'):
                num_songs.append(songs.get_text())
                index += 1

            index = int(1)
            for i in range(len(search_results)):
                if search_results[i].split('/')[0] == 'artist':
                    index -= 1
                elif search_results[i].split('/')[0] != 'artist':
                    flag = 1
                    print search_results[i].replace('', str(index) + '. ', 1).replace('/', ' => ', 1) + ' => ' + num_songs[i]
                index += 1

        if flag == 0:
            index = 1
        if index == 1:
            print "No Results Found! Search again!\n"
            continue
        if index == 2:
            show_name = search_results[0]
            flag = raw_input('Download? (y/n) : ')
            if flag.lower() != 'y':
                print ''
                continue
        else:
            print '\nEnter your choice (int) :'
            inp = int(raw_input('\n> '))
            if inp >= index:
                print 'Out of range!\n'
                continue
            else:
                show_name = search_results[inp-1]

        directory = os.path.join(show_name.split('/')[1].title())
        if not os.path.exists(directory):
            os.makedirs(directory)

        get_music(show_name)

if __name__ == '__main__':
    check_connection()
    parse_args()
    main()

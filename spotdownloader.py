from dbm.dumb import error
import pypresence
from youtube_search import YoutubeSearch
import os
import pyfiglet
import termcolor
import subprocess
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, _make_authorization_headers
from pypresence import Presence
import time

song_list = []

x = 0 

class DownloadError(Exception):
    """Raised when song download bad :("""

class InvalidPlaylistLink(Exception):
    """Invalid Playlist Link"""

def song_download(songig, directory):
    try:
        result = YoutubeSearch(songig, max_results=1).to_dict()
        song_name = result[0]['title']
        global x
        x += 1  

        url_suffix = result[0]['url_suffix']
        url = "https://youtube.com"+url_suffix
        subprocess.check_output(f'youtube-dl --extract-audio --audio-format mp3 --output "{directory}\%(title)s.%(ext)s" {url}', shell=True)
        
        return songig

    except:
        raise DownloadError("Unable to Download song due to an error")
        

def main(i, results):
    track_name = results['items'][i-1]['track']['name']
    artist_name = results['items'][i-1]['track']['album']['artists'][0]['name']

    search = track_name + '-' + artist_name
    song_list.append(search)


def playlist_id(playlistlink):
    playlistt = []

    playlist_id = ''
    i = 1
    weird_var = 0

    for id in playlistlink:
        playlistt.append(id)

    try:
        for idx in range(34,56):
            id_char = playlistt[idx]
            playlist_id = playlist_id + id_char
    
        return playlist_id

    except IndexError:
        raise InvalidPlaylistLink("The playlist link you provided was invalid")

def playlist_song_extraction(playlistid):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="76044f4b24a648e5848964092830c3e8",client_secret="eb50098885f84b73aa3fc5b469c82ae6"))
    i = 1
    results = sp.playlist_tracks(playlistid)
    for x in range(1, results['total']+1):
        try:
            main(i, results)
            i = i+1
        
        except  IndexError:
            i = 1
            results = sp.next(results)
            main(i, results)
            i = i+1
        
    return song_list
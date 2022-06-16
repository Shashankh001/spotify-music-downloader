from threading import Thread
from kivy.lang import Builder
from kivy.uix.screenmanager import *
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.graphics import Rectangle
from kivy.uix.image import Image
from kivymd.uix.spinner import MDSpinner
from tkinter import filedialog
import tkinter
import spotdownloader
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


kv_string = """
#:kivy 2.1.0

#:import WipeTransition kivy.uix.screenmanager.WipeTransition
#:import C kivy.utils.get_color_from_hex


WindowManager:
    transition: WipeTransition()
    Loader:
    Menu
    Song:
    Playlist:
    LoaderSong:
    LoaderPlaylist:

<Loader>:
    name: 'Splash'


<Menu>:
    name: 'menu'

    MDFillRoundFlatButton:
        text: 'Download a song'
        pos_hint: {'center_x': 0.5, 'center_y': 0.55}
        font_size: 18
        md_bg_color: [1,1,1,1]
        on_release: root.song()

    MDFillRoundFlatButton:
        text: 'Download a playlist'
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        font_size: 18
        md_bg_color: [1,1,1,1]
        on_release: root.playlist()



<Song>:
    name: 'song'

    MDFillRoundFlatButton:
        id: back
        text: 'Back'
        pos_hint: {'center_x': 0.96, 'center_y': .96}
        font_size: 15
        md_bg_color: [1,1,1,1]
        on_release: root.back()

    MDLabel:
        text: "Enter a song name:"
        theme_text_color: "Custom"
        text_color: 120/255, 120/255, 120/255, 1
        font_size: 18
        pos_hint: {'center_y': .8}

    MDLabel:
        text: "Note: The song name must be specified properly. That is, it should consist song name, artist/album etc."
        theme_text_color: "Custom"
        text_color: 120/255, 120/255, 120/255, 1
        font_size: 12
        pos_hint: {'center_x':0.5,'center_y': .7}

    MDTextField:
        hint_text: "Song Name"
        mode: "fill"
        fill_color: 0, 0, 0, .4
        icon_left: "music"
        id: song_name
        text: 'Light Switch - Charlie Puth'
        pos_hint: {'center_x':0.5,'center_y': .8}
        size_hint_x: 0.6
        
    MDFillRoundFlatButton:
        id: xd
        text: 'Click to Specify File Location'
        pos_hint: {'center_x': 0.5, 'center_y': .5}
        font_size: 18
        on_press: root.loc_thread()

    MDFillRoundFlatIconButton:
        id: downloadd
        icon: "download"
        text: 'Download Song'
        pos_hint: {'center_x': 0.5, 'center_y': .4}
        font_size: 18
        on_release: root.thread_down()


<Playlist>:
    name: 'playlist'
    
    MDFillRoundFlatButton:
        id: back
        text: 'Back'
        pos_hint: {'center_x': 0.96, 'center_y': .96}
        font_size: 15
        md_bg_color: [1,1,1,1]
        on_release: root.back()

    MDLabel:
        text: "Enter playlist link:"
        theme_text_color: "Custom"
        text_color: 120/255, 120/255, 120/255, 1
        font_size: 18
        pos_hint: {'center_y': .8}

    MDTextField:
        hint_text: "Playlist Link"
        mode: "fill"
        fill_color: 0, 0, 0, .4
        icon_left: "music"
        id: playlist_link
        text: 'https://open.spotify.com/track/...'
        pos_hint: {'center_x':0.5,'center_y': .8}
        size_hint_x: 0.6

    MDFillRoundFlatButton:
        id: xd
        text: 'Click to Specify File Location'
        pos_hint: {'center_x': 0.5, 'center_y': .5}
        font_size: 18
        on_release: root.loc_thread()

    MDFillRoundFlatIconButton:
        id: downloadd
        icon: "download"
        text: 'Download Playlist'
        pos_hint: {'center_x': 0.5, 'center_y': .4}
        font_size: 18
        on_release: root.thread_down()

<LoaderSong>:
    name: 'loader_song'
    Label:
        text: "Downloading your song! This might take a while"
        font_size: 30
        bold: True
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    
    Label:
        text: "You will be redirected to the main menu after the download is finished"
        font_size: 15
        pos_hint: {'center_x': 0.5, 'center_y': .45}

    MDSpinner:
        pos_hint: {'center_x': 0.5, 'center_y': .5}
        size: (50,50)


<LoaderPlaylist>:
    name: 'loader_playlist'

    Label:
        id: loader_playlist_label
        text: "Downloading your playlist! This may take several minutes!"
        font_size: 30
        bold: True
        pos_hint: {'center_x': 0.5, 'center_y': .5}

    Label:
        text: "You will be redirected to the main menu after the download is finished"
        font_size: 15
        pos_hint: {'center_x': 0.5, 'center_y': .45}

    MDSpinner:
        pos_hint: {'center_x': 0.5, 'center_y': .5}
        size: (50,50)
"""




class Loader(Screen):
    """This class will show the splash screen"""
    def on_enter(self, *args):
        Clock.schedule_once(self.switch_to_home, 5)
        image = Image(
            size = (50,50),
            source = 'banner2.png',
            pos_hint= {'center_x': 0.5, 'center_y': 0.7}
        )

        spinner = MDSpinner(
            size_hint = (None,None),
            size= (46,46),
            pos_hint = {'center_x': .5, 'center_y': .4}
        )

        self.add_widget(image)
        self.add_widget(spinner)

    def switch_to_home(self, dt):
        self.manager.current = 'menu'

#self.screen.ids.text_field_error.error = True

class Menu(Screen):
    def on_enter(self, *args):
        image = Rectangle(
            source = 'banner3.png',
            pos_hint= {'center_x': 0.5, 'center_y': 0.5},
            size = self.size,
            allow_stretch = True
        )

        logo = Rectangle(
            source = 'spotify_black2.png',
            size = (100,100)
        )

        
        self.canvas.before.add(image)
        self.canvas.before.add(logo)

        return super().on_enter(*args)
        
        
    def song(self):
        SpotifySongsDownloader.build.kv.current = 'song'

    def playlist(self):
        SpotifySongsDownloader.build.kv.current = 'playlist'

class Song(Screen):
    def on_enter(self, *args):
        logo = Image(
            source = 'small_logo2.png',
            size = (50,50),
            pos_hint = {'center_x': 0.03, 'center_y': .96}
        )

        self.add_widget(logo)

        return super().on_enter(*args)

    def back(self):
        SpotifySongsDownloader.build.kv.current = 'menu'
        SpotifySongsDownloader.build.kv.direction = 'left'
        self.ids.song_name.text = 'Light Switch - Charlie Puth'

    def loc_thread(self):
        self.ids.back.disabled = True
        self.ids.xd.disabled = True
        self.ids.downloadd.disabled = True
        t = Thread(target=self.location)
        t.daemon = True
        t.start()

    def location(self):
        root = tkinter.Tk()
        root.withdraw()
        Song.location.loc = filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
        
        if Song.location.loc == '':
            self.ids.xd.text = 'Click to Specify File Location'
            self.ids.xd.disabled = False
            self.ids.downloadd.disabled = False
            self.ids.back.disabled = False
            return

        self.ids.xd.text = Song.location.loc
        self.ids.xd.disabled = False
        self.ids.downloadd.disabled = False
        self.ids.back.disabled = False

    def thread_down(self):
        Song.thread_down.t = Thread(target=self.download)
        Song.thread_down.t.daemon = True
        Song.thread_down.t.start()

    def go_back(self, dt):
        SpotifySongsDownloader.build.kv.current = 'menu'
        SpotifySongsDownloader.build.kv.direction = 'left'

    def loader(self, dt):
        SpotifySongsDownloader.build.kv.current = 'loader_song'
        SpotifySongsDownloader.build.kv.direction = 'right'
    
    def invaliddirectory(self, dt):
        dialog = MDDialog(
                text="Invalid Directory")
        dialog.open()

    
    def download(self):
        try:
            directory = Song.location.loc
            song = self.ids.song_name.text

            if directory == '':
                Clock.schedule_once(self.invaliddirectory, 0)
                return

            Clock.schedule_once(self.loader, 0)
            spotdownloader.song_download(song, directory)
            Clock.schedule_once(self.go_back, 1)
        except AttributeError:
            Clock.schedule_once(self.invaliddirectory, 0)
            return


class Playlist(Screen):
    def on_enter(self, *args):
        logo = Image(
            source = 'small_logo2.png',
            size = (50,50),
            pos_hint = {'center_x': 0.03, 'center_y': .96}
        )

        self.add_widget(logo)

        return super().on_enter(*args)
        
    def back(self):
        SpotifySongsDownloader.build.kv.current = 'menu'
        SpotifySongsDownloader.build.kv.direction = 'left'
        self.ids.playlist_link.text = 'https://open.spotify.com/track/...'

    def loc_thread(self):
        self.ids.back.disabled = True
        self.ids.xd.disabled = True
        self.ids.downloadd.disabled = True
        t = Thread(target=self.location)
        t.daemon = True
        t.start()

    def location(self):
        root = tkinter.Tk()
        root.withdraw()
        Playlist.location.loc = filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
        
        if Playlist.location.loc == '':
            self.ids.xd.text = 'Click to Specify File Location'
            self.ids.xd.disabled = False
            self.ids.downloadd.disabled = False
            self.ids.back.disabled = False
            return

        self.ids.xd.text = Playlist.location.loc
        self.ids.xd.disabled = False
        self.ids.downloadd.disabled = False
        self.ids.back.disabled = False


    def thread_down(self):
        Playlist.thread_down.t = Thread(target=self.download)
        Playlist.thread_down.t.daemon = True
        Playlist.thread_down.t.start()

    def go_back(self, dt):
        SpotifySongsDownloader.build.kv.current = 'menu'
        SpotifySongsDownloader.build.kv.direction = 'left'
    
    def loader(self, dt):
        SpotifySongsDownloader.build.kv.current = 'loader_playlist'
        SpotifySongsDownloader.build.kv.direction = 'right'
    
    def invalidplaylistlink(self, dt):
        dialog = MDDialog(
                text="Invalid Playlist Link")
        dialog.open()

    def invaliddirectory(self, dt):
        dialog = MDDialog(
                text="Invalid Directory")
        dialog.open()

    def download(self):
        try:
            directory = Playlist.location.loc 
            link = self.ids.playlist_link.text

            if directory == '':
                Clock.schedule_once(self.invaliddirectory, 0)
                return

            try:
                f = spotdownloader.playlist_id(link)
            except spotdownloader.InvalidPlaylistLink:
                    Clock.schedule_once(self.invalidplaylistlink, 0)
                    return
            except spotdownloader.DownloadError:
                    pass

            try:        
                v  = spotdownloader.playlist_song_extraction(f)
            except spotdownloader.InvalidPlaylistLink:
                    Clock.schedule_once(self.invalidplaylistlink, 0)
                    return
            except spotdownloader.DownloadError:
                    pass

            l = []
            

            for i in v:
                Clock.schedule_once(self.loader, 0)
                try:
                    x = spotdownloader.song_download(i, directory)
                except spotdownloader.InvalidPlaylistLink:
                    Clock.schedule_once(self.invalidplaylistlink, 0)
                    return
                except spotdownloader.DownloadError:
                    pass

                if x != True:
                    l.append(i)

                else:
                    continue

        except AttributeError:
            Clock.schedule_once(self.invaliddirectory, 0)
            return

        Clock.schedule_once(self.go_back, 1)
    



class LoaderSong(Screen):
    pass

class LoaderPlaylist(Screen):
    pass

class WindowManager(ScreenManager):
    pass


class SpotifySongsDownloader(MDApp):
    def __init__(self, **kwargs):
        self.title = "Spotify Music Downloader"
        super().__init__(**kwargs)

    def build(self):
        SpotifySongsDownloader.build.kv = Builder.load_string(kv_string)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        self.icon = 'logo.ico'
        return SpotifySongsDownloader.build.kv


if __name__ == '__main__':
    SpotifySongsDownloader().run()


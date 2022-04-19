import PySimpleGUI as sg
import pygame

class Music:

    def __init__(self, path):
        pygame.init()
        pygame.mixer.init()
        self.music = pygame.mixer.music
        self.sound = path
        self.music.load(self.sound)
        self.music.play()

    def volchange(self, volume):
        self.music.set_volume(volume)  # The set_volume range is from 0.00 to 1.00 (every 0.01)
    def isplaying(self):
        return self.music.get_busy()



class Volume:
    def __init__(self, song):
        self.layout = [
            [sg.Slider(key = 'volume', range=(0, 100), 
            orientation='h', size=(20, 15), default_value= 50,
            enable_events = True)]
        ]
        self.song = song
        self.new_volume = self.song.music.get_volume()
        self.window = sg.Window('Help me', self.layout)

    def draw_mixer(self):
        while True:
            event, values = self.window.read()
            if self.song.isplaying():
                value = values['volume']
                self.new_volume = value / 100.0
                self.song.volchange(self.new_volume)
            if event == sg.WIN_CLOSED :
                break
        pygame.event.clear()

song = Music("assets/happy.mp3")

volume = Volume(song)

# volume.draw_mixer()
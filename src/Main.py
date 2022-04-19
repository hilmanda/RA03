import pygame
import PySimpleGUI as PSG

from music import Music, Volume

pygame.init()
pygame.font.init()
pygame.mixer.init()

#music
class Music:
    def __init__(self):
        self.music = pygame.mixer.music
        self.music.load("assets/happy.mp3")
        self.music.set_volume(0.5)
        self.music.play(-1,0.0,3000)
        
    def music_composer(self, *even):
        self.music.set_volume(*even)






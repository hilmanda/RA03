<<<<<<< HEAD
=======

>>>>>>> 530fa1bdfa1f3781a76e715ec4316af1b28a42bd
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
<<<<<<< HEAD
=======

>>>>>>> 530fa1bdfa1f3781a76e715ec4316af1b28a42bd

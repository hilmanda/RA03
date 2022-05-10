import pygame
from src.menu import *
from src.music import *
from src.start import *

WINDOW = WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 800
WHITE = (255, 255, 255)
clock = pygame.time.Clock()
FPS = 60
class Game():
    def __init__(self):
        pygame.init()
        self.song = Music('assets/spongebob.mp3')
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY = self.DISPLAY_W, self.DISPLAY_H = 1200, 800
        self.mainbackground = pygame.image.load('assets/mainbg.jpg').convert()
        self.mainbackground = pygame.transform.scale(self.mainbackground,self.DISPLAY)
        self.display = self.mainbackground.copy()
        self.window = pygame.display.set_mode((self.DISPLAY_W,self.DISPLAY_H))
        # self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        # self.font_name = '8-BIT WONDER.TTF'
        self.font_name = 'assets/fonts/font.ttf'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.difficulty = DifficultyMenu(self)
        self.volume = VolumeMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

    def game_loop(self):
        game = Start()
        while self.playing:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_4:
                        self.playing = False

            game.update(event_list)

            pygame.display.update()
            self.reset_keys()
            clock.tick(FPS)
        

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y, color = WHITE ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)
    
    def clear_text(self):
        self.display = self.mainbackground.copy()
        



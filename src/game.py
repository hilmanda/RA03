import pygame
from src.menu import *
from src.music import *
from src.start import *
from src.start import Start

pygame.display.set_caption("EXIATOMA-RA03")
WINDOW = WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 800
WHITE = (255, 255, 255)
FPS = 60
frame_set = pygame.time.Clock()
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
        self.font_name = 'assets/fonts/font.ttf'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.difficulty_menu = DifficultyMenu(self)
        self.volume = VolumeMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        self.difficulty = 1
        self.game = Start(self.difficulty)
        self.gameOver = False
        self.time = 4

    def game_loop(self):
        self.game = Start(self.difficulty)
        self.game.set_timer((self.time + self.difficulty) * 60)
        while self.playing and self.game.time:
            frame_set.tick(FPS)
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_BACKSPACE :
                        self.playing = False
                    if event.key == pygame.K_ESCAPE:
                        self.gameOver = True

            if not self.playing or not self.game.time:
                self.game_over()
            else:
                self.game.update(event_list)

            pygame.mixer.music.unpause()
            pygame.display.update()
            self.reset_keys()

    def game_over(self):
        pygame.mixer.music.pause()
        self.game.game_over_sound.play()
        self.run_display = True
        while self.run_display:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.playing = True
                        self.run_display = False
                    if event.key == pygame.K_BACKSPACE:
                        self.run_display = False
            

            game_over_images = pygame.image .load("assets/images/gameOver.png")
            game_over_images = pygame.transform.scale(game_over_images, (WINDOW_WIDTH, WINDOW_HEIGHT))
            game_over_rect = game_over_images.get_rect(topleft = (0,0))

            content_font = pygame.font.Font('assets/fonts/font.ttf', 30)
            
            quit_text = content_font.render('Backspace to QUIT!', True, RED)
            quit_rect = quit_text.get_rect(midtop=(self.DISPLAY_W //2, self.DISPLAY_H //2 +20))
            restart_text = content_font.render('Enter to Play Again', True, WHITE)
            restart_rect = restart_text.get_rect(midtop=(self.DISPLAY_W //2, self.DISPLAY_H//2 +70))
            
            self.window.blit(game_over_images, game_over_rect)
            self.window.blit(quit_text, quit_rect)
            self.window.blit(restart_text, restart_rect)
            
            pygame.display.update()

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
                    self.game.btn_click.play()
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.game.btn_click.play()
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
        



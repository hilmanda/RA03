import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from src.music import *


class Menu():
    def __init__(self, game):
        self.GREEN = (0,128,0)
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offsetx = - 100
        self.offsety = 10

    def draw_cursor(self, text):
        self.game.draw_text(text, 49, self.cursor_rect[0], self.cursor_rect[1], self.GREEN)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h
        self.difficultx, self.difficulty = self.mid_w, self.mid_h +50
        self.volumex, self.volumey = self.mid_w, self.mid_h + 100
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 150
        self.cursor_rect = (self.startx, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.clear_text()
            self.game.check_events()
            self.check_input()
            self.game.draw_text('Main Menu', 80, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 4)
            self.game.draw_text("Start", 50, self.startx, self.starty)
            self.game.draw_text("Difficulty", 50, self.difficultx, self.difficulty)
            self.game.draw_text("Volume", 50, self.volumex, self.volumey)
            self.game.draw_text("Credits", 50, self.creditsx, self.creditsy)
            self.draw_cursor(self.state)
            self.blit_screen()
        self.game.clear_text()


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect = (self.difficultx , self.difficulty)
                self.state = 'Difficulty'
            elif self.state == 'Difficulty':
                self.cursor_rect = (self.volumex , self.volumey)
                self.state = 'Volume'
            elif self.state == 'Volume':
                self.cursor_rect = (self.creditsx , self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect = (self.startx , self.starty)
                self.state = 'Start'
                
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect = (self.creditsx , self.creditsy)
                self.state = 'Credits'
            if self.state == 'Difficulty':
                self.cursor_rect = (self.startx , self.starty)
                self.state = 'Start'
            elif self.state == 'Volume':
                self.cursor_rect = (self.difficultx , self.difficulty)
                self.state = 'Difficulty'
            elif self.state == 'Credits':
                self.cursor_rect = (self.volumex , self.volumey)
                self.state = 'Volume'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Difficulty':
                self.game.curr_menu =self.game.difficulty
            elif self.state == 'Volume':
                self.game.curr_menu = self.game.volume
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False

class DifficultyMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Difficulty'
        self.difficulty = 1
    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.clear_text()
            self.game.draw_text('Credits', 70, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 4)
            self.game.draw_text('AUTHOR :', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 5 + 110, '#000000')
            self.game.draw_text('120140050, 120140131, 120140141, 120140147, 120140153, 120140199', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 5 + 150)
            self.game.draw_text('SONG :', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 5 + 200, '#000000')
            self.game.draw_text('OST SPONGEBOB SQUAREPANTS', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 5 + 240)
            self.game.draw_text('IMAGES :', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 5 + 290, '#000000')
            self.game.draw_text('Vecteezy.com', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 5 + 340)
            self.game.draw_text('wallpaperaccess.com', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 5 + 370)
            
            self.blit_screen()
        self.game.clear_text()


class VolumeMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect = (self.volx, self.voly)
        self.slider = Slider(self.game.window, int(self.volx) - 100, int(self.voly), 200, 10, min=0, max=50, step=1,handleColour = (255,0,0), initial = 50)

    def slider_update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False

        pygame_widgets.update(events)
        

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.clear_text()
            self.game.check_events()
            self.check_input()
            self.slider_update()
            pygame.display.update()
            self.new_volume = self.slider.getValue() / 100.0
            self.game.song.volchange(self.new_volume)
            self.game.draw_text('Set Volume', 50, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 4)
            self.game.window.blit(self.game.display, (0, 0))
            self.game.reset_keys()
        self.game.clear_text()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.clear_text()
            self.game.draw_text('Credits', 70, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 4)
            self.game.draw_text('AUTHOR :', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 5 + 110, '#000000')
            self.game.draw_text('120140050, 120140131, 120140141, 120140147, 120140153, 120140199', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 5 + 150)
            self.game.draw_text('SONG :', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 5 + 200, '#000000')
            self.game.draw_text('OST SPONGEBOB SQUAREPANTS', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 5 + 240)
            self.game.draw_text('IMAGES :', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 5 + 290, '#000000')
            self.game.draw_text('Vecteezy.com', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 5 + 340)
            self.game.draw_text('wallpaperaccess.com', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 5 + 370)
            
            self.blit_screen()
        self.game.clear_text()
        

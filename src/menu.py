import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from src.music import *


class Menu():
    def __init__(self, game):
        self.BROWN = (0,128,0)
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 3
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offsetx = - 100
        self.offsety = 10

    def draw_cursor(self, text):
        self.game.draw_text(text, 39, self.cursor_rect[0], self.cursor_rect[1], self.BROWN)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h
        self.difx, self.dify = self.mid_w, self.mid_h + 50
        self.volumex, self.volumey = self.mid_w, self.mid_h + 100
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 150
        self.cursor_rect = (self.startx, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            # self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Main Menu', 80, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 5)
            self.game.draw_text("Start", 40, self.startx, self.starty)
            self.game.draw_text("Difficulty", 40, self.difx, self.dify)
            self.game.draw_text("Volume", 40, self.volumex, self.volumey)
            self.game.draw_text("Credits", 40, self.creditsx, self.creditsy)
            self.draw_cursor(self.state)
            self.blit_screen()
        # self.game.clear_text()


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect = (self.difx, self.dify)
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
            elif self.state == 'Difficulty':
                self.cursor_rect = (self.startx , self.starty)
                self.state = 'Start'
            elif self.state == 'Volume':
                self.cursor_rect = (self.difx , self.dify)
                self.state = 'Difficulty'
            elif self.state == 'Credits':
                self.cursor_rect = (self.volumex , self.volumey)
                self.state = 'Volume'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Volume':
                self.game.curr_menu = self.game.volume
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False

class DifficultyMenu(Menu):
    pass

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
            self.game.draw_text('Set Volume', 50, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 5)
            self.game.window.blit(self.game.display, (0, 0))
            self.game.reset_keys()
        self.game.clear_text()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        # elif self.game.UP_KEY or self.game.DOWN_KEY:
        #     if self.state == 'Volume':
        #         self.state = 'Controls'
        #         self.cursor_rect.midtop = (self.controlsx + self.offsetx, self.controlsy)
        #     elif self.state == 'Controls':
        #         self.state = 'Volume'
        #         self.cursor_rect.midtop = (self.volx + self.offsetx, self.voly)
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
            # self.game.display.fill(self.game.BLACK)
            self.game.clear_text()
            self.game.draw_text('Credits', 50, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Made by me', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 20)
            self.blit_screen()
        self.game.clear_text()
        
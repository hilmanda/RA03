from asyncio import events
import pygame
from src.music import *
import pygame_widgets
from pygame_widgets.slider import Slider


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.volumex, self.volumey = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Main Menu', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Volume Setting", 20, self.volumex, self.volumey)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.volumex + self.offset, self.volumey)
                self.state = 'Volume'
            elif self.state == 'Volume':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Volume':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.volumex + self.offset, self.volumey)
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

class VolumeMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
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
        pygame.display.update()

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Set Volume', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            # self.game.draw_text("Volume", 15, self.volx, self.voly)
            # self.game.draw_text("Controls", 15, self.controlsx, self.controlsy)
            self.game.check_events()
            self.check_input()
            # self.blit_screen()
            self.slider_update()
            self.new_volume = self.slider.getValue() / 100.0
            self.game.song.volchange(self.new_volume)
            self.game.window.blit(self.game.display, (0, 0))
            self.game.reset_keys()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        # elif self.game.UP_KEY or self.game.DOWN_KEY:
        #     if self.state == 'Volume':
        #         self.state = 'Controls'
        #         self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
        #     elif self.state == 'Controls':
        #         self.state = 'Volume'
        #         self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
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
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Made by me', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.blit_screen()
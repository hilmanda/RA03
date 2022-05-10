import pygame
import cv2
import os
import random
from src.menu import *
from src.music import *
from src.game import *
from src.tile import *

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
FPS = 60
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

class Start():
    def __init__(self):
        self.level = 1
        self.level_complete = False

        # food
        self.all_food = [f for f in os.listdir('assets/cards/') if os.path.join('assets/cards/', f)]

        self.img_width, self.img_height = (128, 128)
        self.padding = 20
        self.margin_top = 160
        self.cols = 4
        self.rows = 2
        self.width = WINDOW_WIDTH

        self.tiles_group = pygame.sprite.Group()

        # flipping & timing
        self.flipped = []
        self.frame_count = 0
        self.block_game = False

        # generate first level
        self.generate_level(self.level)

        # initialize video
        self.is_video_playing = True
        self.play = pygame.image.load('assets/images/play2.png').convert_alpha()
        self.stop = pygame.image.load('assets/images/pause2.png').convert_alpha()
        self.video_toggle = self.play
        self.video_toggle_rect = self.video_toggle.get_rect(topright=(WINDOW_WIDTH - 50, 10))
        self.get_video()

        # initialize music
        self.is_music_playing = True
        self.sound_on = pygame.image.load('assets/images/sound2.png').convert_alpha()
        self.sound_off = pygame.image.load('assets/images/mute2.png').convert_alpha()
        self.music_toggle = self.sound_on
        self.music_toggle_rect = self.music_toggle.get_rect(topright=(WINDOW_WIDTH - -1, 10))

        # load music
        # pygame.mixer.music.load('assets/spongebob.mp3')
        # pygame.mixer.music.set_volume(.3)
        # pygame.mixer.music.play()

    def update(self, event_list):
        # if self.is_video_playing:
        #     self.success, self.img = self.cap.read()
        self.user_input(event_list)
        self.draw()
        self.check_level_complete(event_list)

    def check_level_complete(self, event_list):
        if not self.block_game:
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for tile in self.tiles_group:
                        if tile.rect.collidepoint(event.pos):
                            self.flipped.append(tile.name)
                            tile.show()
                            if len(self.flipped) == 2:
                                if self.flipped[0] != self.flipped[1]:
                                    self.block_game = True
                                else:
                                    self.flipped = []
                                    for tile in self.tiles_group:
                                        if tile.shown:
                                            self.level_complete = True
                                        else:
                                            self.level_complete = False
                                            break
        else:
            self.frame_count += 1
            if self.frame_count == FPS:
                self.frame_count = 0
                self.block_game = False

                for tile in self.tiles_group:
                    if tile.name in self.flipped:
                        tile.hide()
                self.flipped = []

    def generate_level(self, level):
        self.food = self.select_random_food(self.level)
        self.level_complete = False
        self.rows = self.level + 1
        self.cols = 4
        self.generate_tileset(self.food)

    def generate_tileset(self, food):
        self.cols = self.rows = self.cols if self.cols >= self.rows else self.rows

        TILES_WIDTH = (self.img_width * self.cols + self.padding * 3)
        LEFT_MARGIN = RIGHT_MARGIN = (self.width - TILES_WIDTH) // 2
        # tiles = []
        self.tiles_group.empty()

        for i in range(len(food)):
            x = LEFT_MARGIN + ((self.img_width + self.padding) * (i % self.cols))
            y = self.margin_top + (i // self.rows * (self.img_height + self.padding))
            tile = Tile(food[i], x, y)
            self.tiles_group.add(tile)

    def select_random_food(self, level):
        food = random.sample(self.all_food, (self.level + self.level + 2))
        food_copy = food.copy()
        food.extend(food_copy)
        random.shuffle(food)
        return food

    def user_input(self, event_list):
        # video toggle
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.music_toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.is_music_playing:
                        self.is_music_playing = False
                        self.music_toggle = self.sound_off
                        pygame.mixer.music.pause()
                    else:
                        self.is_music_playing = True
                        self.music_toggle = self.sound_on
                        pygame.mixer.music.unpause()
                if self.video_toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.is_video_playing:
                        self.is_video_playing = False
                        self.video_toggle = self.stop
                    else:
                        self.is_video_playing = True
                        self.video_toggle = self.play

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.level_complete:
                    self.level += 1
                    if self.level >=3:
                        self.level = 1
                    self.generate_level(self.level)

    def draw(self):
        screen.fill(BLACK)

        # fonts
        title_font = pygame.font.Font('assets/fonts/font.ttf', 44)
        content_font = pygame.font.Font('assets/fonts/font.ttf', 24)

        # text
        title_text = title_font.render('Memory Game', True, WHITE)
        title_rect = title_text.get_rect(midtop=(WINDOW_WIDTH // 2, 10))

        level_text = content_font.render('Level ' + str(self.level), True, WHITE)
        level_rect = level_text.get_rect(midtop=(WINDOW_WIDTH // 2, 80))

        info_text = content_font.render('Temukan Pasangan Gambar yang Sama', True, WHITE)
        info_rect = info_text.get_rect(midtop=(WINDOW_WIDTH // 2, 120))

        if self.is_video_playing:
            if self.success:
                screen.blit(pygame.image.frombuffer(self.img.tobytes(), self.shape, 'BGR'), (0, 120))
            else:
                self.get_video()
        else:
            screen.blit(pygame.image.frombuffer(self.img.tobytes(), self.shape, 'BGR'), (0, 120))

        if self.level < 3:
            next_text = content_font.render('Tekan Spasi untuk level selanjutnya!', True, WHITE)
        else:
            next_text = content_font.render('Selamat kamu menang!!! Tekan spasi untuk memulai lagi', True, WHITE)
        next_rect = next_text.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))

        screen.blit(title_text, title_rect)
        screen.blit(level_text, level_rect)
        screen.blit(info_text, info_rect)
        pygame.draw.rect(screen, BLACK, (WINDOW_WIDTH - 110, 0, 130, 70))
        screen.blit(self.video_toggle, self.video_toggle_rect)
        screen.blit(self.music_toggle, self.music_toggle_rect)

        # draw tileset
        self.tiles_group.draw(screen)
        self.tiles_group.update()

        if self.level_complete:
            screen.blit(next_text, next_rect)

    def get_video(self):
        self.img = cv2.imread('assets/images/playbg.jpeg')
        self.img = cv2.resize(self.img,dsize=(WINDOW_WIDTH,WINDOW_HEIGHT-110))
        self.success = True
        self.shape = self.img.shape[1::-1]
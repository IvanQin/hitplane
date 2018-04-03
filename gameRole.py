# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:36:03 2013

@author: Leo
"""

import pygame

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

TYPE_SMALL = 1
TYPE_MIDDLE = 2
TYPE_BIG = 3


# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed


# 玩家类
class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []  # 用来存储玩家对象精灵图片的列表
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.rect = player_rect[0]  # 初始化图片所在的矩形
        self.rect.topleft = init_pos  # 初始化矩形的左上角坐标
        self.speed = 8  # 初始化玩家速度，这里是一个确定的值
        self.bullets = pygame.sprite.Group()  # 玩家飞机所发射的子弹的集合
        self.img_index = 0  # 玩家精灵图片索引
        self.is_hit = False  # 玩家是否被击中

    # 发射子弹
    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    # 向上移动
    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    # 向下移动
    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    # 向左移动，判断边界
    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    # 向右移动，判断边界
    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed


# 敌人类
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 2
        self.down_index = 0

    # 敌人移动，判断边界，在主循环中删除处理
    def move(self):
        self.rect.top += self.speed


class Button:
    def __init__(self, text, pos, font_size):
        self.pos = pos
        user_font = pygame.font.Font(None, font_size)
        self.render_text = user_font.render(str(text), True, (128, 128, 128))
        self.rect = self.render_text.get_rect()
        self.rect.center = pos

    def render(self, screen):
        screen.blit(self.render_text, self.rect)

    def is_clicked(self):
        x, y = pygame.mouse.get_pos()
        w, h = self.rect.width, self.rect.height
        in_button_x = self.pos[0] - w / 2 < x < self.pos[0] + w / 2
        in_button_y = self.pos[1] - h / 2 < y < self.pos[1] + h / 2
        return in_button_x and in_button_y

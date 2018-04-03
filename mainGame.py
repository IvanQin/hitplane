# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:05:00 2013

@author: Leo
"""

import pygame
from sys import exit
from pygame.locals import *
from gameRole import *
import random
from setting import *


def init():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # 载入背景图
    background = pygame.image.load('resources/image/background.png').convert()
    screen.fill(0)
    screen.blit(background, (0, 0))
    easy_level_btn = Button("EASY", (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), 36)
    medium_level_btn = Button("MEDIUM", (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 36), 36)
    hard_level_btn = Button("HARD", (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 72), 36)
    easy_level_btn.render(screen)
    medium_level_btn.render(screen)
    hard_level_btn.render(screen)

    game_level = None
    is_waiting = True
    while is_waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                if easy_level_btn.is_clicked():
                    game_level = EasyLevel
                    is_waiting = False
                elif medium_level_btn.is_clicked():
                    game_level = MediumLevel
                    is_waiting = False
                elif hard_level_btn.is_clicked():
                    game_level = HardLevel
                    is_waiting = False
        pygame.display.update()

    return game_level


def run(level):
    # 初始化游戏
    pygame.init()
    # 设置游戏界面大小，背景和标题
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('飞机大战')

    # 载入游戏音乐
    bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
    enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
    game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
    bullet_sound.set_volume(0.3)
    enemy1_down_sound.set_volume(0.3)
    game_over_sound.set_volume(0.3)

    # 载入背景图
    background = pygame.image.load('resources/image/background.png').convert()
    # 游戏结束背景图
    game_over = pygame.image.load('resources/image/gameover.png')

    # 飞机，子弹素材图片
    filename = 'resources/image/shoot.png'
    plane_img = pygame.image.load(filename)

    # 设置玩家相关参数
    player_rect = []
    player_rect.append(pygame.Rect(0, 99, 102, 126))  # 玩家飞机图片
    player_rect.append(pygame.Rect(165, 360, 102, 126))
    player_rect.append(pygame.Rect(165, 234, 102, 126))  # 飞机爆炸图片
    player_rect.append(pygame.Rect(330, 624, 102, 126))
    player_rect.append(pygame.Rect(330, 498, 102, 126))
    player_rect.append(pygame.Rect(432, 624, 102, 126))
    player_pos = [200, 600]
    player = Player(plane_img, player_rect, player_pos)

    # 子弹图片
    bullet_rect = pygame.Rect(1004, 987, 9, 21)
    bullet_img = plane_img.subsurface(bullet_rect)

    # 敌人不同状态的图片列表，多张连续显示动画
    enemy1_rect = pygame.Rect(534, 612, 57, 43)
    enemy1_img = plane_img.subsurface(enemy1_rect)
    enemy1_down_imgs = []
    enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
    enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
    enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
    enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

    enemies1 = pygame.sprite.Group()

    # 存储被击毁的飞机，用来渲染击毁动画
    enemies_down = pygame.sprite.Group()

    # 初始化射击以及敌人的移动频率
    shoot_frequency = 0
    enemy_frequency = 0

    # 玩家飞机被击中后的效果
    player_down_index = 16

    # 初始化分数
    score = 0

    # 游戏循环帧率设置
    clock = pygame.time.Clock()

    # 判断游戏循环退出参数
    running = True

    # 主循环
    while running:
        # 控制游戏最大帧率为60
        clock.tick(60)

        # 生成子弹，控制子弹发射频率，先判断飞机没被击中
        if not player.is_hit:
            if shoot_frequency % level.SHOOT_INTERVAL == 0:
                bullet_sound.play()
                player.shoot(bullet_img)
            shoot_frequency += 1
            if shoot_frequency >= level.SHOOT_INTERVAL:
                shoot_frequency = 0

        # 生成敌机，控制生成频率
        if enemy_frequency % level.ENEMY_INTERVAL == 0:
            enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
            enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
            enemies1.add(enemy1)
        enemy_frequency += 1
        if enemy_frequency >= 100:
            enemy_frequency = 0

        # 移动子弹
        for bullet in player.bullets:
            bullet.move()
            # 超出窗口范围则删除
            if bullet.rect.bottom < 0:
                player.bullets.remove(bullet)

        # 移动敌机
        for enemy in enemies1:
            enemy.move()
            # 判断玩家是否被击中，碰撞效果处理
            if pygame.sprite.collide_circle(enemy, player):
                enemies_down.add(enemy)
                enemies1.remove(enemy)
                player.is_hit = True
                game_over_sound.play()
                break
            # 敌机超出窗口范围则删除
            if enemy.rect.top > SCREEN_HEIGHT:
                enemies1.remove(enemy)

        # 敌机被子弹击中效果
        # 将被击中的敌机对象添加到击毁敌机Group中，用来渲染击毁动画
        enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
        for enemy_down in enemies1_down:
            enemies_down.add(enemy_down)

        # 绘制背景
        screen.fill(0)
        screen.blit(background, (0, 0))

        # 绘制玩家飞机
        if not player.is_hit:
            screen.blit(player.image[player.img_index], player.rect)
            # 更换图片索引使飞机有动画效果
            player.img_index = shoot_frequency // ((level.SHOOT_INTERVAL + 1) / 2)
        else:
            # 玩家飞机被击中后效果
            player.img_index = player_down_index // 8
            screen.blit(player.image[player.img_index], player.rect)
            player_down_index += 1
            if player_down_index > 47:
                # 击中后游戏结束
                running = False

        # 敌机被子弹击中效果显示
        for enemy_down in enemies_down:
            if enemy_down.down_index == 0:
                enemy1_down_sound.play()
            if enemy_down.down_index > 7:
                enemies_down.remove(enemy_down)
                score += 1000
                continue
            screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
            enemy_down.down_index += 1

        # 显示子弹
        player.bullets.draw(screen)
        # 显示敌机
        enemies1.draw(screen)

        # 绘制得分
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(str(score), True, (128, 128, 128))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]
        screen.blit(score_text, text_rect)

        user_font = pygame.font.Font(None, 36)
        user_text = user_font.render(str("Jack"), True, (128, 128, 128))
        user_rect = user_text.get_rect()
        user_rect.topright = [SCREEN_WIDTH - 10, 10]
        screen.blit(user_text, user_rect)

        # 更新屏幕
        pygame.display.update()

        # 处理游戏退出
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # 获取上下左右按键操作
        key_pressed = pygame.key.get_pressed()
        # 反映键盘操作在屏幕上
        if not player.is_hit:
            if key_pressed[K_w] or key_pressed[K_UP]:
                player.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                player.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                player.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                player.moveRight()

    # 游戏结束后显示最终得分
    font = pygame.font.Font(None, 48)
    text = font.render('Score: ' + str(score), True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 24
    screen.blit(game_over, (0, 0))
    screen.blit(text, text_rect)

    # 显示得分并处理游戏结束
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.update()


if __name__ == '__main__':
    level = init()
    run(level)

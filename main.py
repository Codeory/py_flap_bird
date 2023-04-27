#
# https://itsourcecode.com/free-projects/pygame/how-to-make-flappy-bird-in-python/
#

import pygame
from pygame.locals import *
import random
import time
import sys

from bird import Bird

FPS = 32
scr_width = 290
scr_height = 520
display_screen_window = pygame.display.set_mode((scr_width, scr_height))
play_ground = scr_height * 0.8
game_image = {}
game_audio_sound = {}
player = 'images/bird.png'
bcg_image = 'images/background.png'
pipe_image = 'images/pipe.png'


def main_screen():
    """
        游戏主界面
    """

    player_start_x = int(scr_width / 5)
    player_start_y = int(scr_width / 2)

    base_start_x = 0

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                """
                    如果是 escape 事件，直接退出
                """
                pygame.quit()
                sys.exit(0)

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                """
                    空格键和箭头上 返回到开始游戏界面
                """
                return

            else:

                """
                    显示游戏开始界面 使用 blit 函数进行图片显示，update 函数根据FPS刷新屏幕
                """

                display_screen_window.blit(game_image['background'], (0, 0))
                display_screen_window.blit(game_image['player'], (player_start_x, player_start_y))

                display_screen_window.blit(game_image['base'], (base_start_x, play_ground))

                pygame.display.update()
                time_clock.tick(FPS)


def main_gameplay():
    """
        游戏运行逻辑
    """

    player_posi_x = int(scr_width / 5)
    player_posi_y = int(scr_height / 5)

    bird = Bird(player_posi_x, player_posi_y)

    base_posi = 0

    new_pipe_1 = get_random_pipes()
    new_pipe_2 = get_random_pipes()

    up_pipe = [
        {'x': scr_width + 200, 'y': new_pipe_1[0]['y']},
        {'x': scr_width + 200 + (scr_width / 2), 'y': new_pipe_2[0]['y']}
    ]

    down_pipe = [
        {'x': scr_width + 200, 'y': new_pipe_1[1]['y']},
        {'x': scr_width + 200 + (scr_width / 2), 'y': new_pipe_2[1]['y']}
    ]

    pipe_var_x = -4
    player_is_flap = False

    while True:

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                player_is_flap = True
                game_audio_sound['wing'].play()

        collid_test = is_colliding(bird.get_position_x(), bird.get_position_y(),
                                   up_pipe, down_pipe)

        if collid_test:
            return

        """"
            判断和更新分数
        """

        player_middle_position = bird.get_position_x() + game_image['player'].get_width() / 2
        for pipe in up_pipe:
            pipe_middle_position = pipe['x'] + game_image['pipe'][0].get_width() / 2
            if pipe_middle_position <= player_middle_position < pipe_middle_position + 4:
                bird.inc_score(1)
                game_audio_sound['point'].play()

        player_var_y = bird.flap(player_is_flap)

        if player_is_flap:
            player_is_flap = False
        player_height = game_image['player'].get_height()
        bird.up_position_y(play_ground, player_height, player_var_y)

        """
            更新管道横轴位置，实时向左移动
        """
        for pip_upper, pip_down in zip(up_pipe, down_pipe):
            pip_upper['x'] += pipe_var_x
            pip_down['x'] += pipe_var_x

        if 0 < up_pipe[0]['x'] < 5:
            new_pipe = get_random_pipes()
            up_pipe.append(new_pipe[0])
            down_pipe.append(new_pipe[1])

        if up_pipe[0]['x'] < -game_image['pipe'][0].get_width():
            up_pipe.pop(0)
            down_pipe.pop(0)

        display_screen_window.blit(game_image['background'], (0, 0))
        for pip_upper, pip_down in zip(up_pipe, down_pipe):
            display_screen_window.blit(game_image['pipe'][0], (pip_upper['x'], pip_upper['y']))
            display_screen_window.blit(game_image['pipe'][1], (pip_down['x'], pip_down['y']))

        display_screen_window.blit(game_image['base'], (0, play_ground))
        display_screen_window.blit(game_image['player'],
                                   (bird.get_position_x(), bird.get_position_y()))

        """
            显示游戏分数
        """
        score_digit = [int(x) for x in list(str(bird.get_score()))]
        digit_width = 0
        for digit in score_digit:
            digit_width += game_image['numbers'][digit].get_width()
        digit_x_offset = (scr_width - digit_width) / 2

        for digit in score_digit:
            display_screen_window.blit(game_image['numbers'][digit],
                                       (digit_x_offset, scr_height * 0.12))
            digit_x_offset += game_image['numbers'][digit].get_width()

        """
            更新游戏界面
        """
        pygame.display.update()
        time_clock.tick(FPS)


def is_colliding(player_position_x, player_position_y, up_pipes, down_pipes):
    if player_position_y > play_ground - 25 or player_position_y < 0:
        game_audio_sound['hit'].play()
        return True

    pipe_height = game_image['pipe'][0].get_height()
    pipe_width = game_image['pipe'][0].get_width()
    player_height = game_image['player'].get_height()

    for pipe in up_pipes:
        if player_position_y < pipe_height + pipe['y'] and abs(player_position_x - pipe['x']) < pipe_width:
            game_audio_sound['hit'].play()
            return True

    for pipe in down_pipes:
        if (player_position_y + player_height > pipe['y']) and abs(player_position_x - pipe['x']) < pipe_width:
            game_audio_sound['hit'].play()
            return True

    return False


def get_random_pipes():
    """
        随机生成上下两个管道
    """

    pipe_height = game_image['pipe'][0].get_height()
    off_s = scr_height / 3
    down_pipe_y = off_s + random.randrange(0, int(scr_height - game_image['base'].get_height() - 1.2 * off_s))
    up_pipe_y = pipe_height - down_pipe_y + off_s
    pipe_position_x = scr_width + 10

    pipe = [
        {'x': pipe_position_x, 'y': -up_pipe_y},
        {'x': pipe_position_x, 'y': down_pipe_y}
    ]

    return pipe


#
#  游戏主函数--完成游戏界面初始化、图片和音频的加载
#
if __name__ == '__main__':

    pygame.init()
    time_clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')

    #
    # 加载游戏资源--图片和音频
    #

    game_image['numbers'] = (
        pygame.image.load('images/0.png').convert_alpha(),
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),
        pygame.image.load('images/5.png').convert_alpha(),
        pygame.image.load('images/6.png').convert_alpha(),
        pygame.image.load('images/7.png').convert_alpha(),
        pygame.image.load('images/8.png').convert_alpha(),
        pygame.image.load('images/9.png').convert_alpha(),
    )

    game_image['message'] = pygame.image.load('images/message.png').convert_alpha()
    game_image['base'] = pygame.image.load('images/base.png').convert_alpha()
    game_image['pipe'] = (
        pygame.transform.rotate(pygame.image.load(pipe_image).convert_alpha(), 180),
        pygame.image.load(pipe_image).convert_alpha()
    )

    game_audio_sound['die'] = pygame.mixer.Sound('sounds/die.wav')
    game_audio_sound['hit'] = pygame.mixer.Sound('sounds/hit.wav')
    game_audio_sound['point'] = pygame.mixer.Sound('sounds/point.wav')
    game_audio_sound['swoosh'] = pygame.mixer.Sound('sounds/swoosh.wav')
    game_audio_sound['wing'] = pygame.mixer.Sound('sounds/wing.wav')

    game_image['background'] = pygame.image.load(bcg_image).convert_alpha()
    game_image['player'] = pygame.image.load(player).convert_alpha()

    while True:
        main_screen()
        main_gameplay()

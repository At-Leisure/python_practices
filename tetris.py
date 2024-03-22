import pygame
import Tetris
from Tetris.constant import *
import time
import random
import numpy as np

WINDOW_WIDTH = COLUME*UNIT
WINDOW_HWIGHT = ROW*UNIT

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HWIGHT), flags=pygame.RESIZABLE)
background = Tetris.make_background(ROW, COLUME, UNIT)

last_time = time.time()

base_array = np.zeros([4+ROW+1, COLUME], dtype=np.uint8)
base_array[-1] = 1

block_now = Tetris.Block()
block_now.rebuild(Tetris.BlockShape.I)
block_next = Tetris.Block()
run_game = True
while run_game:

    screen.blit(background, (0, 0))  # 对齐的坐标
    block_now.draw_on(screen)
    pygame.display.update()  # 显示内容

    for event in pygame.event.get():
        # 判断用户是否点了关闭按钮
        if event.type == pygame.QUIT:
            run_game = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print('rotate')

    if block_now.state is Tetris.BlockState.Falling:
        new_time = time.time()
        if new_time - last_time > SECOND_INTERVAL:

            test_array = base_array.copy()
            test_array[block_now.row:block_now.row+block_now.n_row, block_now.col:block_now.col+4] += block_now.array[0:block_now.n_row, :]
            # print(test_array)
            # if (test_array == 2).any():
            #     block_now.state = Tetris.BlockState.Grounded

            if not block_now.state is Tetris.BlockState.Grounded:
                block_now.row += 1
            last_time = new_time
    if block_now.state is Tetris.BlockState.Grounded:
        print('Grounded')
        base_array[block_now.row:block_now.row+block_now.n_row, block_now.col:block_now.col+4] += block_now.array[0:block_now.n_row, :]
        block_now.draw_on(background)
        block_now.rebuild(random.randint(0, 3))

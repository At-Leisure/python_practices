import pygame as pygame
import time
from . import classes as clss
from . import functions as funs
# 简谐运动 x = A cos(ωt + φ)
pygame.init()
SCR = clss.Seen(600,600)
circle_R = 20
screen = pygame.display.set_mode(SCR.size)

background = pygame.Surface(SCR.size,flags=pygame.HWSURFACE)
background.fill((33,43,53))
background_circle = clss.Circle((125,125,125),SCR.center,SCR.hei/2-circle_R,1)

line_number = 10
lines = []
def resetLines():
    global lines
    lines = [clss.Linecircle(screen,
                SCR.center,
                SCR.hei-circle_R*2,
                180/line_number*i, 
                360/line_number/2*(line_number-1-i),
                circle_color=funs.RBG_random(360/line_number*i)
            ) for i in range(line_number)]
resetLines()


def _main():
    gamerun = True

    start_time = time.time()
    while gamerun:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamerun = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    line_number += 1
                    resetLines()
                if event.key == pygame.K_DOWN:
                    line_number -=1
                    resetLines()


        screen.blit(background,(0,0))
        background_circle.draw(screen)
        for line in lines:
            line.draw()
        pygame.display.flip()


if __name__ == '__main__':
    _main()


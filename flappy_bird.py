import pygame
import time
from Flappy_Bird.classes import Bird, PillarGroup, Pause, CollisionDetector, ScoreDisplay  # 左ctrl-暂停
from Flappy_Bird import resource,classes

GameRun = True
pause = False
pygame.init()
screen = pygame.display.set_mode((756, 483), flags=pygame.RESIZABLE)
bg0 = pygame.image.load(resource.img['sky'])
background = bg0
bird = Bird(((650)/2, (350)/2), screen)
pillars = PillarGroup()
pausee = Pause((756, 483))
score = ScoreDisplay((756-20, 20), screen, init_num=1212514901)
detector = CollisionDetector(bird, pillars.group)

pass_n = 0
wrong_n = 0

while GameRun:  # 循环刷新
    time.sleep(1/120)  # 延迟时间
    if pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:  # 左ctrl-暂停
                    pause = not pause
                    bird.pause()
        continue

    screen.blit(background, (0, 0))  # 对齐的坐标
    pillars.update(screen, dx=-1)
    score.blit()
    bird.blit()
    pygame.display.update()  # 显示内容
    # 循环获取事件，监听事件
    for event in pygame.event.get():
        # 判断用户是否点了关闭按钮
        if event.type == pygame.QUIT:
            GameRun = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()
            if event.key == pygame.K_DOWN:
                bird.dowm()
            if event.key == pygame.K_LCTRL:  # 左ctrl-暂停
                pause = not pause
                # screen.blit(bg1,(0,0))
                screen.blit(pausee.image, pausee.rect)
                bird.pause()

    if detector.collisionTrue():
        wrong_n += 1
        print(f'{wrong_n=}')
    if detector.anyPassTrue():
        pass_n += 1
        print(f'{pass_n=}')
        # score.updateScore(pass_n)
        score.updateScore(pass_n)
    # 更新屏幕内容
    pygame.display.flip()

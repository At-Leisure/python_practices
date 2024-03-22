import pygame
from threading import Thread
from time import sleep
from random import random
from .resrc import resource

# 233像素=1米
METER = 233


class Bird(pygame.sprite.Sprite):
    # 定义构造函数
    def __init__(self, location, screen: pygame.Surface):
        # 调父类来初始化子类
        pygame.sprite.Sprite.__init__(self)
        self.state = 0
        self.pointedScreen = screen
        self.angle = 0
        self.image1 = pygame.image.load(resource.img['blue_bird-1'])    # 加载图片
        self.image2 = pygame.image.load(resource.img['blue_bird-2'])
        self.image3 = pygame.image.load(resource.img['blue_bird-3'])
        self.image = self.image1
        self.rect = self.image.get_rect()       # 获取图片rect区域
        self.rect.topleft = location      # 设置位置
        self.Pause = False
        self.exercise_state = 'rotation'  # rotation自转 not_rotation不自转

        self.take_smmoth = True
        if self.take_smmoth:
            self.v = 0
            self.a = -233*1.5
            self.thread = Thread(target=self.smooth_moving, daemon=True)
            self.thread.start()

    def jump(self):
        if self.take_smmoth:
            self.v = 233
        else:
            self.rect.y -= 10
        self.angle = 20

    def dowm(self):
        if self.take_smmoth:
            self.y = 10
        else:
            self.rect.y += 10

    @property
    def y(self): return 483-self.rect.y
    @y.setter
    def y(self, y_): self.rect.y = 483-y_

    def pause(self): self.Pause = not self.Pause

    def blit(self):
        self.pointedScreen.blit(pygame.transform.rotate(
            self.image, self.angle), self.rect)

    def smooth_moving(self):
        t = 1/60
        wing = 0
        while self.take_smmoth:
            sleep(t)

            if self.Pause:
                continue

            self.v += self.a*t
            self.y = self.y + self.v*t + 0.5*self.a*t*t

            if self.y < 28:
                self.y = 28.1
                self.v = -0.7*self.v

            if abs(self.v) < 1e-10:
                self.v = -50
                self.angle = -self.angle

            if self.y > 483:
                self.y = 483
                self.v *= 0.1

            wing += 1
            wing %= 7
            if wing == 0:
                self.state += 1
                self.state %= 4
                if self.state == 0:
                    self.image = self.image1
                if self.state == 1:
                    self.image = self.image2
                if self.state == 2:
                    self.image = self.image3
                if self.state == 3:
                    self.image = self.image2


class PlrTop(pygame.sprite.Sprite):
    # 定义构造函数
    def __init__(self, location):
        # 调父类来初始化子类
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(resource.img['pipe'])    # 加载图片
        self.rect = self.image.get_rect()       # 获取图片rect区域
        self.rect.topleft = location      # 设置位置


class PlrBelow(pygame.sprite.Sprite):
    # 定义构造函数
    def __init__(self, location):
        # 调父类来初始化子类
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(resource.img['pipe'])    # 加载图片
        self.rect = self.image.get_rect()       # 获取图片rect区域
        self.rect.topleft = location      # 设置位置


class Pillar:
    def __init__(self, distance_to_top: int):
        SPACE = 130
        self.distance_to_top = distance_to_top
        self.top = PlrTop((756, -(640-distance_to_top)))
        self.below = PlrBelow((756, SPACE+distance_to_top))

    def update(self, screen, dx=0):
        self.top.rect.x += dx
        self.below.rect.x += dx
        screen.blit(self.top.image, self.top.rect)
        screen.blit(self.below.image, self.below.rect)


class PillarGroup:
    def __init__(self):
        self.group = []
        self.group.append(Pillar(100))

    def update(self, screen, *, dx=0):
        for plr in self.group:
            plr.update(screen, dx)
        self.try_add()
        self.remove_old()

    def try_add(self):
        if self.group[-1].top.rect.x < 756-260:
            dist = self.group[-1].distance_to_top+(random()-0.5)*200
            if dist < 0:
                dist = 10
            if 483-dist < 0:
                dist = 473
            self.group.append(Pillar(dist))

    def remove_old(self):
        if self.group[0].top.rect.x < -100:
            del self.group[0]


class Pause(pygame.sprite.Sprite):
    # 定义构造函数
    def __init__(self, fullsize):
        # 调父类来初始化子类
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(resource.img['pause'])    # 加载图片
        self.rect = self.image.get_rect()       # 获取图片rect区域
        self.rect.x = fullsize[0]/2 - self.image.get_width()/2
        self.rect.y = fullsize[1]/2 - self.image.get_height()/2


class CollisionDetector():  # 检测 碰撞+通过
    def __init__(self, bird: Bird, plrGroup: PillarGroup) -> None:
        self.pointedGroup = plrGroup
        self.bird = bird
        self.pillar = plrGroup[0]
        self.detected = False
        self.passed = False

    def updateObject(self):  # 重置self.detected & self.passed
        self.pillar = self.pointedGroup[self.pointedGroup.index(self.pillar)+1]
        self.detected = self.passed = False

    def collisionTrue(self):
        if self.detected:
            return
        result1 = pygame.sprite.collide_mask(
            self.bird, self.pillar.top)  # 两个精灵之间的像素蒙版检测，更为精准的一种检测方式。
        result2 = pygame.sprite.collide_mask(self.bird, self.pillar.below)
        if result1 or result2:
            self.detected = True

            return True

    def anyPassTrue(self):  # 不管是否碰撞 只检测是否穿过
        if self.passed:
            return
        if self.bird.rect.x > self.pillar.top.rect.x+self.pillar.top.image.get_width():
            self.passed = True
            self.updateObject()
            return True


class ScoreDisplay():
    def __init__(self, location, screen: pygame.Surface, *, init_num=0) -> None:
        self.num = init_num
        self.pointedScreen = screen
        self.imageGroup = [pygame.image.load(resource.img['score'][i]) for i in range(10)]
        self.updateScore(self.num)
        self.location = location      # 设置位置

    def updateScore(self, num: int):
        self.num = num

    def scoreadd(self):
        self.num += 1

    def blit(self):
        nums = list(map(int, str(self.num)))
        rect = self.imageGroup[0].get_rect()
        rect.topleft = self.location
        for i in range(len(nums)-1, -1, -1):
            img = self.imageGroup[nums[i]]
            rect.x -= img.get_width()
            self.pointedScreen.blit(img, rect)

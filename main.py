import time

import pyxel
import random as rand
from enum import Enum
from collections import deque


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    STOP = 5


class Apple:
    def __init__(self):
        self.x = rand.randint(0, 160)
        self.y = rand.randint(0, 120)
        self.w = 10
        self.h = 10

    def collide(self, x, y, w, h):
        intersected = False
        # print(x, self.x, y, self.y)
        if (
                (x + w) > self.x and
                (y + h) > self.y and
                (self.x + self.w) > x and
                (self.y + self.h) > y
        ):
            intersected = True
        return intersected

    def update(self):
        self.x = self.x

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16, 0, self.h, self.w)


count: int = 0


class Section:
    def __init__(self, x, y, direction, is_head=False):
        global count
        self.x = x
        self.y = y
        self.w = 8
        self.h = 8
        self.count = count
        self.delta = 1
        count += 1
        self.is_head = is_head
        self.q = deque()
        for i in range(0, self.w+1):
            print(i)
            self.q.append(direction)

    def move(self, dir, now=False):
        d = dir
        if not(now):
            self.q.append(dir)
            d = self.q.popleft()
        match d:
            case Direction.LEFT:
                self.x = (self.x - self.delta) % pyxel.width
            case Direction.UP:
                self.y = (self.y - self.delta) % pyxel.width
            case Direction.RIGHT:
                self.x = (self.x + self.delta) % pyxel.width
            case Direction.DOWN:
                self.y = (self.y + self.delta) % pyxel.width

    def draw(self):
        # print(self.count, self.x ,self.x)
        pyxel.rect(self.x, self.y, self.w, self.h, 9)
        if self.is_head:
            pyxel.blt(self.x, self.y, 0, 8, 0, self.w, self.h)
        else:
            pyxel.blt(self.x, self.y, 0, 0, 0, self.w, self.h)


class Worm:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 8
        self.h = 8
        self.Dir = Direction.LEFT
        self.dt = 0
        self.speed = 1
        self.time_last_move = time.time()
        self.sections = []
        self.sections.append(Section(0, 32, Direction.LEFT, True))
        self.sections.append(Section(8, 32, Direction.LEFT))
        self.sections.append(Section(16, 32, Direction.LEFT))

    def move(self, delta):
        pre = self.Dir
        for s in self.sections:
            s.delta = delta
            if s.is_head:
                s.move(pre, True)
            else:
                s.move(pre)
                pre = s.q[0]
            # match s.direction:
            #     case Direction.LEFT:
            #         self.sections[0].x = (self.sections[0].x - 1) % pyxel.width
            #     case Direction.UP:
            #         self.sections[0].y = (self.sections[0].y - 1) % pyxel.width
            #     case Direction.RIGHT:
            #         self.sections[0].x = (self.sections[0].x + 1) % pyxel.width
            #     case Direction.DOWN:
            #         self.sections[0].y = (self.sections[0].y + 1) % pyxel.width

    def update(self):
        time_now = time.time()
        time_delta = time_now - self.speed
        if (time_delta) > (1 / self.speed):
            self.move(self.speed/1)
            self.time_last_move = time_now

    def draw(self):
        for s in self.sections:
            s.draw()


class App:
    def __init__(self):
        pyxel.init(160, 120, fps=100)
        pyxel.load("Assets/myres.pyxres")
        self.worm = Worm()
        self.apple = Apple()
        pyxel.run(self.update, self.draw)

    def draw(self):
        pyxel.cls(0)
        self.worm.draw()
        self.apple.draw()

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_UP):
            self.worm.Dir = Direction.UP
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.worm.Dir = Direction.DOWN
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.worm.Dir = Direction.RIGHT
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.worm.Dir = Direction.LEFT
        if pyxel.btnp(pyxel.KEY_S):
            self.worm.speed = self.worm.speed * 1.1
            print(self.worm.speed)
        if self.apple.collide(self.worm.sections[0].x, self.worm.sections[0].y, self.worm.w, self.worm.h):
            self.worm.sections.append(
                Section(self.worm.sections[-1].x, self.worm.sections[-1].y, Direction.STOP))
            retry = 10
            while self.apple.collide(self.worm.sections[0].x, self.worm.sections[0].y, self.worm.w,
                                     self.worm.h) and retry > 0:
                self.apple.x = rand.randint(10, 150)
                self.apple.y = rand.randint(10, 110)
                retry -= 1
            if (retry == 0):
                print("YOU WIN")
                pyxel.quit()
        self.worm.update()
        self.apple.update()


App()

"""
@author : Léo Imbert
@created : 04/06/2025
@updated : 04/06/2025
"""

import random
import pyxel
import math

class Boulder:

    def __init__(self, x:int, y:int):
        self.x, self.y = x, y
        self.tx, self.ty = x, y
        self.max_speed = 20
        self.speed, self.friction = 0, 0.9
        self.moving = False
        self.direction_x, self.direction_y = 0, 0
        self.traj_x, self.traj_y = 0, 0

    def cal(self):
        self.direction_x = -1 if self.tx - self.x < 0 else 1
        self.direction_y = -1 if self.ty - self.y < 0 else 1

        direction_x = self.tx - self.x
        direction_y = self.ty - self.y
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        self.traj_x = direction_x
        self.traj_y = direction_y
        
    def update(self):
        if self.speed < 1:
            self.moving = False

        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.speed < self.max_speed:
            self.speed += 0.2

        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and not self.moving:
            self.tx, self.ty = clamp(pyxel.mouse_x, 0, pyxel.width), clamp(pyxel.mouse_y, 0, pyxel.height)
            self.moving = True
            self.cal()

        if self.moving:
            self.x += abs(self.traj_x * self.speed) * self.direction_x
            self.y += abs(self.traj_y * self.speed) * self.direction_y
            self.speed *= self.friction

            if self.x - 5 < 0 or self.x + 5 > pyxel.width:
                self.direction_x = -self.direction_x
            if self.y - 5 < 0 or self.y + 5 > pyxel.height:
                self.direction_y = -self.direction_y

    def draw(self):
        pyxel.circ(self.x, self.y, 5, 13)

class Box:

    def __init__(self, x:int, y:int, w:int, h:int):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.alive = True

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, 4)

def clamp(x, mini, maxi):
    return max(mini, min(x, maxi))

def lerp(a, b, t):
    return a + (b - a) * t

class Game:

    def __init__(self):
        pyxel.init(128, 128, title="Boulder Blast", fps=60)
        pyxel.fullscreen(True)

        self.shake_amount = 0
        self.shake_sub_amount = 0

        self.b = Boulder(64, 64)
        self.boxes = [Box(10, 40, 10, 10)]

        pyxel.run(self.update, self.draw)

    def shake_camera(self, amount:int, sub_amount:float):
        self.shake_amount = amount
        self.shake_sub_amount = sub_amount

    def update(self):
        self.b.update()

        for box in self.boxes:
            x = (box.x + box.w // 2) - self.b.x
            y = (box.y + box.h // 2) - self.b.y
            if abs(x) < box.w // 2 + 5 and abs(y) < box.h // 2 + 5:
                box.alive = False
                self.shake_camera(2, 0.1)
                self.boxes.append(Box(random.randint(0, 117), random.randint(0, 117), 10, 10))

        self.boxes = [box for box in self.boxes if box.alive]

        if self.shake_amount > 0:
            amount = round(self.shake_amount)
            pyxel.camera(random.randint(-amount, amount), random.randint(-amount, amount))
            self.shake_amount -= self.shake_sub_amount
        else:
            pyxel.camera(0, 0)

    def draw(self):
        pyxel.cls(2)

        for box in self.boxes:
            box.draw()

        self.b.draw()

        pyxel.circb(pyxel.mouse_x, pyxel.mouse_y, 5, 7)

if __name__ == "__main__":
    Game()
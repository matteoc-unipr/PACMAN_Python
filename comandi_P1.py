
import g2d
from random import choice, randrange
from time import time
from actor import Actor, Arena


class PacMan(Actor):
    def __init__(self, arena, pos):
        self._x, self._y = pos
        self._w, self._h = 20, 20
        self._speed = 2
        self._dx, self._dy = 0, 0
        self._lives = 3
        self._last_collision = 0
        self._arena = arena
        arena.add(self)

    def move(self):
        arena_w, arena_h = self._arena.size()
        self._y += self._dy
        if self._y < 0:
            self._y = 0
        elif self._y > arena_h - self._h:
            self._y = arena_h - self._h

        self._x += self._dx
        if self._x < 0:
            self._x = 0
        elif self._x > arena_w - self._w:
            self._x = arena_w - self._w

    def control(self, keys):
        u, d, l, r = "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"
        #u, d, l, r = "w", "s", "a", "d"

        if g2d.key_pressed(u) and self._x % 8 and self._y % 8: 
            self._dy = -2
        elif g2d.key_pressed(d) and self._x % 8 and self._y % 8:
            self._dy = self._speed
        else: 
            self._dy = self._speed

        if g2d.key_pressed(l) and self._x % 8 and self._y % 8:
            self._dx = -2
        elif g2d.key_pressed(r) and self._x % 8 and self._y % 8:
            self._dx = 2
        else: 
            self._dx = 0
    def lives(self) -> int:
        return self._lives

    def collide(self, other):
        pass
    def position(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def symbol(self):
        return 0, 20

#!/usr/bin/env python3

from pacman_map import board
class Actor():
    '''Interface to be implemented by each game character
    '''
    def move(self):
        '''Called by Arena, at the actor's turn
        '''
        raise NotImplementedError('Abstract method')

    def collide(self, other: 'Actor'):
        '''Called by Arena, whenever the `self` actor collides with some
        `other` actor
        '''
        raise NotImplementedError('Abstract method')

    def position(self) -> (int, int):
        '''Return the position of the actor (left-top corner)
        (x, y)
        '''
        raise NotImplementedError('Abstract method')

    def size(self) -> (int, int):
        '''Return the size of the actor
        (w, h)
        '''
        raise NotImplementedError('Abstract method')

    def symbol(self) -> (int, int):
        '''Return the position (x, y) of current sprite, if it is contained in
        a larger image, with other sprites. Otherwise, simply return None
        '''
        raise NotImplementedError('Abstract method')


class Arena():
    '''A generic 2D game, with a given size in pixels and a list of actors
    '''
    def __init__(self, size: (int, int)):
        '''Create an arena, with given dimensions in pixels
        '''
        self._w, self._h = size
        self._count = 0
        self._actors = []
        self._cookies_list = []
        self._big_cookies_list = []
        
    
    
    def add(self, a: Actor):
        '''Register an actor into this arena.
        Actors are blitted in their order of registration
        '''
        if a not in self._actors:
            self._actors.append(a)

    def remove(self, a: Actor):
        '''Cancel an actor from this arena
        '''
        if a in self._actors:
            self._actors.remove(a)

    def move_all(self):
        '''Move all actors (through their own move method).
        After each single move, collisions are checked and eventually
        the `collide` methods of both colliding actors are called
        '''
        actors = list(reversed(self._actors))
        for a in actors:
            pos = a.position()
            a.move()
            if pos != a.position():
                for other in actors:
                    # reversed order, so actors drawn on top of others
                    # (towards the end of the cycle) are checked first
                    if other is not a and self.check_collision(a, other):
                            a.collide(other)
                            other.collide(a)
        self._count += 1

    def check_collision(self, a1: Actor, a2: Actor) -> bool:
        '''Check the two actors (args) for mutual collision (bounding-box
        collision detection). Return True if colliding, False otherwise
        '''
        x1, y1, w1, h1 = a1.position() + a1.size()
        x2, y2, w2, h2 = a2.position() + a2.size()
        return (y2 < y1 + h1 and y1 < y2 + h2
            and x2 < x1 + w1 and x1 < x2 + w2
            and a1 in self._actors and a2 in self._actors)

    def actors(self) -> list:
        '''Return a copy of the list of actors
        '''
        return list(self._actors)

    def size(self) -> (int, int):
        '''Return the size of the arena as a couple: (width, height)
        '''
        return (self._w, self._h)

    def count(self) -> int:
        '''Return the total count of ticks (or frames)
        '''
        return self._count

    def add_cookies(self):
        line = 0
        h = 0
        l = 0
        for line_ in board:
            line +=1
            for element in board[len(board) - (len(board) - line) - 1]:
                if element == "-":
                   y = h - 1
                   x = l - 1
                   pos = x, y                                                    #cookies
                   self._cookies_list.append(pos)
                elif element == "+":
                   y = h -4
                   x = l - 4
                   pos = x, y 
                   self._big_cookies_list.append(pos)                    
                l += 8
            l = 0
            h += 8
        
    def draw_cookies(self) -> list:
        '''Return a copy of the list of cookies
        '''
        return list(self._cookies_list)

    def draw_big_cookies(self) -> list:
        '''Return a copy of the list of cookies
        '''
        return list(self._big_cookies_list)


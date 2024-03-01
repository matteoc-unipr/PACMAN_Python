
from pygame.constants import BLEND_ADD
from pacman_map import in_wall
import g2d
from random import choice, randrange
from time import time
from actor import Actor, Arena


class Ghost(Actor):
    def __init__(self, arena, pos, color):
        self._v = 2
        self._x, self._y = pos
        self._w, self._h = 16, 16
        self._arena = arena
        arena.add(self)
        self._direction = 0, 0 
        self._visible = True
        self._ghost_sim = False
        self._symbol = 0
        self._up = 0, -self._v
        self._down = 0, self._v
        self._left = -self._v, 0
        self._right = self._v, 0
        self._dx = 0
        self._dy = 0
        self._count = 0
        self._color = color
        
    def move(self):
        '''
        Prevides ghosts to collide walls and control their directions
        '''
        possible_directions = [self._up, self._down, self._left, self._right]
        self._direction = choice(possible_directions)
        
        if in_wall(self._x + self._dx, self._y + self._dy) == True:
            possible_directions.remove(self._direction)
        
        
        if self._direction == self._up and self._dy != self._v and in_wall(self._x, self._y - self._v) == False:
            self._dx, self._dy = self._up                                                                           #up
            
        if self._direction == self._down and self._dy != -self._v and in_wall(self._x, self._y + self._v) == False:
            self._dx, self._dy = self._down                                                                         #down

        if self._direction == self._left and self._dx != self._v and in_wall(self._x - self._v, self._y) == False:
            self._dx, self._dy = self._left                                                                         #left
        if self._direction == self._right and self._dx != -self._v and in_wall(self._x + self._v, self._y) == False:
            self._dx, self._dy = self._right                                                                        #right
        
       
        if in_wall(self._x + self._dx, self._y + self._dy) == False:   
            arena_w, arena_h = self._arena.size()
            if self._x + self._dx >= arena_w - 16:
                self._x = 0
            if self._x + self._dx <= 0:
                self._x = arena_w

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
        
        '''
        Every 100 frames changes ghosts' symbols
        '''
        if randrange(100) == 0:
            self._visible = not self._visible
        
        self._count += 1
        if self._count % 5 == 0:
                self._ghost_sim = not self._ghost_sim

    def collide(self, other):
        pass

    def position(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def simb_ghost(self):
        '''
        Manage the variation of ghosts' symbols for the animation
        '''
        if self._ghost_sim == True:
            self._symbol = 16
        else:
            self._symbol = 0 
        
        return self._symbol

    def symbol(self):
        '''
        Manage Ghosts' symbols for each direction and color combination. 
        '''
        color = 0 
        if self._color == 1:
            color = 64
        if self._color == 2:
            color = 80
        if self._color == 3:
            color = 96
        if self._color == 4:
            color = 112
        
        if self._visible:
            if self._dx == 0 and self._dy == -self._v:
                return 64 + self._symbol, color                         #up visible
        
            if self._dx == 0 and self._dy == self._v:
                return 96 + self._symbol, color                            #down visible
        
            if self._dx == -self._v and self._dy == 0:
                return 32 + self._symbol, color                            #left visible
        
            if self._dx == self._v and self._dy == 0:
                return 0 + self._symbol, color                              #right visible
            
            if self._dx == 0 and self._dy == 0:
                return 32 + self._symbol, color   


        else:
            if self._dx == 0 and self._dy == -self._v:
                return 160, 80                           #up invisible
        
            if self._dx == 0 and self._dy == self._v:
                return 176, 80                           #down invisible
        
            if self._dx == -self._v and self._dy == 0:
                return 144, 80                           #left invisible
        
            if self._dx == self._v and self._dy == 0:
                return 128, 80                           #right invisible









class Cookies(Actor):
    def __init__(self, arena, pos):
        self._x, self._y = pos
        self._w, self._h = 2, 2
        self._arena = arena
        arena.add(self)
        

    def move(self):
        pass

    def collide(self, other):
        if isinstance(other, PacMan):
            self._arena.remove(self)

    def position(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h
    
    def symbol(self):
        symbol = 167, 55
        return symbol

class BigCookies(Actor):
    def __init__(self, arena, pos):
        self._x, self._y = pos
        self._w, self._h = 8, 8
        self._arena = arena
        arena.add(self)
    
    def move(self):
        pass

    def collide(self, other):
        if isinstance(other, PacMan):
            self._arena.remove(self)
           
    def position(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h
    
    def symbol(self):
        symbol = 180, 52
        return symbol

class PacMan(Actor):
    def __init__(self, arena, pos):
        self._x, self._y = pos
        self._w, self._h = 16, 16
        self._speed = 2
        self._dx, self._dy = 0, 0
        self._lives = 3
        self._last_collision = 0
        self._arena = arena
        self._count = 0
        self._mouth_open = False 
        self._symbol = 0
        self._sup = False
        self._superpower = None
        arena.add(self)   



    
    def move(self):
        if in_wall(self._x + self._dx, self._y + self._dy) == False:
            arena_w, arena_h = self._arena.size()
            if self._x + self._dx >= arena_w - 16:
                self._x = 0
            if self._x + self._dx <= 0:
                self._x = arena_w

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
            
            self._count += 1
            if self._count % 5 == 0:                                     #mouth
                self._mouth_open = not self._mouth_open
            
            #if self._sup == True:
            #    count = self._count
            #    #print(count)
            #    while (self._count - count) != 300:
            #        print(self._count)
            #        self._superpower = True
            #    self._sup = False
            #else:
            #    self._superpower = False


    def control(self, keys):
        #print(self._superpower)
        '''
        Control the direction of the pacman with the given keys.
        It works with WASD but also with arrows.
        It controls walls and avoid pacman to collide them.
        '''
        dx, dy = self._dx, self._dy
        
        if "ArrowUp" in keys or "w" in keys and in_wall(self._x, self._y - self._speed) == False:
            self._dx = 0                 #up
            self._dy = -self._speed
        elif "ArrowDown" in keys or "s" in keys and in_wall(self._x, self._y + self._speed) == False:
            self._dx = 0
            self._dy = self._speed       #down
        elif "ArrowLeft" in keys or "a" in keys and in_wall(self._x - self._speed, self._y) == False:
            self._dx = -self._speed
            self._dy = 0                 #left  
        elif "ArrowRight" in keys or "d" in keys and in_wall(self._x + self._speed, self._y) == False:
            self._dx = self._speed
            self._dy = 0                 #right
        else:
            self._dx, self._dy = dx, dy
        
    def lives(self) -> int:
        return self._lives
    
    def collide(self, other):
        if isinstance(other, Ghost):
            self._arena.remove(self)
    
        if isinstance(other, Ghost):            #################
            self._arena.remove(Ghost)

        if isinstance(other, BigCookies):
            self._sup = True
        
        
                
    def position(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h
    

    def simb_mouth_open(self):
        if self._mouth_open == True:
            self._symbol = 0
        else:
            self._symbol = 16
        
        return self._symbol


    def symbol(self):
        '''
        Manage the symbol of the pacman for each direction.
        '''
        if self._dx == 0 and self._dy == -self._speed:
            return self._symbol, 32                           #up
        
        if self._dx == 0 and self._dy == self._speed:
            return self._symbol, 48                           #down
        
        if self._dx == -self._speed and self._dy == 0:
            return self._symbol, 16                           #left
        
        if self._dx == self._speed and self._dy == 0:
            return self._symbol, 0                           #right

        if self._dx == 0 and self._dy == 0:
            return 32, 0
import g2d_mod as g2d
from pacman_map import in_wall
from random import choice, randrange
from actor_mod import Actor, Arena

#CARICA ANCHE G2D, FONT, ACTOR E SPRITES 

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
        return self._x, self._y + 42

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
        return self._x, self._y + 42

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
        self._sup_count = 300 
        self._sup = False
        self._superpower = False
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
           

    def control(self, keys):
        self._sup_count += 1
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
    
    def sup_count(self):
        if self._sup_count in range(0, 200):
            self._superpower = True
            return True
        else:
            self._superpower = False
            return False    
    
    def collide(self, other):        
        if isinstance(other, BigCookies):
            self._sup_count = 0


        if isinstance(other, Ghost) and self._superpower == False:
            if self._arena.count() - self._last_collision < 90:
                return
            self._last_collision = self._arena.count()
            self._lives -= 1
            if self._lives > 0:
                self._x, self._y = 110, 186
            if self._lives == 0:
                self._arena.remove(self)            


    def position(self):
        return self._x, self._y + 42

    def size(self):
        return self._w, self._h
    
    def symbol(self):
        '''
        Manage the symbol of the pacman for each direction.
        '''
    
        if self._dx == 0 and self._dy == -self._speed:
            if self._mouth_open == True:
                return 0, 32     
            else:                                              #up
                return 16, 32                       
        
        if self._dx == 0 and self._dy == self._speed:
            if self._mouth_open == True:
                return 0, 48     
            else:
                return 16, 48                                 #down

        if self._dx == -self._speed and self._dy == 0:
            if self._mouth_open == True:
                return 0, 16     
            else:                                             #left
                return 16, 16                          
        
        if self._dx == self._speed and self._dy == 0:
            if self._mouth_open == True:
                return 0, 0     
            else:                                             #right
                return 16, 0                          
        if self._dx == 0 and self._dy == 0:
            return 32, 0


class Ghost(Actor):
    def __init__(self, arena, pos, color):
        self._v = 2
        self._x, self._y = pos
        self._w, self._h = 16, 16
        self._arena = arena
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
        self._collision = None
        self._blue_ghost = True
        arena.add(self)
    
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
        if self._blue_ghost == False:
            if randrange(100) == 0:
                self._visible = not self._visible
        if self._blue_ghost == True:
            self._visible = True
        
        self._count += 1
        if self._count % 5 == 0:
                self._ghost_sim = not self._ghost_sim

    def collide(self, other):
            if isinstance(other, PacMan):
                self._collision = True
            else:
                self._collision = False
    
    def superpower(self,):
        return self._collision

    def remove_ghost(self):
        self._arena.remove(self)

    def position(self):
        return self._x, self._y + 42

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
    
    def blue_ghost(self):
        self._blue_ghost = True
    def not_blue_ghost(self):
        self._blue_ghost = False
    
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
        if self._color == 5:      #BLUE for superpower
            color = 64
        
        if self._visible:
            if self._dx == 0 and self._dy == -self._v:                      #up visible
                if self._blue_ghost == False:
                    if self._ghost_sim == True:
                        return 64 + 16, color                                  
                    else:
                        return 64, color
                else:
                    if self._ghost_sim == True:
                        return 192, 64                                  
                    else:
                        return 208, 64

            if self._dx == 0 and self._dy == self._v:
                if self._blue_ghost == False:                               #down visible 
                    if self._ghost_sim == True:
                        return 96 + 16, color                                  
                    else:
                        return 96, color  
                else:
                    if self._ghost_sim == True:
                        return 224, 64                                  
                    else:
                        return 240, 64                                  
        
            if self._dx == -self._v and self._dy == 0:                      #left visible
                if self._blue_ghost == False:
                    if self._ghost_sim == True:
                        return 32 + 16, color                                  
                    else:
                        return 32, color
                else:
                    if self._ghost_sim == True:
                        return 160, 64                                  
                    else:
                        return 176, 64                                                              
        
            if self._dx == self._v and self._dy == 0:                       #right visible
                if self._blue_ghost == False:
                    if self._ghost_sim == True:
                        return 0 + 16, color                                  
                    else:
                        return 0, color
                else:
                    if self._ghost_sim == True:
                        return 128, 64                                  
                    else:
                        return 144, 64                                      
            
            if self._dx == 0 and self._dy == 0:
                if self._blue_ghost == False:
                    if self._ghost_sim == True:
                        return 32 + 16, color                                  
                    else:
                        return 32, color 
                else:
                    if self._ghost_sim == True:
                        return 128, 64                                  
                    else:
                        return 144, 64               


        else:
            if self._dx == 0 and self._dy == -self._v:
                return 160, 80                           #up invisible
        
            if self._dx == 0 and self._dy == self._v:
                return 176, 80                           #down invisible
        
            if self._dx == -self._v and self._dy == 0:
                return 144, 80                           #left invisible
        
            if self._dx == self._v and self._dy == 0:
                return 128, 80                           #right invisible



class Boardgame():
    def __init__(self):
        self._arena = Arena((232, 256))
        self._arena.add_cookies()
        for i in self._arena.draw_cookies():           
            Cookies(self._arena, i)                                  #Funzione aggiunta in arena
        for i in self._arena.draw_big_cookies():
            BigCookies(self._arena, i)
        
        self._PacMan = PacMan(self._arena, (112, 184))
        self._RedGhost = Ghost(self._arena, (8, 232), 1)              #red = 1
        self._PGhost = Ghost(self._arena, (208, 232), 3)        #purple = 2
        self._BlueGhost = Ghost(self._arena, (208, 8), 3)            #blue = 3
        self._YellowGhost = Ghost(self._arena, (8, 8), 4)         #yellow = 4

        self._time = 300
        self._score = 0
        self._name = g2d.prompt("Player username?")
    
    def superpower(self):
        #print(self._RedGhost.superpower())
        if self._PacMan.sup_count() == True:
            self._RedGhost.blue_ghost()              
            self._PGhost.blue_ghost()         
            self._BlueGhost.blue_ghost()            
            self._YellowGhost.blue_ghost()
        else:
            self._RedGhost.not_blue_ghost()              
            self._PGhost.not_blue_ghost()         
            self._BlueGhost.not_blue_ghost()            
            self._YellowGhost.not_blue_ghost()                 
        
        if self._PacMan.sup_count() == True:
            if self._RedGhost.superpower() == True:
                self._RedGhost.remove_ghost()
                #print("R")
                self._RedGhost = Ghost(self._arena, (112, 88), 1)  
            if self._PGhost.superpower() == True:
                self._PGhost.remove_ghost()
                self._PGhost.superpower() = False
                self.PGhost = Ghost(self._arena, (112, 88), 3)                #AGGIUNGERE CONTATORE
            if self._BlueGhost.superpower() == True:
                self._BlueGhost.remove_ghost()
                self._BlueGhost = Ghost(self._arena, (112, 88), 3) 
            if self._YellowGhost.superpower() == True:
                self._YellowGhost.remove_ghost() 
                self._YellowGhost = Ghost(self._arena, (112, 88), 4)            
    
    def game_over(self):
        return self._PacMan.lives() <= 0

    def game_won(self):
        return len(self._arena.actors()) <= 5

    def game_start(self):
        return 

    def game_lost(self):
        return self.remaining_time() <= 0

    def name(self):
        return self._name
    
    def score(self):
        if self._PacMan.lives() == 3:
            return self._score
        if self._PacMan.lives() == 2:
            return self._score - 500
        if self._PacMan.lives() == 1:
            return self._score - 1000
        if self._PacMan.lives() == 0:
            return self._score - 1500   

    def remaining_time(self):
        return (self._time - self._arena.count() // 30)

    def arena(self):
        return self._arena

    def hero(self):
        return self._PacMan

class PacGui():
    def __init__(self):
        self._game = Boardgame()
        g2d.init_canvas((232, 340))        
        g2d.main_loop(self.tick)
        self._game.game_start()
        self._bestscore = 0
        

    
    def tick(self):        
        self._game.superpower()      
        self._game.hero().control(g2d.current_keys())
        arena = self._game.arena()
        arena.move_all()  # Game logic
        
        with open("BESTSCORE.txt", "r") as bestscore:
            for line in bestscore:
                bestscore = line 
                self._bestscore = int(bestscore)
        
        g2d.clear_canvas()
        g2d.set_color((0, 0, 0))
        g2d.fill_rect((0, 0), (232, 340))
        g2d.draw_image("pacman_bg.png", (0, 42))

        for a in arena.actors():
            if a.symbol() != None:
                g2d.draw_image_clip("PacMan_sprites_mod.png", a.symbol(), a.size(), a.position())
        name = "ID: " + str(self._game.name())
        lives = "Lives: " + str(self._game.hero().lives())
        toplay = "Time: " + str(self._game.remaining_time())
        scores = "Score: " + str(self._game.score())
        best_score = "Best Score: " + str(self._bestscore)

        g2d.set_color((255, 255, 255))
        g2d.draw_text(name + " ", (5, 10), 8)
        g2d.draw_text(lives + " ", (5, 300), 8)
        g2d.draw_text(toplay + " ", (150, 300), 8)
        g2d.draw_text(scores + " ", (140, 30), 6)
        g2d.draw_text(best_score + " ", (8, 30), 6)
        
        if self._game.hero().lives() >= 1:
            g2d.draw_image_clip("PacMan_sprites_mod.png", (16, 0), (16, 16), (5, 314))

        if self._game.hero().lives() >= 2:
            g2d.draw_image_clip("PacMan_sprites_mod.png", (16, 0), (16, 16), (21, 314))

        if self._game.hero().lives() >= 3:
            g2d.draw_image_clip("PacMan_sprites_mod.png", (16, 0), (16, 16), (37, 314))

        if self._game.hero().sup_count():
            g2d.draw_image_clip("PacMan_sprites_mod.png", (208, 0), (16, 16), (100, 15))       
        
        if self._game.game_over():
            if self._game.score() > self._bestscore:
                with open("BESTSCORE.txt", "w") as new_bestscore:
                    print(self._game.score(), file=new_bestscore)
                g2d.alert(("Game over!" " " "   New Best Score!!! ", self._game.score()))
            else:
                g2d.alert(("Game over!" " " "   Your score is  ", self._game.score()))
            
            g2d.close_canvas()

        
        elif self._game.game_lost():
            g2d.alert(("Game over!" " " "   Your score is", self._game.score()))
            g2d.close_canvas()
        
        elif self._game.game_won():
            g2d.alert(("Game won!" " " "   Your score is", self._game.score()))
            g2d.close_canvas()

gui = PacGui()

def main():
    g2d.init_canvas(Boardgame.arena.size())
    g2d.main_loop(PacGui.tick)

main()

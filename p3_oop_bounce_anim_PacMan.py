import g2d
from p3_oop_bounce_PacMan import Arena, PacMan, Ghost, Cookies, BigCookies

arena = Arena((232, 256))
arena.add_cookies()
for i in arena.draw_cookies():
    Cookies(arena, i)
for i in arena.draw_big_cookies():
    BigCookies(arena, i)

PacMan = PacMan(arena, (112, 184))
RedGhost = Ghost(arena, (80, 8), 1)              #red = 1
PurpleGhost = Ghost(arena, (208, 232), 2)        #purple = 2
BlueGhost = Ghost(arena, (208, 8), 3)            #blue = 3
YellowGhost = Ghost(arena, (208, 64), 4)         #yellow = 4



def tick():
    PacMan.control(g2d.current_keys())
    arena.move_all()  # Game logic

    g2d.clear_canvas()
    g2d.draw_image("pacman_bg.png", (0, 0))
    
    for a in arena.actors():
        if a.symbol() != None:
            PacMan.simb_mouth_open()
            g2d.draw_image_clip("PacMan_sprites.png", a.symbol(), a.size(), a.position())
            
            
        else:
            g2d.fill_rect(a.position(), a.size())
    

def main():
    g2d.init_canvas(arena.size())
    g2d.main_loop(tick)

main()

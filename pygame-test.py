# first time trying the pygame module
# unfinished game i was working on, called "Animal Run"
# related files are in assets folder

import pygame as pg
from sys import exit

#initial
pg.init()
screen = pg.display.set_mode((800,450))
screen.fill('light blue')
pg.display.set_caption('Animal Run')
clock = pg.time.Clock()

#variables & flags
player_x_pos = 50
player_y_pos = 350
cat_flag = False
cat_atk = False
player_gravity = 0
last_update = pg.time.get_ticks()
cooldown = 150

#surfaces & frames
sky_surface = pg.image.load('graphics/sky.jpg').convert()
ground_surface = pg.image.load('graphics/ground.jpg').convert()
cat1idle = [pg.image.load(f'graphics/cat/cat1idle{i}.png').convert_alpha() for i in range(1,5)]
cat1run = [pg.image.load(f'graphics/cat/cat1run{i}.png').convert_alpha() for i in range(1,6)]
cat1attack = [pg.image.load(f'graphics/cat/cat1attack{i}.png').convert_alpha() for i in range(1,5)]
bin = pg.image.load('graphics/cat/bin.png').convert()
frames = {'idle' : 0, 'run' : 0, 'attack' : 0}

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if cat_rect.collidepoint(event.pos):
                cat_atk = True
        if event.type == pg.KEYDOWN:
            if event.key in [pg.K_d, pg.K_RIGHT]:
                cat_flag = 1
            if event.key == pg.K_a:
                cat_flag = -1
            if event.key in [pg.K_SPACE, pg.K_w] and player_y_pos == 350:
                player_gravity = -19
        if event.type == pg.KEYUP:
            if event.key in [pg.K_d, pg.K_RIGHT, pg.K_a]:
                cat_flag = 0
       
    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0,350))
    screen.blit(bin, (100, 350))

    #frame updater
    current_time = pg.time.get_ticks()
    if current_time-last_update >= cooldown:
        last_update = current_time
        if cat_flag in [1,-1]:
            frames['run'] += 1
            if cat_flag == 1:
                player_x_pos += 20
            elif cat_flag == -1:
                player_x_pos -= 20
            if frames['run'] >= len(cat1run): frames['run'] = 0
        elif cat_flag == 0 and cat_atk == False:
            frames['idle'] += 1
            if frames['idle'] >= len(cat1idle) : frames['idle'] = 0 

    if cat_flag in [1,-1]:
        cat_surf = cat1run[frames['run']]
    else:
        cat_surf = cat1idle[frames['idle']]
    cat_rect = cat_surf.get_rect(midbottom = (player_x_pos, player_y_pos))

    player_gravity += 1
    player_y_pos += player_gravity
    if player_y_pos >= 350: player_y_pos = 350
    if player_x_pos < 0: player_x_pos = 880
    if player_x_pos > 880: player_x_pos = 0

    screen.blit(cat_surf, cat_rect) 

    pg.display.update()
    clock.tick(60)

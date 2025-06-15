# basic pong game i made to play at school, it has a single-player and a two-player mode

#imports
import pygame as pg
from sys import exit
import random

#functions
def player_movement():
    global player_spd

    player.y += player_spd
    if player.top <= 0:
        player.top = 0
    elif player.bottom >= screen_h:
        player.bottom = screen_h

def opponent_movement():
    global opponent_spd, ai_spd

    opponent.y += opponent_spd
    ai_spd = 5 + player_scr
    if ai_flag:
        if ball.centery < opponent.centery:
            opponent_spd = -ai_spd
        elif ball.centery > opponent.centery:
            opponent_spd = ai_spd
    if opponent.top <= 0:
        opponent.top = 0
    elif opponent.bottom >= screen_h:
        opponent.bottom = screen_h

def ball_movement():
    global ball_spd_x, ball_spd_y, player_scr, opponent_scr, scr_time

    ball.x += ball_spd_x ; ball.y += ball_spd_y
    if ball.top <= 0 or ball.bottom >= screen_h:
        ball_spd_y *= -1
    if ball.left <= 0:
        scr_time = pg.time.get_ticks()
        player_scr += 1
    elif ball.right >= screen_w:
        scr_time = pg.time.get_ticks()
        opponent_scr += 1
    if ball.colliderect(player) and ball_spd_x > 0:
        if abs(ball.right - player.left) < 10:
            ball_spd_x *= -1
            if player_spd < 0:
                ball_spd_y -= 3 ; ball_spd_x += 3
            elif player_spd > 0 :
                ball_spd_y += 3 ; ball_spd_x -= 3

    elif ball.colliderect(opponent) and ball_spd_x < 0:
        ball_spd_x *= -1
        if player_spd < 0:
                ball_spd_y -= 3 ; ball_spd_x += 3
        elif player_spd > 0 :
                ball_spd_y += 3 ; ball_spd_x -= 3

def ball_start():
    global ball_spd_x, ball_spd_y, scr_time

    curr_time = pg.time.get_ticks()

    ball.center = (screen_w/2, screen_h/2)

    if curr_time - scr_time < 700:
        cnt = game_font.render('3', False, light_grey)
        screen.blit(cnt, (screen_w/2 - 10, screen_h/2 + 20))
    elif 700 < curr_time - scr_time < 1400:
        cnt = game_font.render('2', False, light_grey)
        screen.blit(cnt, (screen_w/2 - 10, screen_h/2 + 20))
    elif 1400 < curr_time - scr_time < 2100:
        cnt = game_font.render('1', False, light_grey)
        screen.blit(cnt, (screen_w/2 - 10, screen_h/2 + 20))
    if curr_time - scr_time < 2100:
        ball_spd_x, ball_spd_y = 0,0
    else:
        ball_spd_x = init_ball_spd*random.choice((1,-1))
        ball_spd_y = init_ball_spd*random.choice((1,-1))
        scr_time = None

#initializers
pg.init()
screen_w = 1280 ; screen_h = 640
screen = pg.display.set_mode((screen_w, screen_h))
pg.display.set_caption('pong')
clock = pg.time.Clock()

#flags
start_flag = True
ai_flag = True

#rects
ball = pg.Rect(screen_w/2 - 15, screen_h/2 - 15, 30, 30)
player = pg.Rect(screen_w-20, screen_h/2 - 70, 10, 140)
opponent = pg.Rect(10, screen_h/2 - 70, 10, 140)
pve = pg.Rect((screen_w/2, screen_h/2), (50,50))

#variables
light_grey = (200,200,200)
game_font = pg.font.Font('assets/BrassMono-Regular.ttf', 32)
ball_spd_x = 7 ; ball_spd_y = 7
player_spd = 0 ; opponent_spd = 0
init_ball_spd = 9
player_scr = 0 ; opponent_scr = 0
ai_spd = 5 
scr_time = None

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                ai_flag = not ai_flag
            if event.key == pg.K_DOWN:
                player_spd = (7 + opponent_scr)
            if event.key == pg.K_UP:
                player_spd = -(7 + opponent_scr) 
            if event.key == pg.K_s and ai_flag == False:
                opponent_spd = 7+player_scr
            if event.key == pg.K_w and ai_flag == False:
                opponent_spd = -(7 + player_scr)
        if event.type == pg.KEYUP:
            if event.key in [pg.K_DOWN, pg.K_UP]:
                player_spd = 0
            if event.key in [pg.K_s, pg.K_w]:
                opponent_spd = 0 

    screen.fill('black')

    if start_flag == True:
        ball_movement()
        player_movement()
        opponent_movement()

        pg.draw.rect(screen, light_grey, player)
        pg.draw.rect(screen, light_grey, opponent)
        pg.draw.ellipse(screen, light_grey, ball)

        player_txt = game_font.render(f'{player_scr}', False, light_grey)
        screen.blit(player_txt, (658, screen_h/2))
        opponent_txt = game_font.render(f'{opponent_scr}', False, light_grey)
        screen.blit(opponent_txt, (607, screen_h/2))

        if scr_time:
            ball_start()
    else:
        menu_txt = pg.font.Font('assets/BrassMono-Regular.ttf', 64).render('PONG', False, light_grey)
        screen.blit(menu_txt, (600, screen_h/2 - 160))
        pg.draw.rect(screen, light_grey, pve)
    
    pg.display.flip()
    clock.tick(60)

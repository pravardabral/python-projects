# testing and messing around with the pymunk library

import pygame
import pymunk
import math
import pymunk.pygame_util

pygame.init()

WIDTH, HEIGHT = 1000, 600
window = pygame.display.set_mode((WIDTH,HEIGHT))

def calc_dist(p1, p2):
    return math.sqrt((p2[1]-p1[1])**2 + (p2[0]-p1[0])**2)

def calc_angle(p1, p2):
    return math.atan2(p2[1]-p1[1], p2[0]-p1[0])

def draw(space, window, draw_opt, line):
    window.fill('white')

    if line:
        pygame.draw.line(window, 'black', line[0], line[1], 3)
    space.debug_draw(draw_opt)

    pygame.display.update()

def add_bound(space, width, height):
    rects = [[(width/2, height-10), (width, 20)],
             [(width/2, 10), (width, 20)],
             [(10, height/2), (20, height)],
             [(width-10, height/2), (20, height)]]
    
    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 0.2
        space.add(body, shape)

def add_ball(space, radius, mass, pos):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.color = (255, 0, 0, 100)
    shape.mass = mass
    shape.elasticity = 1
    shape.friction = 0.1
    space.add(body, shape)
    return shape

def add_struct(space, width, height):
    BROWN = (139, 69, 19, 100)
    BLACK = (0, 0, 0, 100)
    rects = [[(600, height-100), (40, 200), BROWN, 100],
             [(900, height-100), (40, 200), BROWN, 100],
             [(750, height-200), (340, 40), BROWN, 140],
             [(700, height-240), (30, 150), BROWN, 90],
             [(800, height-240), (30, 150), BROWN, 90],
             [(750, height-390), (170, 30), BROWN, 95]]
    
    for pos, size, color, mass in rects:
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Poly.create_box(body, size, radius=1)
        shape.color = color
        shape.mass = mass
        shape.elasticity = 0.6
        shape.friction = 0.2
        space.add(body, shape)

def run(window, width, height):
    running = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1/fps

    space = pymunk.Space()
    space.gravity = (0, 981)

    add_bound(space, width, height)
    add_struct(space, width, height)

    draw_opt = pymunk.pygame_util.DrawOptions(window)

    clicked_pos = None
    ball = None

    while running:
        line = None
        if ball and clicked_pos:
            line = [clicked_pos, pygame.mouse.get_pos()]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not ball:
                    clicked_pos = pygame.mouse.get_pos()
                    ball = add_ball(space, 25, 50, clicked_pos)
                elif clicked_pos:
                    ball.body.body_type = pymunk.Body.DYNAMIC
                    angle = calc_angle(*line)
                    force = calc_dist(*line) * 30 * ball.mass
                    fx = math.cos(angle) * force ; fy = math.sin(angle) * force
                    ball.body.apply_impulse_at_local_point((fx, fy), (0, 0))
                    clicked_pos = None
                else:
                    space.remove(ball, ball.body)
                    ball = None

        draw(space, window, draw_opt, line)
        space.step(dt)
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)

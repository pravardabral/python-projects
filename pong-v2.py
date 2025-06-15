# slightly better version of pong with classes, this one requires images for the ball and paaddle
# the images are stored in the assets folder

#imports
import pygame, sys, random

#base sprite class
class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos, y_pos))

#player class
class Player(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0
    
    def screen_const(self):
        if self.rect.top < 0: self.rect.top = 0
        elif self.rect.bottom > screen_h: self.rect.bottom = screen_h

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_const()

#ball class
class Ball(Block):
    def __init__(self, path, x_pos, y_pos, x_speed, y_speed, paddles):
        super().__init__(path, x_pos, y_pos)
        self.x_speed = x_speed * random.choice((-1,1))
        self.y_speed = y_speed * random.choice((-1,1))
        self.paddles = paddles
        self.active = False
        self.score_time = 0

    def update(self):
        if self.active:
            self.rect.x += self.x_speed
            self.rect.y += self.y_speed
            self.collision()
        else:
            self.restart_counter()

    def collision(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen_h: 
            self.y_speed *= -1

        if pygame.sprite.spritecollide(self, self.paddles, False):
            collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.x_speed > 0 :
                self.x_speed *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.x_speed < 0:
                self.x_speed *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.y_speed < 0 :
                self.y_speed *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.y_speed > 0:
                self.y_speed *= -1

            if self.rect.colliderect(collision_paddle):
                if player.movement < 0:
                    if self.y_speed < 0:
                        self.y_speed -= 1 ; self.x_speed += 1
                    elif self.y_speed > 0:
                        self.y_speed += 1 ; self.x_speed -= 1
                elif player.movement > 0 :
                    if self.y_speed > 0:
                        self.y_speed += 1 ; self.x_speed -= 1
                    elif self.y_speed < 0:
                        self.y_speed -= 1 ; self.x_speed += 1
                if opponent.movement < 0:
                    if self.y_speed < 0:
                        self.y_speed -= 1 ; self.x_speed += 1
                    elif self.y_speed > 0:
                        self.y_speed += 1 ; self.x_speed -= 1
                elif opponent.movement > 0 :
                    if self.y_speed > 0:
                        self.y_speed += 1 ; self.x_speed -= 1
                    elif self.y_speed < 0:
                        self.y_speed -= 1 ; self.x_speed += 1

    def reset_ball(self):
        self.active = False
        self.x_speed = random.choice((-1,1)) * ball_speed
        self.y_speed = random.choice((-1,1)) * ball_speed
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_w/2, screen_h/2)

    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        number = 3

        if current_time - self.score_time <= 700:
            number = 3
        if 700 < current_time - self.score_time <= 1400:
            number = 2
        if 1400 < current_time - self.score_time <= 2100:
            number = 1
        if current_time - self.score_time >= 2100:
            self.active = True

        time_counter = game_font.render(str(number), True, acc_colour)
        time_counter_rect = time_counter.get_rect(center= (screen_w/2, screen_h/2 +50))
        pygame.draw.rect(screen, bg_colour, time_counter_rect)
        screen.blit(time_counter, time_counter_rect)

#opponent class
class Opponent(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0

    def update(self, ball_group):
        if ai_flag:
            if self.rect.top < ball_group.sprite.rect.y:
                self.rect.y += self.speed
            elif self.rect.bottom > ball_group.sprite.rect.y:
                self.rect.y -= self.speed
        else:
            self.rect.y += self.movement
        self.screen_const()

    def screen_const(self):
        if self.rect.top < 0: self.rect.top = 0
        elif self.rect.bottom > screen_h: self.rect.bottom = screen_h

#game runner class
class Mainframe:
    def __init__(self, ball_group, paddle_group):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group

    def run_game(self):
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_w:
            self.opponent_score += 1
            self.ball_group.sprite.reset_ball()
        elif self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            self.ball_group.sprite.reset_ball()

    def draw_score(self):
        player_score = game_font.render(str(self.player_score), True, acc_colour)
        opponent_score = game_font.render(str(self.opponent_score), True, acc_colour)

        player_score_rect = player_score.get_rect(midleft = (screen_w/2 + 40, screen_h/2))
        opponent_score_rect = opponent_score.get_rect(midleft = (screen_w/2 - 60, screen_h/2))

        screen.blit(player_score, player_score_rect)
        screen.blit(opponent_score, opponent_score_rect)

#initializers
pygame.init()
screen_w = 1280 ; screen_h = 640
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('pong')
clock = pygame.time.Clock()

#global variables
game_font = pygame.font.Font("C:/Users/Pravar/Downloads/BrassMono/BrassMono-Bold.ttf", 32)
bg_colour = pygame.Color(0,0,0)
acc_colour = pygame.Color(27,35,43)
strip = pygame.Rect(screen_w/2 - 2, 0, 4, screen_h)

#game variables
paddle_speed = 5
ball_speed = 5

#flags
ai_flag = True

#player & opponent objects
player = Player('assets/Paddle.png', screen_w - 20, screen_h/2, paddle_speed)
opponent = Opponent('assets/Paddle.png',20, screen_h/2, paddle_speed)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

#ball object
ball = Ball('assets/Ball.png', screen_w/2, screen_h/2, ball_speed, ball_speed, paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

game = Mainframe(ball_sprite, paddle_group)

while True:
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #key pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ai_flag = not ai_flag
            if event.key == pygame.K_DOWN:
                player.movement += player.speed
            if event.key == pygame.K_UP:
               player.movement -= player.speed 
            if event.key == pygame.K_s and ai_flag == False:
                opponent.movement += opponent.speed
            if event.key == pygame.K_w and ai_flag == False:
                opponent.movement -= opponent.speed
        #key released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player.movement -= player.speed
            if event.key == pygame.K_UP:
               player.movement += player.speed 
            if event.key == pygame.K_s and ai_flag == False:
                opponent.movement -= opponent.speed
            if event.key == pygame.K_w and ai_flag == False:
                opponent.movement += opponent.speed
            

    screen.fill(bg_colour)
    pygame.draw.rect(screen, acc_colour, strip)

    game.run_game()
    
    pygame.display.flip()
    clock.tick(120)

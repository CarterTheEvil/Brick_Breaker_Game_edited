import pygame
import math

pygame.init()
window = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Brick Breaker")
clock = pygame.time.Clock()

window_icon = pygame.image.load("assets/favicon.png")
pygame.display.set_icon(window_icon)

window_width, window_height = window.get_width(), window.get_height()

class Ball:
    def __init__(self):
        self.x = (window_width/2)-13
        self.y = window_height-48
        self.move = False
        self.move_change = [0, 0]
        self.pause = False
        self.over = False
        self.img = "assets/ball.png"
        self.ball = pygame.image.load(self.img).convert_alpha()
        self.ball = pygame.transform.scale(self.ball, (25,25))
    def draw(self):
        window.blit(self.ball, (self.x, self.y))
    def set_default(self, paddle_x):
        self.x = paddle_x + 37
        self.y = window_height-48
        self.move = False
        self.pause = False
        self.over = False
    def change_with_paddle_and_border(self, paddle_x):
        if not self.move and not self.pause and not self.over:
            self.x = paddle_x + 37
        elif self.move:
            if (self.x <= 0):
                if (self.move_change[0] < 0):
                    self.move_change[0] = -1 * self.move_change[0]
            elif (self.x >= (window_width-25)):
                if (self.move_change[0] > 0):
                    self.move_change[0] = -1 * self.move_change[0]
            if (self.y <= 0):
                if (self.move_change[1] < 0):
                    self.move_change[1] = -1 * self.move_change[1]
            elif (self.y >= (window_height-48) and self.y <= (window_height-46) and self.x > (paddle_x - 25) and self.x < (paddle_x + 100)):
                if (self.move_change[1] > 0):
                    if (self.x < paddle.x):
                        angle = 170-(80*((self.x-(paddle_x-25))/25))
                        self.move_change = [math.cos(math.radians(angle)), math.sin(math.radians(angle))]
                    elif (self.x > (paddle_x + 75)):
                        angle = 80-(80*((self.x-(paddle_x+75))/25))
                        self.move_change = [math.cos(math.radians(angle)), math.sin(math.radians(angle))]
                    self.move_change[1] = -1 * self.move_change[1]
            elif (self.y >= (window_height-45) and self.y <= (window_height-5) and self.x > (paddle_x - 25) and self.x < (paddle_x + 100)):
                if (self.move_change[1] > 0):
                    if (self.x < paddle.x):
                        if (self.move_change[0] > 0):
                            self.move_change[0] = -1 * self.move_change[0]
                    elif (self.x > (paddle_x + 75)):
                        if (self.move_change[0] < 0):
                            self.move_change[0] = -1 * self.move_change[0]
            elif (self.y >= (window_height+10)):
                pass
            self.x = self.x + self.move_change[0]
            self.y = self.y + self.move_change[1]
    def change_after_hit_brick(self, hitting_side):
        if (hitting_side == None):
            return
        elif (hitting_side == "up"):
            if (self.move_change[1] > 0):
                self.move_change[1] = -1 * self.move_change[1]
        elif (hitting_side == "down"):
            if (self.move_change[1] < 0):
                self.move_change[1] = -1 * self.move_change[1]
        elif (hitting_side == "left"):
            if (self.move_change[0] > 0):
                self.move_change[0] = -1 * self.move_change[0]
        elif (hitting_side == "right"):
            if (self.move_change[0] < 0):
                self.move_change[0] = -1 * self.move_change[0]
    def when_screen_size_change(self):
        self.x = (window_width/2)-13
        self.y = window_height-48
                
class Paddle:
    def __init__(self):
        self.x = (window_width/2)-50
        self.y = window_height-25
        self.change_length = 2
        self.img = "assets/paddle.png"
        self.paddle = pygame.image.load(self.img).convert_alpha()
        self.paddle = pygame.transform.scale(self.paddle, (100,20))
    def draw(self):
        window.blit(self.paddle, (self.x, self.y))
    def when_screen_size_change(self):
        self.x = (window_width/2)-50
        self.y = window_height-25
    def change(self, direction):
        if (direction == ""):
            return
        elif (direction == "left"):
            if (self.x > 0):
                self.x = self.x - self.change_length
        elif (direction == "right"):
            if (self.x < (window_width-100)):
                self.x = self.x + self.change_length

class Start_angle:
    def __init__(self):
        self.x_y = ((window_width/2)-25, window_height-130)
        self.paddle_x = window_height/2
        self.current_angle = 90
        self.img = "assets/dotted_line.png"
        self.line = pygame.image.load(self.img)
        self.line = pygame.transform.scale(self.line, (50,100))
    def draw(self):
        window.blit(self.line, self.x_y)
    def angle(self, theta):
        self.line = pygame.image.load(self.img)
        self.line = pygame.transform.scale(self.line, (50,100))
        offset = pygame.math.Vector2(0, 50)
        rotate = offset.rotate(-theta)
        self.line = pygame.transform.rotozoom(self.line, theta, 1.0)
        new_center = ((self.paddle_x)-rotate.x, (window_height-35)-rotate.y)
        self.x_y = self.line.get_rect(center=new_center)
    def change(self, direction):
        if (direction == ""):
            return
        elif (direction == "up"):
            if (self.current_angle > 1):
                self.current_angle = self.current_angle - 1
                self.angle(self.current_angle-90)
        elif (direction == "down"):
            if (self.current_angle < 179):
                self.current_angle = self.current_angle + 1
                self.angle(self.current_angle-90)
        elif (direction == "mid"):
            self.current_angle = 90
            self.angle(0)
    def adjust_with_paddle(self, x):
        self.paddle_x = x + 50
        self.angle(self.current_angle-90)

class Brick:
    def __init__(self):
        self.img = "assets/brick.png"
        self.brick = pygame.image.load(self.img).convert_alpha()
        self.brick = pygame.transform.scale(self.brick, (50,25))
        self.bricks_columns = 8
        self.bricks_rows = 4
        self.first_brick_coordinate = [(window_width-(56*self.bricks_columns))/2, ((window_height-(30*self.bricks_rows))/2)-40]
        self.bricks_active = [[]]
        self.bricks_coordinate = [[]]
        self.total_bricks = 0
        self.all_bricks_wiped_out = True
        self.default_brick()
    def default_brick(self):
        self.first_brick_coordinate = [(window_width-(56*self.bricks_columns))/2, ((window_height-(30*self.bricks_rows))/2)-40]
        self.bricks_active.clear()
        self.bricks_coordinate.clear()
        self.total_bricks = 0
        for i in range(self.bricks_rows):
            l = []
            c = []
            for j in range(self.bricks_columns):
                l.append(True)
                c.append([self.first_brick_coordinate[0]+(j*56), self.first_brick_coordinate[1]+(i*30)])
                self.total_bricks = self.total_bricks + 1
            self.bricks_active.append(l)
            self.bricks_coordinate.append(c)
    def draw(self):
        for i in range(self.bricks_rows):
            for j in range(self.bricks_columns):
                if self.bricks_active[i][j]:
                    window.blit(self.brick, tuple(self.bricks_coordinate[i][j]))
    def update(self, ball_x, ball_y):
        ball_x = int(ball_x)
        ball_y = int(ball_y)
        hitting_side = None
        current_brick = 0
        self.all_bricks_wiped_out = True
        for i in range(self.bricks_rows):
            for j in range(self.bricks_columns):
                if self.bricks_active[i][j]:
                    self.all_bricks_wiped_out = False
                    current_brick = current_brick + 1
                    if (self.bricks_coordinate[i][j][0] <= (ball_x+25) and
                        (self.bricks_coordinate[i][j][0]+50) >= ball_x and
                        self.bricks_coordinate[i][j][1] == (ball_y+25)):
                        self.bricks_active[i][j] = False
                        hitting_side = "up"
                    elif (self.bricks_coordinate[i][j][0] <= (ball_x+25) and
                        (self.bricks_coordinate[i][j][0]+50) >= ball_x and
                        (self.bricks_coordinate[i][j][1]+25) == ball_y):
                        self.bricks_active[i][j] = False
                        hitting_side = "down"
                    if (self.bricks_coordinate[i][j][1] <= (ball_y+25) and
                        (self.bricks_coordinate[i][j][1]+25) >= ball_y and
                        self.bricks_coordinate[i][j][0] == (ball_x+25)):
                        self.bricks_active[i][j] = False
                        hitting_side = "left"
                    elif (self.bricks_coordinate[i][j][1] <= (ball_y+25) and
                        (self.bricks_coordinate[i][j][1]+25) >= ball_y and
                        (self.bricks_coordinate[i][j][0]+50) == ball_x):
                        self.bricks_active[i][j] = False
                        hitting_side = "right"
        return hitting_side, (self.total_bricks-current_brick)
    def bricks_number_change(self, operator):
        if (operator == "+" and self.bricks_columns < 12):
            self.bricks_columns = self.bricks_columns + 1
            self.bricks_rows = self.bricks_columns - 4
        elif (operator == "-" and self.bricks_columns > 6):
            self.bricks_columns = self.bricks_columns - 1
            self.bricks_rows = self.bricks_columns - 4
    def when_screen_size_change(self):
        self.first_brick_coordinate = [(window_width-(56*self.bricks_columns))/2, ((window_height-(30*self.bricks_rows))/2)-40]
        self.bricks_coordinate.clear()
        for i in range(self.bricks_rows):
            c = []
            for j in range(self.bricks_columns):
                c.append([self.first_brick_coordinate[0]+(j*56), self.first_brick_coordinate[1]+(i*30)])
            self.bricks_coordinate.append(c)

class Statistics:
    def __init__(self):
        self.l_img = "assets/lifeline.png"
        self.nl_img = "assets/no_lifeline.png"
        self.lifeline_img = pygame.image.load(self.l_img).convert_alpha()
        self.lifeline = pygame.transform.scale(self.lifeline_img, (int(window_height/20),int(window_height/20)))
        self.no_lifeline_img = pygame.image.load(self.nl_img).convert_alpha()
        self.no_lifeline = pygame.transform.scale(self.no_lifeline_img, (int(window_height/20),int(window_height/20)))
        self.lifeline_available = 3
        self.font = pygame.font.Font(None, int(window_height/20))
        self.score = 0
        self.text = self.font.render("Score: 0", True, (255, 255, 255))
        self.pause = self.font.render("PAUSE", True, (255, 255, 255))
    def draw(self):
        score = "Score: " + str(self.score)
        self.text = self.font.render(score, True, (255, 255, 255))
        window.blit(self.text, (10, (window_height/20)+5))
        for i in range(3):
            if (self.lifeline_available > i):
                window.blit(self.lifeline, (5+(i*(window_height/20)+5),5))
            else:
                window.blit(self.no_lifeline, (5+(i*(window_height/20)+5),5))
    def update_score(self, score):
        self.score = score
    def pause_active_message(self):
        width = self.pause.get_width()
        window.blit(self.pause, ((window_width/2)-(width/2), 10))
    def final_result(self, win):
        if win:
            result = "You Win"
            color = (0, 255, 0)
        else:
            result = "You Loss! Your Score is " + str(self.score)
            color = (255, 0, 0)
        font = pygame.font.Font(None, 50)
        text = font.render(result, False, color)
        text_width, text_height = text.get_width(), text.get_height()
        window.blit(text, ((window_width/2)-(text_width/2), (window_height/2)-(text_height/2)))
    def when_screen_size_change(self):
        self.lifeline = pygame.transform.scale(self.lifeline_img, (int(window_height/20),int(window_height/20)))
        self.no_lifeline = pygame.transform.scale(self.no_lifeline_img, (int(window_height/20),int(window_height/20)))
        self.font = pygame.font.Font(None, int(window_height/20))
        

ball = Ball()
paddle = Paddle()
startAngle = Start_angle()
brick = Brick()
stat = Statistics()

paddle_change_direction = ""
start_angle_change = ""

def restart_game():
    ball.set_default(paddle.x)
    stat.update_score(0)
    stat.lifeline_available = 3
    brick.default_brick()

fullscreen = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle_change_direction = "left"
            elif event.key == pygame.K_RIGHT:
                paddle_change_direction = "right"
            elif event.key == pygame.K_UP:
                start_angle_change = "up"
            elif event.key == pygame.K_DOWN:
                start_angle_change = "down"
            elif event.key == pygame.K_RETURN:
                if (stat.lifeline_available <= 0 or not ball.move and ball.over):
                    restart_game()
                elif not ball.move and not ball.pause:
                    ball.move = True
                    ball_start_angle = startAngle.current_angle
                    ball.move_change = [math.cos(math.radians(ball_start_angle)), math.sin(math.radians(ball_start_angle))]
                    startAngle.change("mid")
                elif ball.y >= (window_height+10):
                    restart_game()
            elif event.key == pygame.K_ESCAPE:
                if (ball.move and ball.y < window_height):
                    stat.lifeline_available = stat.lifeline_available - 1
                    if (stat.lifeline_available <= 0):
                        ball.move = False
                        ball.over = True
                    else:
                        ball.set_default(paddle.x)
                elif (stat.lifeline_available <= 0 or not ball.move and ball.over):
                    restart_game()
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                if not ball.move and not ball.pause or stat.lifeline_available <= 0:
                    brick.bricks_number_change("+")
                    restart_game()
            elif event.key == pygame.K_MINUS or event.key == pygame.K_UNDERSCORE:
                if not ball.move and not ball.pause or stat.lifeline_available <= 0:
                    brick.bricks_number_change("-")
                    restart_game()
            elif event.key == pygame.K_SPACE:
                if ball.move:
                    ball.move = False
                    ball.pause = True
                elif ball.pause:
                    ball.move = True
                    ball.pause = False
            elif event.key == pygame.K_DELETE:
                restart_game()
        elif event.type == pygame.KEYUP:
            paddle_change_direction = ""
            start_angle_change = ""
            if event.key == pygame.K_F11:
                if not ball.move and not ball.pause:
                    if fullscreen:
                        window = pygame.display.set_mode((800, 400))
                    else:
                        window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    window_width, window_height = window.get_width(), window.get_height()
                    fullscreen = not fullscreen
                    ball.when_screen_size_change()
                    paddle.when_screen_size_change()
                    brick.when_screen_size_change()
                    stat.when_screen_size_change()
    window.fill((0, 0, 0))
    stat.draw()
    if not ball.move:
        if (ball.x == (paddle.x+37) and ball.y == (window_height-48)):
            startAngle.adjust_with_paddle(paddle.x)
            startAngle.change(start_angle_change)
            startAngle.draw()
    else:
        hit, score = brick.update(ball.x, ball.y)
        ball.change_after_hit_brick(hit)
        stat.update_score(score)
        if brick.all_bricks_wiped_out:
            ball.move = False
            ball.over = True
    brick.draw()
    if not ball.pause:
        paddle.change(paddle_change_direction)
    else:
        stat.pause_active_message()
    paddle.draw()

    ball.change_with_paddle_and_border(paddle.x)
    ball.draw()

    if (ball.move and ball.y >= (window_height+10)):
        stat.lifeline_available = stat.lifeline_available - 1
        if (stat.lifeline_available > 0):
            ball.set_default(paddle.x)
    
    if not ball.move and ball.over and (stat.lifeline_available > 0):
        stat.final_result(True)
    elif (stat.lifeline_available <= 0):
        stat.final_result(False)

    pygame.display.update()
    clock.tick(600)

pygame.quit()
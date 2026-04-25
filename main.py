import pygame
import time
import random

class Ball:
    def __init__(self):
        self.x = random.randint(150,650)
        self.y= random.randint(150, 450)
        self.vx= random.uniform(-300, 300)
        self.vy= random.uniform(-200, 0)
        self.color = (50,70,200)
        # self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

# this is a reset button
class Button:
    # to form a rectangle
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    # to draw the rectangle on a screen and fill it with text
    def draw(self, screen, font):
        pygame.draw.rect(screen, (100,100,100), self.rect)
        pygame.draw.rect(screen, (255,255,255), self.rect, 2)

        txt = font.render(self.text, True, (255,255,255))
        screen.blit(txt, (self.rect.x + 10, self.rect.y + 5))

    # upon clicking the button the simulation is reset
    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
    

class Slider:
    # this is the slider
    # x,y are the coords for location
    # width is how long you want to slider to be
    # min_val is the minimum value of the variable
    # start_val is the initial/default value of the variable
    def __init__(self, x, y, width, min_val, max_val, start_val):
        self.x = x
        self.y = y
        self.width = width
        self.min = min_val
        self.max = max_val
        self.value = start_val
        
        self.handle_x = x + (start_val - min_val) / (max_val - min_val) * width
        self.dragging = False

    def draw(self, screen):
        # line
        pygame.draw.line(screen, (200,200,200), (self.x, self.y), (self.x + self.width, self.y), 4)
        # handle
        pygame.draw.circle(screen, (255,0,0), (int(self.handle_x), self.y), 8)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if abs(event.pos[0] - self.handle_x) < 10 and abs(event.pos[1] - self.y) < 10:
                self.dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        if event.type == pygame.MOUSEMOTION and self.dragging:
            self.handle_x = max(self.x, min(event.pos[0], self.x + self.width))

            # convert position → value
            ratio = (self.handle_x - self.x) / self.width
            self.value = self.min + ratio * (self.max - self.min)


simulation_speed = 1 # default 1
acceleration = 50    # gravity
bounce_factor = 0.8  # {0 : no bounce, 1 : perfect bounce} 
radius = 10

reset_button = Button(650, 20, 120, 40, "Reset")
gravity_slider = Slider(50, 550, 200, 0, 500, acceleration)
bounce_slider = Slider(300, 550, 200, 0, 1, bounce_factor)
speed_slider = Slider(550, 550, 200, 0.1, 3, simulation_speed)

no_of_balls = 5
balls = []*no_of_balls

for _ in range(no_of_balls):
    balls.append(Ball())


pygame.init()
font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

# create window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game Window")

def reset_simulation():
    global balls

    balls = []
    for _ in range(no_of_balls):
        balls.append(Ball())
# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if reset_button.is_clicked(event):
            reset_simulation()

        gravity_slider.update(event)
        bounce_slider.update(event)
        speed_slider.update(event)

    screen.fill((0, 0, 0))
    dt = (clock.tick(60) / 1000) * simulation_speed  # 60 FPS, dt in seconds

    acceleration = gravity_slider.value
    bounce_factor = bounce_slider.value
    simulation_speed = speed_slider.value

    # render text
    def render_text(elms)->None:
        keys = list(elms.keys())
        for i in range(len(elms)):
            screen.blit(font.render(f"{keys[i]}: {elms[keys[i]]:.2f}", True, (255,255,255)), (10,10 + (i) * 20))
    
    render_info = {"X":balls[0].x,"Y":balls[0].y,"velX":balls[0].vx,"velY":balls[0].vy}
    render_text(render_info)


    for ball in balls:
        ball.vy += acceleration * dt # gravity
        ball.x += ball.vx * dt
        ball.y += ball.vy * dt

    for ball in balls:
        if ball.x <= 100 + radius: # top
            ball.x = 100 + radius
            ball.vx = -ball.vx * bounce_factor

        if ball.x >= 700 - radius: # bottom
            ball.x = 700 - radius
            ball.vx = -ball.vx * bounce_factor

        if ball.y <= 100 + radius: # left
            ball.y = 100 + radius
            ball.vy = -ball.vy * bounce_factor

        if ball.y >= 500 - radius: # right
            ball.y = 500 - radius
            ball.vy = -ball.vy * bounce_factor
    for i in range(len(balls)):
        for j in range(i+1, len(balls)):
            b1 = balls[i]
            b2 = balls[j]

            dx = b1.x - b2.x
            dy = b1.y - b2.y
            dist = (dx**2 + dy**2)**0.5
            
            if dist == 0:
                continue

            if dist < 2 * radius:
                # push apart (important)
                overlap = 2 * radius - dist
                b1.x += dx / dist * overlap / 2
                b1.y += dy / dist * overlap / 2
                b2.x -= dx / dist * overlap / 2
                b2.y -= dy / dist * overlap / 2

                # swap velocities
                b1.vx, b2.vx = b2.vx, b1.vx
                b1.vy, b2.vy = b2.vy, b1.vy
    for ball in balls:
        #pygame.draw.circle(screen,(color(RGB)), (coords), size of the circle)
        pygame.draw.circle(screen, ball.color, (int(ball.x), int(ball.y)), radius)

    # pygame.draw.line(screen,(0,255,0),(balls[0]["x"],balls[0]["y"]),(balls[1]["x"],balls[1]["y"]),1)
    # for i in range(len(balls)):
    #     for j in range(i,len(balls)):
    #         if i!=j:
    #             pygame.draw.line(screen,(0,255,0),(balls[i]["x"],balls[i]["y"]),(balls[j]["x"],balls[j]["y"]),1)
                
    pygame.draw.line(screen,(255,255,255),(100,100),(700,100),2) # top
    pygame.draw.line(screen,(255,255,255),(100,500),(700,500),2) # bottom
    pygame.draw.line(screen,(255,255,255),(700,100),(700,500),2) # right
    pygame.draw.line(screen,(255,255,255),(100,100),(100,500),2) # left


    reset_button.draw(screen, font) # resets the simulation
    gravity_slider.draw(screen) # to adjust gravity during simulation
    bounce_slider.draw(screen) # to change the bounce factor during simulation
    speed_slider.draw(screen) # to change the speed of simulation

    screen.blit(font.render(f"Gravity:{acceleration}", True, (255,255,255)), (50, 520))
    screen.blit(font.render(f"Bounce:{bounce_factor}", True, (255,255,255)), (300, 520))
    screen.blit(font.render(f"Speed:{simulation_speed:.2f}", True, (255,255,255)), (550, 520))
    pygame.display.update()  # refresh screen

pygame.quit()
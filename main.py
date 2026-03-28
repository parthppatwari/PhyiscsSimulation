import pygame
import time
import random


pygame.init()

def dot_product(a1,a2):
    if len(a1) != len(a2):
        raise "dot prod err: array length does not match"
    return [a1[i] * a2[i] for i in range(len(a1))]


balls = []
no_of_balls = 1
radius = 10

for _ in range(no_of_balls):
    balls.append({
        "x": random.randint(150, 650),
        "y": random.randint(150, 450),
        "vx": random.uniform(-300, 300),
        "vy": random.uniform(-200, 0)
    })

# x, y = 400, 100   # starting position

# vx = random.uniform(-300, 300)
# vy = random.uniform(-200, 0)

acceleration = 0
bounce_factor = 1

font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()


# create window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game Window")

# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    simulation_speed = 1
    dt = (clock.tick(60) / 1000) * simulation_speed  # 60 FPS, dt in seconds

    # render text
    def render_text(elms)->None:
        keys = list(elms.keys())
        for i in range(len(elms)):
            screen.blit(font.render(f"{keys[i]}: {elms[keys[i]]:.2f}", True, (255,255,255)), (10,10 + (i) * 20))
    

    render_info = {"X":balls[0]["x"],"Y":balls[0]["y"],"velX":balls[0]["vx"],"velY":balls[0]["vy"]}
    render_text(render_info)


    for ball in balls:
        ball["x"] += ball["vx"] * dt
        ball["y"] += ball["vy"] * dt
        ball["vy"] += acceleration * dt # gravity

    for ball in balls:
        if ball["x"] <= 100 + radius: # top
            ball["x"] = 100 + radius
            ball["vx"] = -ball["vx"] * bounce_factor

        if ball["x"] >= 700 - radius: # bottom
            ball["x"] = 700 - radius
            ball["vx"] = -ball["vx"] * bounce_factor

        if ball["y"] <= 100 + radius: # left
            ball["y"] = 100 + radius
            ball["vy"] = -ball["vy"] * bounce_factor

        if ball["y"] >= 500 - radius: # right
            ball["y"] = 500 - radius
            ball["vy"] = -ball["vy"] * bounce_factor
    
    for ball in balls:
        #pygame.draw.circle(screen,(color(RGB)), (coords), size of the circle)
        pygame.draw.circle(screen, (255,255,255), (int(ball["x"]), int(ball["y"])), radius)

    pygame.draw.line(screen,(255,255,255),(100,100),(700,100),2) # top
    pygame.draw.line(screen,(255,255,255),(100,500),(700,500),2) # bottom
    pygame.draw.line(screen,(255,255,255),(700,100),(700,500),2) # right
    pygame.draw.line(screen,(255,255,255),(100,100),(100,500),2) # left

    

    pygame.display.update()  # refresh screen

pygame.quit()
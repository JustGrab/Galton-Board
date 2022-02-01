import pygame
from pygame.color import *
import pymunk
from random import *
import time


#Colors
WHITE = (255,255,255)
GRAY = (33, 33, 33)
RED = (255,0,0)
BLACK = (0,0,0)
pygame.init()

WIDTH = 1100
HEIGHT = 1000
FPS = 144
B_RADIUS = 7.2
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galton Board")
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, 1000)

def convertPoints(point):
    return point[0], HEIGHT-point[1]

def createBall(space, radius, x,y):
   body = pymunk.Body(1,100,body_type = pymunk.Body.DYNAMIC)
   body.position = (x, y)
   shape = pymunk.Circle(body, radius)
   shape.color = (randint(1,255), randint(1,255), randint(1,255), 255)
   shape.elasticity = .1
   shape.density = 1
   shape.friction = 0.1
   space.add(body,shape)
   return shape

def drawBall(balls, color):
    for ball in balls:
        x,y = int(ball.body.position.x), int(ball.body.position.y)
        pygame.draw.circle(WINDOW, ball.color, (x,y), B_RADIUS)

def createBoard(x,y):
    walls = [pymunk.Segment(space.static_body, (0,y), (x,y), 5),
            pymunk.Segment(space.static_body, (0,0), (x,0), 5),
            pymunk.Segment(space.static_body, (0,0), (0,y), 6), 
            pymunk.Segment(space.static_body, (x,0), (x,y), 5),
            pymunk.Segment(space.static_body, (0,20), (x/2-(B_RADIUS*2.5),250), 5),
            pymunk.Segment(space.static_body, (x,25), (x/2+ (B_RADIUS*2.5), 250), 5)]

    for wall in walls:
        wall.elasticity = .1
        space.add(wall)

    return walls

def drawBoard(walls, x,y):
    for wall in walls:  
        pygame.draw.line(WINDOW, WHITE, wall.a, wall.b, 11)

def createCol(width, height, spacing):
    columns = []
    for col in range(0, int(WIDTH/ spacing)):
        columns.append(pymunk.Segment(space.static_body, (spacing * col,HEIGHT), (spacing * col, HEIGHT - height), width))
        columns[col].elasticity = 0.1
        space.add(columns[col])
    return columns

def drawCol(columns, width):
    for col in columns:
        pygame.draw.line(WINDOW, WHITE, col.a, col.b, width)

def createPegs(radius, spacing):
    pegs = []
    counter = 0
    for col in range(1, int(WIDTH/spacing)):
        for row in range(1, 9):
            if row % 2 == 1:
                pegs.append(pymunk.Circle(space.static_body, radius, (col * spacing , (HEIGHT/4) + (row * spacing)    )))
                pegs[counter].elasticity = 0.1
            else:
                pegs.append(pymunk.Circle(space.static_body, radius, (((col * spacing) + spacing / 2), (HEIGHT/4) + (row * spacing)    )))
                pegs[counter].elasticity = 0.1
            space.add(pegs[counter])
            counter +=1
    return pegs

def drawPegs(pegs):
    for peg in pegs:
        pygame.draw.circle(WINDOW, BLACK, (peg.offset), peg.radius)
        
if __name__ == "__main__" :

    balls = []
    walls = createBoard(WIDTH,HEIGHT)
    col = createCol(5, 275, 50)
    pegs = createPegs(16.4, 50.1)
    #drawBoard(walls, WIDTH, HEIGHT)
    for i in range(0,275):
    # balls.append(createBall(space, B_RADIUS, randint(0,WIDTH),randint(0,200)))
        balls.append(createBall(space, B_RADIUS, WIDTH/2, 0))

    run = True
    while(run):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        WINDOW.fill(GRAY)
        drawBoard(walls, WIDTH, HEIGHT)
        drawBall(balls, WHITE)
        drawCol(col, 8)
        drawPegs(pegs)
        #pygame.draw.line(WINDOW, BLACK, (WIDTH/2, 0), (WIDTH/2,HEIGHT), 5)
        pygame.display.update()
        space.step(1/FPS)
        clock.tick(FPS)
        #space.debug_draw(surface)
    pygame.quit()
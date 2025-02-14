import pygame
import numpy as np
import math
import random

G = 6.67430e-11

pygame.init()
screen = pygame.display.set_mode((1250, 1000))
pygame.display.set_caption("GRAVSIM v1.0 by Taj Entabi")
clock = pygame.time.Clock()

class Body:
    def __init__(self, mass, posX, posY, velX, velY, size):
        self.mass = mass
        self.posX = posX
        self.posY = posY
        self.velX = velX
        self.velY = velY
        self.accX = 0
        self.accY = 0
        self.size = size

    def update_acc(self, bodies):
        self.accX = 0
        self.accY = 0
        for body in bodies:
            if body is not self:
                dist = math.sqrt((body.posX - self.posX)**2 + (body.posY - self.posY)**2)
                if dist == 0:
                    continue
                mag = (G * body.mass) / dist**2
                theta = math.atan2(body.posY - self.posY, body.posX - self.posX)
                self.accX += mag * math.cos(theta)
                self.accY += mag * math.sin(theta)

    def update_pos(self, dt):
        self.velX += self.accX * dt
        self.velY += self.accY * dt
        self.posX += self.velX * dt
        self.posY += self.velY * dt

def circ_orbit(planet, sun, add=0, invert=False):
    r = abs(bodies[sun].posX - bodies[planet].posX)
    vel_circ = math.sqrt(G * bodies[sun].mass / r)
    if invert:
        bodies[planet].velY = -(vel_circ + add)
    else:
        bodies[planet].velY = vel_circ + add

bodies = [
    Body(1e16, 625, 500, 0, 0, 5)
]
e = 1
for i in range(0):
    bodies.append(Body(0, random.randint(400,500), random.randint(400,600), 0, 0, 1))
    circ_orbit(e,0,add=random.randint(-25,15))
    e += 1

running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                
    screen.fill((0, 0, 0))
    
    for body in bodies:
        body.update_acc(bodies)
        body.update_pos(dt)
        pygame.draw.circle(screen, (255, 255, 255), (body.posX, body.posY), body.size)
        
    pygame.display.update()

pygame.quit()

from itertools import count

import pygame
import math as m
import random

#Important Variables
running = True

# Initialize pygame
pygame.init()
# Set up display
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Soup")

# Define colors
#WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (155,155,155)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)


class Particles:
    def __init__(self, surface, size, color, count):
        self.surface = surface
        self.size = size
        self.color = color
        self.count = count

        self.x = [random.randint(0 + 50, WIDTH - 50) for i in range(self.count)]
        self.y = [random.randint(0 + 50, HEIGHT - 50) for j in range(self.count)]
        self.vx = [random.uniform(-1, 1) for i in range(self.count)]
        self.vy = [random.uniform(-1, 1) for j in range(self.count)]

    def draw(self):
        for p in range(self.count):
            pygame.draw.circle(self.surface, self.color, [self.x[p] , self.y[p]], self.size)

            #Update Position
            self.x[p] += self.vx[p]
            self.y[p] += self.vy[p]

            # Wall Collision
            if self.x[p] <= 0 or self.x[p] >= WIDTH:
                self.vx[p] *= -1
            if self.y[p] <= 0 or self.y[p] >= HEIGHT:
                self.vy[p] *= -1

    def rule(self, particle, g, interaction_radius = 700):

            for i in range(self.count):
                fx, fy = 0, 0 #Force Vector Component

                for j in range(particle.count):
                    dx = self.x[i] - particle.x[j]
                    dy = self.y[i] - particle.y[j]
                    dist = m.sqrt(dx**2 + dy**2)

                    if dist == 0 or dist > interaction_radius:
                        continue

                    force = g * (1/ (dist+0.0001))
                    fx += dx * force
                    fy += dy * force

                self.vx[i] += fx * 0.01
                self.vy[i] += fy * 0.01


#---------------------------------------------------------------------------------------------------------

red = Particles(screen, 5, RED, 100)
#blue = Particles(screen, 4, BLUE, 100)
#green = Particles(screen, 5, GREEN, 100)

clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)  # Clear the screen
    red.draw()
    #blue.draw()

    red.rule(red, -10)
    #red.rule(blue, -0.1)
    #blue.rule(red, 0.1)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Quit pygame
pygame.quit()
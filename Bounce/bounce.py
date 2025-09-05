import pygame
import random
import math as m

#Important Variables
running = True

# Initialize pygame
pygame.init()
# Set up display
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bounce")
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
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
        self.vy = [random.uniform(-2, 0) for j in range(self.count)]  # Start upward or zero

        self.gravity = 0.3
        self.damping = 0.7

    def draw(self):
        for b in range(self.count):
            pygame.draw.circle(self.surface, self.color, [self.x[b] , self.y[b]], self.size)

            # Apply gravity
            self.vy[b] += self.gravity

            #Update Position
            self.x[b] += self.vx[b]
            self.y[b] += self.vy[b]

            # Wall collision (left/right)
            if self.x[b] <= 0 or self.x[b] >= WIDTH:
                self.vx[b] *= -0.5

            # Floor collision
            if self.y[b] + self.size >= HEIGHT:
                self.y[b] = HEIGHT - self.size
                self.vy[b] = -self.vy[b] * self.damping  # Bounce back up with less energy

            # Optional: Ceiling collision
            #if self.y[b] <= 0:
                #self.y[b] = 0
                #self.vy[b] *= -0.5

    def interaction(self):
        for i in range(self.count):
            for j in range(i + 1, self.count):  # Only check each pair once
                dx = self.x[i] - self.x[j]
                dy = self.y[i] - self.y[j]
                dist = m.sqrt(dx ** 2 + dy ** 2)
                min_dist = self.size * 2

                if dist < min_dist and dist != 0:
                    # Normalize distance vector
                    nx = dx / dist
                    ny = dy / dist

                    # Move particles apart to avoid sticking
                    overlap = min_dist - dist
                    self.x[i] += nx * (overlap / 2)
                    self.y[i] += ny * (overlap / 2)
                    self.x[j] -= nx * (overlap / 2)
                    self.y[j] -= ny * (overlap / 2)

                    # Swap velocities (elastic collision)
                    self.vx[i], self.vx[j] = self.vx[j], self.vx[i]
                    self.vy[i], self.vy[j] = self.vy[j], self.vy[i]


blue = Particles(screen, 5, BLUE, 500)

while running:
    screen.fill(BLACK)  # Clear the screen
    blue.draw()
    #blue.interaction()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Quit pygame
pygame.quit()
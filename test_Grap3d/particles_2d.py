import pygame
import random
import math

pygame.init()


width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Partículas 3D")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Particle:
    def __init__(self, x, y, z, speed=1):  # Aqui estaba el problema
        self.x = x
        self.y = y
        self.z = z
        self.speed = speed
        self.size = random.randint(2, 5)

    def move(self):
        
        self.x += random.uniform(-self.speed, self.speed)
        self.y += random.uniform(-self.speed, self.speed)
        self.z += random.uniform(-self.speed, self.speed)

    def project(self):
        
        factor = 500 / (500 + self.z)  
        x_2d = self.x * factor + width // 2
        y_2d = self.y * factor + height // 2
        return int(x_2d), int(y_2d)

    def draw(self, screen):
        x_2d, y_2d = self.project()
        pygame.draw.circle(screen, WHITE, (x_2d, y_2d), self.size)


particles = [Particle(random.uniform(-1, 1) * 200, random.uniform(-1, 1) * 200, random.uniform(0, 500)) for _ in range(100)]


running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    for particle in particles:
        particle.move()
        particle.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
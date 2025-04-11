import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

# Copos de nieve
NUM_PARTICLES = 300
particles = []

def init_particles():
    for _ in range(NUM_PARTICLES):
        x = random.uniform(-5, 5)
        y = random.uniform(0, 10)
        z = random.uniform(-5, 5)
        speed = random.uniform(0.01, 0.05)
        particles.append([x, y, z, speed])

def draw_particle(x, y, z):
    size = 0.05
    glBegin(GL_QUADS)
    glVertex3f(x - size, y - size, z)
    glVertex3f(x + size, y - size, z)
    glVertex3f(x + size, y + size, z)
    glVertex3f(x - size, y + size, z)
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, -2.0, -15)

    glEnable(GL_DEPTH_TEST)
    glClearColor(0, 0, 0.1, 1)  # Fondo oscuro

    glColor3f(1, 1, 1)  # Blanco para los copos

    init_particles()
    clock = pygame.time.Clock()

    running = True
    while running:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        for p in particles:
            p[1] -= p[3]  # Caída
            if p[1] < -1:
                p[1] = 10
                p[0] = random.uniform(-5, 5)
                p[2] = random.uniform(-5, 5)
            draw_particle(p[0], p[1], p[2])

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

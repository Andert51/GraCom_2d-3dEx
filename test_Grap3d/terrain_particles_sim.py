import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random
from noise import pnoise2

# Config
width, height = 800, 600
terrain_size = 50
particle_count = 100

# Inicialización
pygame.init()
screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Terreno Procedural + Partículas 3D")
gluPerspective(45, (width / height), 0.1, 1000.0)
glTranslatef(0.0, -10.0, -100)
glEnable(GL_DEPTH_TEST)

# Generar terreno procedural con ruido Perlin
def generate_terrain(size, scale=5, height_scale=8):
    vertices = []
    for x in range(size):
        row = []
        for z in range(size):
            y = pnoise2(x * 0.1, z * 0.1) * height_scale
            row.append([x * scale, y, z * scale])
        vertices.append(row)
    return vertices

# Dibujar malla del terreno
def draw_terrain(terrain):
    glColor3f(0.2, 0.8, 0.2)
    for x in range(len(terrain) - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for z in range(len(terrain[0])):
            glVertex3fv(terrain[x][z])
            glVertex3fv(terrain[x+1][z])
        glEnd()

# Partículas
class Particle:
    def __init__(self):
        self.x = random.uniform(-30, 30)
        self.y = random.uniform(10, 30)
        self.z = random.uniform(-30, 30)
        self.dx = random.uniform(-0.2, 0.2)
        self.dy = random.uniform(-0.2, 0.2)
        self.dz = random.uniform(-0.2, 0.2)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz
        # Rebotar
        if self.y < 0 or self.y > 40:
            self.dy *= -1

    def draw(self):
        glColor3f(1, 1, 1)
        glPointSize(5)
        glBegin(GL_POINTS)
        glVertex3f(self.x, self.y, self.z)
        glEnd()

# Inicializar objetos
terrain = generate_terrain(terrain_size)
particles = [Particle() for _ in range(particle_count)]

# Bucle principal
running = True
angle = 0
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Rotar la escena lentamente
    glPushMatrix()
    glRotatef(angle, 0, 1, 0)
    draw_terrain(terrain)

    for p in particles:
        p.update()
        p.draw()

    glPopMatrix()

    angle += 0.2
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

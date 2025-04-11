from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# Piso blanco
ground = Entity(model='plane', scale=(100, 1, 100), color=color.white, texture='white_cube', texture_scale=(100, 100), collider='box')

# Jugador
player = FirstPersonController()
player.gravity = 0
player.y = 2

# Nieve
snow_particles = []
for _ in range(300):
    x = random.uniform(-50, 50)
    y = random.uniform(5, 25)
    z = random.uniform(-50, 50)
    particle = Entity(model='sphere', scale=0.05, color=color.white, position=(x, y, z))
    snow_particles.append(particle)

def update():
    # Mover con flechas además de WASD
    move_speed = 5 * time.dt
    if held_keys['up arrow']: player.position += player.forward * move_speed
    if held_keys['down arrow']: player.position -= player.forward * move_speed
    if held_keys['left arrow']: player.position -= player.right * move_speed
    if held_keys['right arrow']: player.position += player.right * move_speed

    # Cerrar con tecla X
    if held_keys['x']:
        application.quit()

    # Nieve cayendo
    for p in snow_particles:
        p.y -= time.dt * 1.5
        if p.y < 0:
            p.x = random.uniform(player.x - 25, player.x + 25)
            p.y = random.uniform(10, 25)
            p.z = random.uniform(player.z - 25, player.z + 25)

app.run()

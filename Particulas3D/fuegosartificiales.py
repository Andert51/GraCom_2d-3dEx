from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# Fondo negro y piso gris claro
window.color = color.black
camera.clip_plane_near = 0.01

# Piso gris claro
ground = Entity(model='plane', scale=(100, 1, 100), color=color.gray, collider='box')

# Jugador
player = FirstPersonController()
player.gravity = 0
player.y = 2  # Altura inicial del jugador

# Lista de colores brillantes (sin tint())
bright_colors = [
    color.red, color.green, color.blue, color.yellow,
    color.orange, color.magenta, color.cyan, color.azure,
    color.lime, color.white
]

# Lista de fuegos artificiales
fireworks = []

# Cargar dos sonidos de explosión
explosion_sound_1 = Audio('explosion_sound_1', loop=False, autoplay=False)
explosion_sound_2 = Audio('explosion_sound_2', loop=False, autoplay=False)

def create_dotted_firework():
    origin = Vec3(player.x + random.uniform(-10, 10), 0, player.z + random.uniform(-10, 10))
    peak = random.uniform(15, 25)
    explosion = []

    # Elegimos dos colores aleatorios para cada fuego artificial
    color1, color2 = random.sample(bright_colors, 2)

    for _ in range(60):  # 60 rayos punteados
        direction = Vec3(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)).normalized()
        start = origin + Vec3(0, peak, 0)
        length = random.uniform(4, 7)
        segments = []

        for i in range(6):  # 6 puntos por rayo
            pos = start + direction * (i * (length / 6))
            # Alternamos entre color1 y color2
            color_random = color1 if i % 2 == 0 else color2
            dot = Entity(
                model='sphere',
                scale=0.2,
                color=color_random,
                position=pos,
                add_to_scene_entities=False
            )
            is_last = (i == 5)
            segments.append((dot, direction, is_last))
        explosion.append(segments)
    
    fireworks.append(explosion)

    # Reproducir un sonido de explosión aleatorio
    if random.choice([True, False]):
        explosion_sound_1.play()
    else:
        explosion_sound_2.play()

# Temporizador
firework_timer = 0

def update():
    global firework_timer

    # Movimiento con flechas además de WASD
    move_speed = 5 * time.dt
    if held_keys['up arrow']: player.position += player.forward * move_speed
    if held_keys['down arrow']: player.position -= player.forward * move_speed
    if held_keys['left arrow']: player.position -= player.right * move_speed
    if held_keys['right arrow']: player.position += player.right * move_speed

    # Subir con la barra espaciadora
    if held_keys['space']:
        player.y += 1 * time.dt  # Subir continuamente con la barra espaciadora

    # Salir con X
    if held_keys['x']:
        application.quit()

    # Lanzamiento automático
    firework_timer -= time.dt
    if firework_timer <= 0:
        create_dotted_firework()
        firework_timer = random.uniform(1.0, 2.0)

    # Animación
    for explosion in fireworks:
        for segment in explosion:
            for p, dir, is_last in segment:
                p.position += dir * time.dt * 2.2
                if is_last:
                    p.position += Vec3(0, -0.4 * time.dt, 0)

                # Desvanecimiento lento (aprox 30s)
                p.color = color.rgba(p.color.r, p.color.g, p.color.b, max(p.color.a - 1 * time.dt, 0))
                p.scale *= 0.999  # Escalado mínimo
                if p.color.a <= 0.01:
                    destroy(p)
        explosion[:] = [s for s in explosion if any(p.color.a > 0.01 for p, _, _ in s)]
    fireworks[:] = [e for e in fireworks if len(e) > 0]

app.run()

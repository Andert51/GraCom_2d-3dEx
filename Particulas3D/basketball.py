from ursina import *
import random

app = Ursina()

window.color = color.black  # Fondo general negro
window.size = (1464, 936)

# Fondo con imagen
background = Entity(
    model='quad',
    texture='assets/gym_background.jpg',
    scale=(40, 20),
    position=(0, 5, 20),
    double_sided=True
)

# Crear el piso de la cancha con textura de madera
wood_texture = load_texture('assets/wood_texture.jpg')  # Debes tener esta textura también
floor = Entity(model='plane', scale=(20, 1, 20), texture=wood_texture, position=(0, -2, 0), collider='box')

# Líneas de la cancha
court_lines = [
    Entity(model='plane', scale=(20, 1, 1), color=color.white, position=(0, -1.99, 10)),
    Entity(model='plane', scale=(20, 1, 1), color=color.white, position=(0, -1.99, -10)),
    Entity(model='plane', scale=(1, 1, 20), color=color.white, position=(10, -1.99, 0)),
    Entity(model='plane', scale=(1, 1, 20), color=color.white, position=(-10, -1.99, 0)),
    Entity(model='plane', scale=(1, 1, 20), color=color.white, position=(0, -1.99, 0))
]

# Crear canasta con aro visible y bien formada
def create_hoop(position):
    # Tablero con textura de imagen
    backboard = Entity(
        model='cube',
        scale=(2, 1.2, 0.1),
        texture='assets/backboard_texture.jpg',  # Asegúrate de tener esta imagen en la carpeta assets
        position=position + Vec3(0, 3.5, -0.6)
    )

    # Soporte
    pole = Entity(model='cube', scale=(0.2, 4, 0.2), color=color.gray, position=position + Vec3(0, 1, 0))

    return [backboard, pole]

# Crear dos canastas
create_hoop(Vec3(7, -2, 5))
create_hoop(Vec3(-7, -2, 5))

# Pelotas de baloncesto
balls = []

def create_ball():
    x = random.uniform(-8, 8)
    z = random.uniform(-8, 8)
    ball = Entity(
        model='sphere',
        scale=1,
        color=color.orange,
        texture='basketball',  # Asegúrate de tener esta textura
        position=(x, 10, z),
        collider='sphere'
    )
    ball.velocity = Vec3(0, -random.uniform(15, 20), 0)
    balls.append(ball)

ball_timer = 0.0

def update():
    global ball_timer

    # Lanzamiento de balones
    ball_timer -= time.dt
    if ball_timer <= 0:
        create_ball()
        ball_timer = 0.25

    # Movimiento de pelotas
    for ball in balls:
        ball.position += ball.velocity * time.dt
        ball.velocity.y -= 0.1  # gravedad

        if ball.position.y <= 0:
            ball.position.y = 0
            ball.velocity.y = random.uniform(4, 6)
            ball.velocity *= 0.9

    # Movimiento de cámara
    speed = 2.0
    if held_keys['w'] or held_keys['up arrow']:
        camera.position += camera.forward * speed * time.dt
    if held_keys['s'] or held_keys['down arrow']:
        camera.position -= camera.forward * speed * time.dt
    if held_keys['a'] or held_keys['left arrow']:
        camera.position -= camera.right * speed * time.dt
    if held_keys['d'] or held_keys['right arrow']:
        camera.position += camera.right * speed * time.dt
    if held_keys['space']:
        camera.position += camera.up * speed * time.dt
    if held_keys['enter']:
        camera.position -= camera.up * speed * time.dt

    # Movimiento de cámara más suave
    camera.rotation_y += mouse.x * 0.1 * 1.5
    camera.rotation_x -= mouse.y * 0.1 * 1.5

    # Zoom
    if held_keys['+']:
        camera.fov = max(5, camera.fov - 0.5)
    if held_keys['-']:
        camera.fov = min(100, camera.fov + 0.5)

    # Salida
    if held_keys['x']:
        application.quit()

app.run()

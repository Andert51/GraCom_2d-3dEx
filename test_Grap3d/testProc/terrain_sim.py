import glfw
import moderngl
import numpy as np
from pyrr import Matrix44, Vector3
from noise import pnoise2
import time
import os

# Configuración inicial
WIDTH, HEIGHT = 1280, 720

# Generación procedural del terreno
def generate_terrain(size=100, scale=1.0, height_scale=10.0, freq=0.1):
    vertices = []
    normals = []

    for z in range(size):
        for x in range(size):
            y = pnoise2(x * freq, z * freq, octaves=4) * height_scale
            vertices.append([x * scale, y, z * scale])
            normals.append([0.0, 1.0, 0.0])  # temporal

    vertices = np.array(vertices, dtype='f4')
    normals = np.array(normals, dtype='f4')

    indices = []
    for z in range(size - 1):
        for x in range(size - 1):
            top_left = z * size + x
            top_right = top_left + 1
            bottom_left = (z + 1) * size + x
            bottom_right = bottom_left + 1

            indices.extend([top_left, bottom_left, top_right])
            indices.extend([top_right, bottom_left, bottom_right])

    return vertices, normals, np.array(indices, dtype='i4')

# Main
class TerrainApp:
    def __init__(self):
        if not glfw.init():
            raise Exception("GLFW initialization failed")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        self.window = glfw.create_window(WIDTH, HEIGHT, "Generación Procedural 3D", None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window creation failed")

        glfw.make_context_current(self.window)
        self.ctx = moderngl.create_context()

        self.last_time = time.time()
        self.angle_x, self.angle_y = 0, 0
        self.zoom = 200

        self.init_scene()

    def init_scene(self):
        # Cargar shaders
        with open("shaders/terrain.vert") as f:
            vertex_shader = f.read()
        with open("shaders/terrain.frag") as f:
            fragment_shader = f.read()

        self.program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        # Generar malla de terreno
        vertices, normals, indices = generate_terrain()
        self.vbo = self.ctx.buffer(np.hstack([vertices, normals]).astype('f4').tobytes())
        self.ibo = self.ctx.buffer(indices.tobytes())

        self.vao = self.ctx.vertex_array(
            self.program,
            [
                (self.vbo, '3f 3f', 'in_position', 'in_normal'),
            ],
            self.ibo
        )

        self.model = Matrix44.identity()
        self.program['model'].write(self.model.astype('f4').tobytes())

    def update_camera(self):
        view = Matrix44.look_at(
            eye=Vector3([self.zoom * np.sin(self.angle_y) * np.cos(self.angle_x),
                         self.zoom * np.sin(self.angle_x),
                         self.zoom * np.cos(self.angle_y) * np.cos(self.angle_x)]),
            target=Vector3([50, 0, 50]),
            up=Vector3([0, 1, 0])
        )
        proj = Matrix44.perspective_projection(45.0, WIDTH / HEIGHT, 0.1, 1000.0)

        self.program['view'].write(view.astype('f4').tobytes())
        self.program['projection'].write(proj.astype('f4').tobytes())
        self.program['light_pos'].value = (100.0, 100.0, 100.0)
        self.program['view_pos'].value = tuple(view.inverse[:3, 3])
        self.program['light_color'].value = (1.0, 1.0, 1.0)
        self.program['object_color'].value = (0.3, 0.7, 0.3)

    def run(self):
        while not glfw.window_should_close(self.window):
            glfw.poll_events()

            # Control simple de cámara
            if glfw.get_key(self.window, glfw.KEY_LEFT) == glfw.PRESS:
                self.angle_y -= 0.01
            if glfw.get_key(self.window, glfw.KEY_RIGHT) == glfw.PRESS:
                self.angle_y += 0.01
            if glfw.get_key(self.window, glfw.KEY_UP) == glfw.PRESS:
                self.angle_x += 0.01
            if glfw.get_key(self.window, glfw.KEY_DOWN) == glfw.PRESS:
                self.angle_x -= 0.01
            if glfw.get_key(self.window, glfw.KEY_W) == glfw.PRESS:
                self.zoom -= 2
            if glfw.get_key(self.window, glfw.KEY_S) == glfw.PRESS:
                self.zoom += 2

            self.ctx.clear(0.1, 0.2, 0.3)
            self.ctx.enable(moderngl.DEPTH_TEST)

            self.update_camera()
            self.vao.render()

            glfw.swap_buffers(self.window)

        glfw.terminate()

if __name__ == "__main__":
    os.environ["DISPLAY"] = ":0"
    os.environ["XDG_SESSION_TYPE"] = "x11"
    app = TerrainApp()
    app.run()

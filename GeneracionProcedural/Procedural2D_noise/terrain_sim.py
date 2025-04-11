import glfw
import moderngl
import numpy as np
from pyrr import Matrix44, Vector3
from noise import pnoise2
import time
import os
import random

WIDTH, HEIGHT = 1280, 720

def generate_terrain(size=100, scale=1.0, height_scale=10.0, freq=0.1):
    seed = random.randint(0, 1000)
    vertices, normals = [], []
    for z in range(size):
        for x in range(size):
            # Desplazamiento aleatorio para que siempre sea diferente
            y = pnoise2((x + seed) * freq, (z + seed) * freq, octaves=4) * height_scale + 4.0
            vertices.append([x * scale, y, z * scale])
            normals.append([0.0, 1.0, 0.0])
    vertices = np.array(vertices, dtype='f4')
    normals = np.array(normals, dtype='f4')

    indices = []
    for z in range(size - 1):
        for x in range(size - 1):
            tl = z * size + x
            tr = tl + 1
            bl = (z + 1) * size + x
            br = bl + 1
            indices.extend([tl, bl, tr, tr, bl, br])

    return vertices, normals, np.array(indices, dtype='i4')

class ParticleSystem:
    def __init__(self, ctx, shader, num_particles=3000):
        self.ctx = ctx
        self.shader = shader
        self.num = num_particles
        self.positions = np.random.uniform(0, 100, (num_particles, 3)).astype('f4')
        self.positions[:, 1] += np.random.uniform(15, 25, num_particles)  # más altura variable

        self.velocities = np.random.uniform(-0.005, 0.005, (num_particles, 3)).astype('f4')

        self.vbo = ctx.buffer(self.positions.tobytes())
        self.vao = ctx.simple_vertex_array(self.shader, self.vbo, 'in_position')

    def update(self):
        self.positions += self.velocities
        self.positions[:, 1] = np.where(self.positions[:, 1] > 30, 15, self.positions[:, 1])
        self.vbo.write(self.positions.tobytes())

    def render(self):
        self.vao.render(mode=moderngl.POINTS)

class TerrainApp:
    def __init__(self):
        if not glfw.init():
            raise Exception("GLFW init failed")
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        self.window = glfw.create_window(WIDTH, HEIGHT, "Terreno Procedural Realista", None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("Ventana GLFW falló")
        glfw.make_context_current(self.window)
        self.ctx = moderngl.create_context()

        self.angle_x, self.angle_y = 0, 0
        self.zoom = 200
        self.last_time = time.time()

        self.init_scene()

    def load_shader(self, name):
        with open(f"shaders/{name}.vert") as v, open(f"shaders/{name}.frag") as f:
            return self.ctx.program(vertex_shader=v.read(), fragment_shader=f.read())

    def init_scene(self):
        # Terreno
        self.terrain_prog = self.load_shader("terrain")
        verts, norms, indices = generate_terrain()
        self.vbo = self.ctx.buffer(np.hstack([verts, norms]).astype('f4').tobytes())
        self.ibo = self.ctx.buffer(indices.tobytes())
        self.vao = self.ctx.vertex_array(
            self.terrain_prog,
            [(self.vbo, '3f 3f', 'in_position', 'in_normal')],
            self.ibo
        )

        self.terrain_prog['model'].write(Matrix44.identity(dtype='f4'))

        # Partículas
        self.particle_prog = self.load_shader("particle")
        self.particle_prog['model'].write(Matrix44.identity(dtype='f4'))
        self.particles = ParticleSystem(self.ctx, self.particle_prog)

    def update_camera(self):
        eye = Vector3([
            self.zoom * np.sin(self.angle_y) * np.cos(self.angle_x),
            self.zoom * np.sin(self.angle_x),
            self.zoom * np.cos(self.angle_y) * np.cos(self.angle_x)
        ])
        view = Matrix44.look_at(eye, Vector3([50, 0, 50]), Vector3([0, 1, 0]))
        proj = Matrix44.perspective_projection(45.0, WIDTH / HEIGHT, 0.1, 1000.0)

        for prog in [self.terrain_prog, self.particle_prog]:
            prog['view'].write(view.astype('f4').tobytes())
            prog['projection'].write(proj.astype('f4').tobytes())

        self.terrain_prog['light_pos'].value = (100.0, 100.0, 100.0)
        self.terrain_prog['view_pos'].value = tuple(eye)
        self.terrain_prog['light_color'].value = (1.0, 1.0, 1.0)

    def run(self):
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
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
            self.particles.update()
            self.particles.render()

            glfw.swap_buffers(self.window)

        glfw.terminate()

if __name__ == "__main__":
    os.environ["DISPLAY"] = ":0"
    os.environ["XDG_SESSION_TYPE"] = "x11"
    TerrainApp().run()
    os.environ["DISPLAY"] = ":0"
    os.environ["XDG_SESSION_TYPE"] = "x11"

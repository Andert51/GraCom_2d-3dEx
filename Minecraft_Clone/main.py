from settings import *  # Importa configuraciones globales del proyecto
import moderngl as mgl  # Biblioteca para renderizado moderno en OpenGL
import pygame as pg  # Biblioteca para manejo de ventanas, eventos y gráficos
import sys  # Biblioteca para manejar la salida del programa
from shader_program import ShaderProgram  # Clase para manejar los shaders
from scene import Scene  # Clase que representa la escena del juego
from player import Player  # Clase que representa al jugador
from textures import Textures  # Clase para manejar las texturas del juego


class VoxelEngine:
    """
    Clase principal del motor voxel.

    Esta clase inicializa y maneja todos los componentes del motor, incluyendo
    la ventana, el contexto de OpenGL, el jugador, las texturas, los shaders y la escena.
    También gestiona el ciclo principal del juego (eventos, actualización y renderizado).

    Atributos:
        ctx (mgl.Context): Contexto de OpenGL para renderizado.
        clock (pg.time.Clock): Reloj para medir el tiempo entre frames.
        delta_time (float): Tiempo transcurrido entre el frame actual y el anterior.
        time (float): Tiempo total transcurrido desde el inicio del programa.
        is_running (bool): Indica si el motor está en ejecución.
        textures (Textures): Maneja las texturas del juego.
        player (Player): Representa al jugador en el mundo.
        shader_program (ShaderProgram): Maneja los shaders del juego.
        scene (Scene): Representa la escena del juego.
    """

    def __init__(self):
        """
        Inicializa el motor voxel.

        Configura la ventana, el contexto de OpenGL y los atributos iniciales del motor.
        """
        # Inicializa Pygame
        pg.init()

        # Configura los atributos del contexto de OpenGL
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, VERSION_MAYOR)  # Versión mayor de OpenGL
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, VERSION_MENOR)  # Versión menor de OpenGL
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)  # Perfil de OpenGL
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, TAMANO_PROFUNDIDAD)  # Tamaño del buffer de profundidad
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, MUESTRAS_ANTIALIASING)  # Antialiasing

        # Crea la ventana con soporte para OpenGL y doble buffer
        pg.display.set_mode(RESOLUCION_VENTANA, flags=pg.OPENGL | pg.DOUBLEBUF)

        # Crea el contexto de OpenGL
        self.ctx = mgl.create_context()

        # Habilita características de OpenGL
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)  # Prueba de profundidad, culling y blending
        self.ctx.gc_mode = 'auto'  # Modo de recolección de basura automática para OpenGL

        # Inicializa el reloj y variables de tiempo
        self.clock = pg.time.Clock()
        self.delta_time = 0  # Tiempo entre frames
        self.time = 0  # Tiempo total transcurrido

        # Configura el cursor y captura del mouse
        pg.event.set_grab(True)  # Captura el cursor dentro de la ventana
        pg.mouse.set_visible(False)  # Oculta el cursor

        # Estado del motor
        self.is_running = True

        # Inicializa los componentes del motor
        self.on_init()

    def on_init(self):
        """
        Inicializa los componentes principales del motor.

        Carga las texturas, inicializa al jugador, los shaders y la escena.
        """
        self.textures = Textures(self)  # Carga y maneja las texturas
        self.player = Player(self)  # Inicializa al jugador
        self.shader_program = ShaderProgram(self)  # Carga y maneja los shaders
        self.scene = Scene(self)  # Inicializa la escena del juego

    def update(self):
        """
        Actualiza el estado del motor.

        Llama a los métodos de actualización de los componentes principales
        y calcula el tiempo transcurrido entre frames.
        """
        self.player.update()  # Actualiza al jugador
        self.shader_program.update()  # Actualiza los shaders
        self.scene.update()  # Actualiza la escena

        # Calcula el tiempo entre frames y el tiempo total transcurrido
        self.delta_time = self.clock.tick() / 1000.0  # Tiempo entre frames en segundos
        self.time = pg.time.get_ticks() * 0.001  # Tiempo total en segundos

        # Actualiza el título de la ventana con los FPS actuales
        pg.display.set_caption(f'{self.clock.get_fps():.0f} FPS')

    def render(self):
        """
        Renderiza la escena del juego.

        Limpia el buffer de color y profundidad, renderiza la escena y actualiza la ventana.
        """
        self.ctx.clear(color=COLOR_FONDO)  # Limpia la pantalla con el color de fondo
        self.scene.render()  # Renderiza la escena
        pg.display.flip()  # Actualiza el contenido de la ventana

    def handle_events(self):
        """
        Maneja los eventos de entrada del usuario.

        Procesa eventos como cerrar la ventana, presionar teclas o mover el mouse.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.is_running = False  # Detiene el motor si se cierra la ventana o se presiona ESC
            self.player.handle_event(event=event)  # Pasa el evento al jugador para manejarlo

    def run(self):
        """
        Ejecuta el ciclo principal del motor.

        El ciclo principal incluye manejar eventos, actualizar el estado y renderizar la escena.
        """
        while self.is_running:
            self.handle_events()  # Maneja los eventos de entrada
            self.update()  # Actualiza el estado del motor
            self.render()  # Renderiza la escena

        # Finaliza Pygame y cierra el programa
        pg.quit()
        sys.exit()


if __name__ == '__main__':
    # Punto de entrada del programa
    app = VoxelEngine()  # Crea una instancia del motor voxel
    app.run()  # Ejecuta el motor
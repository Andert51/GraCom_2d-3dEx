from object_3d import * # Importa las clases necesarias para la gestión de objetos 3D
from camera import * # Importa las clases necesarias para la gestión de objetos 3D y cámara
from projection import * # Importa las clases necesarias para la gestión de objetos 3D, cámara y proyección
import pygame as pg # Importa la biblioteca Pygame para la gestión de gráficos y eventos
import math # Importa la biblioteca de matemáticas para cálculos trigonométricos y constantes

"""
Este módulo contiene la clase principal `SoftwareRender`, que gestiona el ciclo de renderizado,
la carga de objetos 3D desde archivos y la interacción con la cámara.
"""

class SoftwareRender:
    """
    Clase principal para gestionar el renderizado de objetos 3D en un entorno 2D.
    """

    def __init__(self):
        """
        Inicializa el entorno de renderizado, incluyendo la ventana, la cámara y los objetos.
        """
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900  # Resolución de la ventana
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2  # Mitades de la resolución
        self.FPS = 60  # Fotogramas por segundo
        self.screen = pg.display.set_mode(self.RES)  # Configuración de la ventana
        self.clock = pg.time.Clock()  # Reloj para controlar el FPS
        self.create_objects()  # Inicialización de los objetos

    def create_objects(self):
        """
        Crea e inicializa los objetos necesarios para el renderizado, como la cámara y los objetos 3D.
        """
        self.camera = Camera(self, [-5, 6, -55])  # Inicializa la cámara con una posición inicial
        self.projection = Projection(self)  # Inicializa la proyección
        self.object = self.get_object_from_file('resources/cow-nonormals.obj')  # Carga un objeto 3D desde un archivo
        self.object.rotate_y(-math.pi / 4)  # Aplica una rotación inicial al objeto

    def get_object_from_file(self, filename):
        """
        Carga un objeto 3D desde un archivo en formato OBJ.

        :param filename: Ruta del archivo OBJ.
        :return: Instancia de `Object3D` con los vértices y caras cargados.
        """
        vertex, faces = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):  # Línea que define un vértice
                    vertex.append([float(i) for i in line.split()[1:]] + [1])  # Convierte los vértices a coordenadas homogéneas
                elif line.startswith('f'):  # Línea que define una cara
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])  # Convierte las caras a índices de vértices
        return Object3D(self, vertex, faces)  # Devuelve el objeto 3D creado

    def draw(self):
        """
        Dibuja el contenido en la pantalla, incluyendo el fondo y los objetos 3D.
        """
        self.screen.fill(pg.Color('darkslategray'))  # Rellena el fondo con un color
        self.object.draw()  # Dibuja el objeto 3D

    def run(self):
        """
        Inicia el bucle principal del programa, gestionando el renderizado y los eventos.
        """
        while True:
            self.draw()  # Dibuja el contenido en la pantalla
            self.camera.control()  # Controla el movimiento de la cámara
            [exit() for i in pg.event.get() if i.type == pg.QUIT]  # Detecta si se cierra la ventana
            pg.display.set_caption(str(self.clock.get_fps()))  # Muestra el FPS en el título de la ventana
            pg.display.flip()  # Actualiza la pantalla
            self.clock.tick(self.FPS)  # Controla el FPS del programa


if __name__ == '__main__':
    """
    Punto de entrada del programa. Crea una instancia de `SoftwareRender` y ejecuta el bucle principal.
    """
    app = SoftwareRender()
    app.run()
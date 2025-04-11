import pygame as pg # Importa la biblioteca Pygame para la gestión de gráficos y eventos
from matrix_functions import * # Importa funciones de transformación de matrices
from numba import njit # Importa la biblioteca Numba para optimización de código

"""
Este módulo define clases para representar y manipular objetos 3D en un entorno gráfico.
Incluye transformaciones como traslación, rotación y escalado, así como la proyección en pantalla.
"""

@njit(fastmath=True)
def any_func(arr, a, b):
    """
    Verifica si algún elemento de un arreglo coincide con los valores dados.

    :param arr: Arreglo de entrada.
    :param a: Primer valor a comparar.
    :param b: Segundo valor a comparar.
    :return: True si algún elemento coincide, False en caso contrario.
    """
    return np.any((arr == a) | (arr == b))


class Object3D:
    """
    Clase base para representar un objeto 3D.
    Permite aplicar transformaciones y proyectar el objeto en la pantalla.
    """

    def __init__(self, render, vertices='', faces=''):
        """
        Inicializa un objeto 3D con vértices y caras opcionales.

        :param render: Objeto de renderizado que contiene información de la pantalla y la cámara.
        :param vertices: Lista de vértices del objeto (opcional).
        :param faces: Lista de caras del objeto (opcional).
        """
        self.render = render
        self.vertices = np.array(vertices)
        self.faces = faces
        self.translate([0.0001, 0.0001, 0.0001])  # Evita errores con matrices vacías

        # Configuración de visualización
        self.font = pg.font.SysFont('Arial', 30, bold=True)
        self.color_faces = [(pg.Color('orange'), face) for face in self.faces]
        self.movement_flag = True  # Indica si el objeto debe moverse automáticamente
        self.draw_vertices = False  # Indica si se deben dibujar los vértices
        self.label = ''  # Etiqueta opcional para las caras del objeto

    def draw(self):
        """
        Dibuja el objeto en la pantalla aplicando proyección y movimiento.
        """
        self.screen_projection()
        self.movement()

    def movement(self):
        """
        Aplica un movimiento automático al objeto si está habilitado.
        En este caso, rota el objeto continuamente alrededor del eje Y.
        """
        if self.movement_flag:
            self.rotate_y(-(pg.time.get_ticks() % 0.005))

    def screen_projection(self):
        """
        Proyecta el objeto en la pantalla aplicando las matrices de transformación y proyección.
        """
        # Transformación de los vértices
        vertices = self.vertices @ self.render.camera.camera_matrix() # Aplicación de la matriz de la cámara
        vertices = vertices @ self.render.projection.projection_matrix # Aplicación de la matriz de proyección
        vertices /= vertices[:, -1].reshape(-1, 1)  # Normalización en coordenadas homogéneas
        vertices[(vertices > 2) | (vertices < -2)] = 0  # Clipping
        vertices = vertices @ self.render.projection.to_screen_matrix
        vertices = vertices[:, :2]  # Conversión a coordenadas 2D

        # Dibujo de las caras
        for index, color_face in enumerate(self.color_faces): 
            color, face = color_face # Desempaquetar color y cara
            polygon = vertices[face] # Obtener los vértices de la cara
            if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT): 
                pg.draw.polygon(self.render.screen, color, polygon, 1) # Dibujo de la cara
                if self.label: # Si hay etiqueta, dibujarla
                    text = self.font.render(self.label[index], True, pg.Color('white')) 
                    self.render.screen.blit(text, polygon[-1]) # Dibujo de la etiqueta

        # Dibujo de los vértices
        if self.draw_vertices: # Si se habilita el dibujo de vértices
            for vertex in vertices: # Iterar sobre los vértices
                if not any_func(vertex, self.render.H_WIDTH, self.render.H_HEIGHT): 
                    pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 2) # Dibujo del vértice

    # Métodos de transformación
    def translate(self, pos):
        """
        Aplica una traslación al objeto.

        :param pos: Lista o tupla con los valores de traslación (x, y, z).
        """
        self.vertices = self.vertices @ translate(pos)

    def scale(self, scale_to):
        """
        Aplica un escalado uniforme al objeto.

        :param scale_to: Factor de escalado.
        """
        self.vertices = self.vertices @ scale(scale_to)

    def rotate_x(self, angle):
        """
        Aplica una rotación alrededor del eje X.

        :param angle: Ángulo de rotación en radianes.
        """
        self.vertices = self.vertices @ rotate_x(angle)

    def rotate_y(self, angle):
        """
        Aplica una rotación alrededor del eje Y.

        :param angle: Ángulo de rotación en radianes.
        """
        self.vertices = self.vertices @ rotate_y(angle)

    def rotate_z(self, angle):
        """
        Aplica una rotación alrededor del eje Z.

        :param angle: Ángulo de rotación en radianes.
        """
        self.vertices = self.vertices @ rotate_z(angle)


class Axes(Object3D):
    """
    Clase que representa los ejes XYZ en un espacio 3D.
    Hereda de Object3D y define los vértices y caras para los ejes.
    """

    def __init__(self, render):
        """
        Inicializa los ejes XYZ con colores y etiquetas.

        :param render: Objeto de renderizado que contiene información de la pantalla y la cámara.
        """
        super().__init__(render)
        self.vertices = np.array([
            (0, 0, 0, 1),  # Origen
            (1, 0, 0, 1),  # Eje X
            (0, 1, 0, 1),  # Eje Y
            (0, 0, 1, 1)   # Eje Z
        ])
        self.faces = np.array([
            (0, 1),  # Línea del origen al eje X
            (0, 2),  # Línea del origen al eje Y
            (0, 3)   # Línea del origen al eje Z
        ])
        self.colors = [
            pg.Color('red'),   # Color del eje X
            pg.Color('green'), # Color del eje Y
            pg.Color('blue')   # Color del eje Z
        ]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertices = False  # No dibujar vértices por defecto
        self.label = 'XYZ'  # Etiqueta para los ejes
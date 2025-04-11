import math # Importa la biblioteca math para funciones matemáticas
import numpy as np # Importa la biblioteca NumPy para operaciones matemáticas y matrices

"""
Este módulo define la clase Projection, que se encarga de calcular las matrices de proyección
y transformación necesarias para renderizar objetos 3D en un espacio 2D (pantalla).
"""

class Projection:
    """
    Clase Projection que calcula las matrices de proyección y transformación de pantalla.
    """

    def __init__(self, render):
        """
        Inicializa la clase Projection y calcula las matrices de proyección y transformación.

        :param render: Objeto de renderizado que contiene información de la cámara y la pantalla.
        """
        # Parámetros de la cámara
        NEAR = render.camera.near_plane  # Plano cercano
        FAR = render.camera.far_plane  # Plano lejano
        RIGHT = math.tan(render.camera.h_fov / 2)  # Extremo derecho del campo de visión horizontal
        LEFT = -RIGHT  # Extremo izquierdo del campo de visión horizontal
        TOP = math.tan(render.camera.v_fov / 2)  # Extremo superior del campo de visión vertical
        BOTTOM = -TOP  # Extremo inferior del campo de visión vertical

        # Cálculo de la matriz de proyección
        m00 = 2 / (RIGHT - LEFT)  # Escalado horizontal
        m11 = 2 / (TOP - BOTTOM)  # Escalado vertical
        m22 = (FAR + NEAR) / (FAR - NEAR)  # Relación de profundidad
        m32 = -2 * NEAR * FAR / (FAR - NEAR)  # Traslación en el eje Z
        self.projection_matrix = np.array([
            [m00, 0, 0, 0],
            [0, m11, 0, 0],
            [0, 0, m22, 1],
            [0, 0, m32, 0]
        ])
        """
        Matriz de proyección:
        - Convierte las coordenadas 3D en coordenadas normalizadas para la proyección en pantalla.
        - Incluye escalado y traslación en función de los planos de recorte (NEAR y FAR).
        """

        # Cálculo de la matriz de transformación a coordenadas de pantalla
        HW, HH = render.H_WIDTH, render.H_HEIGHT  # Mitad del ancho y alto de la pantalla
        self.to_screen_matrix = np.array([
            [HW, 0, 0, 0],
            [0, -HH, 0, 0],
            [0, 0, 1, 0],
            [HW, HH, 0, 1]
        ])
        """
        Matriz de transformación a pantalla:
        - Convierte las coordenadas normalizadas en coordenadas de pantalla.
        - Escala y traslada las coordenadas para ajustarlas al tamaño de la ventana de renderizado.
        """
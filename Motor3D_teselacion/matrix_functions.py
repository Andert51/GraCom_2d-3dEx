import math # Importa la biblioteca math para funciones matemáticas
import numpy as np # Importa la biblioteca NumPy para operaciones matemáticas y matrices

"""
Este módulo contiene funciones para generar matrices de transformación en un espacio 3D.
Incluye matrices para traslación, rotación en los ejes X, Y y Z, y escalado uniforme.
"""

def translate(pos):
    """
    Genera una matriz de traslación 4x4.

    :param pos: Una tupla o lista con las coordenadas de traslación (tx, ty, tz).
    :return: Matriz de traslación 4x4.
    """
    tx, ty, tz = pos
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [tx, ty, tz, 1]
    ])


def rotate_x(angle):
    """
    Genera una matriz de rotación 4x4 alrededor del eje X.

    :param angle: Ángulo de rotación en radianes.
    :return: Matriz de rotación 4x4 para el eje X.
    """
    return np.array([
        [1, 0, 0, 0],
        [0, math.cos(angle), math.sin(angle), 0],
        [0, -math.sin(angle), math.cos(angle), 0],
        [0, 0, 0, 1]
    ])


def rotate_y(angle):
    """
    Genera una matriz de rotación 4x4 alrededor del eje Y.

    :param angle: Ángulo de rotación en radianes.
    :return: Matriz de rotación 4x4 para el eje Y.
    """
    return np.array([
        [math.cos(angle), 0, -math.sin(angle), 0],
        [0, 1, 0, 0],
        [math.sin(angle), 0, math.cos(angle), 0],
        [0, 0, 0, 1]
    ])


def rotate_z(angle):
    """
    Genera una matriz de rotación 4x4 alrededor del eje Z.

    :param angle: Ángulo de rotación en radianes.
    :return: Matriz de rotación 4x4 para el eje Z.
    """
    return np.array([
        [math.cos(angle), math.sin(angle), 0, 0],
        [-math.sin(angle), math.cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


def scale(factor):
    """
    Genera una matriz de escalado uniforme 4x4.

    :param factor: Factor de escalado (mismo para todos los ejes).
    :return: Matriz de escalado 4x4.
    """
    return np.array([
        [factor, 0, 0, 0],
        [0, factor, 0, 0],
        [0, 0, factor, 0],
        [0, 0, 0, 1]
    ])
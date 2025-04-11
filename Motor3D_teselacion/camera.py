import pygame as pg # Importa la biblioteca Pygame para la gestión de gráficos y eventos
import numpy as np # Importa la biblioteca NumPy para operaciones matemáticas y matrices
import math # Importa la biblioteca NumPy para operaciones matemáticas y matrices
from matrix_functions import * # Importa funciones de transformación de matrices

class Camera:
    """
    Clase Camera que representa una cámara en un entorno 3D.
    Permite controlar la posición, orientación y matriz de transformación de la cámara.
    """

    def __init__(self, render, position):
        """
        Inicializa la cámara con los parámetros básicos.

        :param render: Objeto de renderizado que contiene información como altura y ancho de la pantalla.
        :param position: Posición inicial de la cámara en el espacio 3D.
        """
        self.render = render
        self.position = np.array([*position, 1.0])  # Posición de la cámara en coordenadas homogéneas
        self.forward = np.array([0, 0, 1, 1])  # Vector de dirección hacia adelante
        self.up = np.array([0, 1, 0, 1])  # Vector hacia arriba
        self.right = np.array([1, 0, 0, 1])  # Vector hacia la derecha

        # Configuración de los campos de visión (FOV) y planos de recorte
        self.h_fov = math.pi / 3  # Campo de visión horizontal
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)  # Campo de visión vertical
        self.near_plane = 0.1  # Plano cercano
        self.far_plane = 100  # Plano lejano

        # Velocidades de movimiento y rotación
        self.moving_speed = 0.3
        self.rotation_speed = 0.015

        # Ángulos de rotación de la cámara
        self.anglePitch = 0  # Rotación en el eje X
        self.angleYaw = 0  # Rotación en el eje Y
        self.angleRoll = 0  # Rotación en el eje Z

    def control(self):
        """
        Controla el movimiento y la rotación de la cámara en función de las teclas presionadas.
        """
        key = pg.key.get_pressed()

        # Movimiento de la cámara
        if key[pg.K_a]:  # Mover a la izquierda
            self.position -= self.right * self.moving_speed
        if key[pg.K_d]:  # Mover a la derecha
            self.position += self.right * self.moving_speed
        if key[pg.K_w]:  # Mover hacia adelante
            self.position += self.forward * self.moving_speed
        if key[pg.K_s]:  # Mover hacia atrás
            self.position -= self.forward * self.moving_speed
        if key[pg.K_q]:  # Mover hacia arriba
            self.position += self.up * self.moving_speed
        if key[pg.K_e]:  # Mover hacia abajo
            self.position -= self.up * self.moving_speed

        # Rotación de la cámara
        if key[pg.K_LEFT]:  # Rotar hacia la izquierda (Yaw)
            self.camera_yaw(-self.rotation_speed)
        if key[pg.K_RIGHT]:  # Rotar hacia la derecha (Yaw)
            self.camera_yaw(self.rotation_speed)
        if key[pg.K_UP]:  # Rotar hacia arriba (Pitch)
            self.camera_pitch(-self.rotation_speed)
        if key[pg.K_DOWN]:  # Rotar hacia abajo (Pitch)
            self.camera_pitch(self.rotation_speed)

    def camera_yaw(self, angle):
        """
        Aplica una rotación en el eje Y (Yaw) a la cámara.

        :param angle: Ángulo de rotación en radianes.
        """
        self.angleYaw += angle

    def camera_pitch(self, angle):
        """
        Aplica una rotación en el eje X (Pitch) a la cámara.

        :param angle: Ángulo de rotación en radianes.
        """
        self.anglePitch += angle

    def axiiIdentity(self):
        """
        Restaura los vectores de dirección de la cámara a sus valores iniciales.
        """
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])

    def camera_update_axii(self):
        """
        Actualiza los vectores de dirección de la cámara en función de los ángulos de rotación.
        """
        # Matriz de rotación combinada (primero Pitch, luego Yaw)
        rotate = rotate_x(self.anglePitch) @ rotate_y(self.angleYaw)
        self.axiiIdentity()  # Restaurar vectores iniciales
        self.forward = self.forward @ rotate  # Actualizar vector forward
        self.right = self.right @ rotate  # Actualizar vector right
        self.up = self.up @ rotate  # Actualizar vector up

    def camera_matrix(self):
        """
        Calcula la matriz de transformación de la cámara combinando traslación y rotación.

        :return: Matriz 4x4 de transformación de la cámara.
        """
        self.camera_update_axii()
        return self.translate_matrix() @ self.rotate_matrix()

    def translate_matrix(self):
        """
        Calcula la matriz de traslación de la cámara.

        :return: Matriz 4x4 de traslación.
        """
        x, y, z, w = self.position
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])

    def rotate_matrix(self):
        """
        Calcula la matriz de rotación de la cámara basada en los vectores de dirección.

        :return: Matriz 4x4 de rotación.
        """
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])
from settings import *  # Importa configuraciones globales del proyecto
from frustum import Frustum  # Importa la clase Frustum para manejar el frustum de la cámara


class Camera:
    """
    Clase que representa la cámara en el mundo voxel.

    La cámara es responsable de definir la perspectiva del jugador en el mundo.
    Maneja la posición, orientación y movimiento de la cámara, así como la
    generación de las matrices de proyección y vista.

    Atributos:
        position (glm.vec3): Posición actual de la cámara en el mundo.
        yaw (float): Ángulo de rotación horizontal (en radianes).
        pitch (float): Ángulo de rotación vertical (en radianes).
        up (glm.vec3): Vector "arriba" de la cámara.
        right (glm.vec3): Vector "derecha" de la cámara.
        forward (glm.vec3): Vector "frontal" de la cámara.
        m_proj (glm.mat4): Matriz de proyección de la cámara.
        m_view (glm.mat4): Matriz de vista de la cámara.
        frustum (Frustum): Objeto que representa el frustum de la cámara.
    """

    def __init__(self, position, yaw, pitch):
        """
        Inicializa la cámara.

        Parámetros:
            position (tuple): Posición inicial de la cámara en el mundo.
            yaw (float): Ángulo inicial de rotación horizontal (en grados).
            pitch (float): Ángulo inicial de rotación vertical (en grados).
        """
        self.position = glm.vec3(position)  # Posición inicial de la cámara
        self.yaw = glm.radians(yaw)  # Convierte el ángulo horizontal a radianes
        self.pitch = glm.radians(pitch)  # Convierte el ángulo vertical a radianes

        # Vectores iniciales de orientación de la cámara
        self.up = glm.vec3(0, 1, 0)  # Vector "arriba"
        self.right = glm.vec3(1, 0, 0)  # Vector "derecha"
        self.forward = glm.vec3(0, 0, -1)  # Vector "frontal"

        # Matriz de proyección (define la perspectiva de la cámara)
        self.m_proj = glm.perspective(
            FOV_VERTICAL_RADIANES,  # Campo de visión vertical en radianes
            RELACION_ASPECTO,  # Relación de aspecto (ancho/alto)
            DISTANCIA_CERCANA,  # Distancia mínima visible
            DISTANCIA_LEJANA  # Distancia máxima visible
        )

        # Matriz de vista (se inicializa vacía, se actualiza más tarde)
        self.m_view = glm.mat4()

        # Frustum de la cámara (para determinar qué objetos están dentro del campo de visión)
        self.frustum = Frustum(self)

    def update(self):
        """
        Actualiza la cámara.

        Este método recalcula los vectores de orientación (`forward`, `right`, `up`)
        y la matriz de vista (`m_view`) en función de la posición y orientación actuales.
        """
        self.update_vectors()  # Actualiza los vectores de orientación
        self.update_view_matrix()  # Actualiza la matriz de vista

    def update_view_matrix(self):
        """
        Actualiza la matriz de vista de la cámara.

        La matriz de vista define la posición y orientación de la cámara en el mundo.
        """
        self.m_view = glm.lookAt(
            self.position,  # Posición de la cámara
            self.position + self.forward,  # Punto hacia donde mira la cámara
            self.up  # Vector "arriba" de la cámara
        )

    def update_vectors(self):
        """
        Actualiza los vectores de orientación de la cámara (`forward`, `right`, `up`).

        Los vectores se recalculan en función de los ángulos `yaw` y `pitch`.
        """
        # Calcula el vector "frontal" (hacia donde mira la cámara)
        self.forward.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.sin(self.yaw) * glm.cos(self.pitch)
        self.forward = glm.normalize(self.forward)  # Normaliza el vector

        # Calcula el vector "derecha" (perpendicular al vector "frontal" y al eje Y)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))

        # Calcula el vector "arriba" (perpendicular a los vectores "derecha" y "frontal")
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def rotate_pitch(self, delta_y):
        """
        Rota la cámara verticalmente (pitch).

        Parámetros:
            delta_y (float): Cambio en el ángulo vertical (en radianes).
        """
        self.pitch -= delta_y  # Ajusta el ángulo vertical
        self.pitch = glm.clamp(self.pitch, -MAX_PITCH, MAX_PITCH)  # Limita el ángulo vertical

    def rotate_yaw(self, delta_x):
        """
        Rota la cámara horizontalmente (yaw).

        Parámetros:
            delta_x (float): Cambio en el ángulo horizontal (en radianes).
        """
        self.yaw += delta_x  # Ajusta el ángulo horizontal

    def move_left(self, velocity):
        """
        Mueve la cámara hacia la izquierda.

        Parámetros:
            velocity (float): Velocidad del movimiento.
        """
        self.position -= self.right * velocity  # Ajusta la posición hacia la izquierda

    def move_right(self, velocity):
        """
        Mueve la cámara hacia la derecha.

        Parámetros:
            velocity (float): Velocidad del movimiento.
        """
        self.position += self.right * velocity  # Ajusta la posición hacia la derecha

    def move_up(self, velocity):
        """
        Mueve la cámara hacia arriba.

        Parámetros:
            velocity (float): Velocidad del movimiento.
        """
        self.position += self.up * velocity  # Ajusta la posición hacia arriba

    def move_down(self, velocity):
        """
        Mueve la cámara hacia abajo.

        Parámetros:
            velocity (float): Velocidad del movimiento.
        """
        self.position -= self.up * velocity  # Ajusta la posición hacia abajo

    def move_forward(self, velocity):
        """
        Mueve la cámara hacia adelante.

        Parámetros:
            velocity (float): Velocidad del movimiento.
        """
        self.position += self.forward * velocity  # Ajusta la posición hacia adelante

    def move_back(self, velocity):
        """
        Mueve la cámara hacia atrás.

        Parámetros:
            velocity (float): Velocidad del movimiento.
        """
        self.position -= self.forward * velocity  # Ajusta la posición hacia atrás
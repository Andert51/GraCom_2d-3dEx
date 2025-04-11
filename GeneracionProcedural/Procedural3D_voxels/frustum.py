from settings import *  # Importa configuraciones globales del proyecto


class Frustum:
    """
    Clase que representa el frustum de la cámara.

    El frustum es una pirámide truncada que define el volumen visible de la cámara.
    Esta clase se utiliza para determinar si un objeto (como un chunk) está dentro
    del campo de visión de la cámara.

    Atributos:
        cam (Camera): Referencia a la cámara asociada al frustum.
        factor_y (float): Factor de ajuste para los planos superior e inferior del frustum.
        tan_y (float): Tangente del ángulo vertical del campo de visión.
        factor_x (float): Factor de ajuste para los planos izquierdo y derecho del frustum.
        tan_x (float): Tangente del ángulo horizontal del campo de visión.
    """

    def __init__(self, camera):
        """
        Inicializa el frustum de la cámara.

        Parámetros:
            camera (Camera): Referencia a la cámara asociada al frustum.
        """
        self.cam: Camera = camera  # Referencia a la cámara

        # Calcula el factor y la tangente para los planos superior e inferior
        self.factor_y = 1.0 / math.cos(half_y := FOV_VERTICAL_RADIANES * 0.5)
        self.tan_y = math.tan(half_y)

        # Calcula el factor y la tangente para los planos izquierdo y derecho
        self.factor_x = 1.0 / math.cos(half_x := FOV_HORIZONTAL * 0.5)
        self.tan_x = math.tan(half_x)

    def is_on_frustum(self, chunk):
        """
        Determina si un chunk está dentro del frustum de la cámara.

        Parámetros:
            chunk (Chunk): Chunk a verificar.

        Retorna:
            bool: True si el chunk está dentro del frustum, False en caso contrario.
        """
        # Calcula el vector desde la posición de la cámara al centro del chunk
        sphere_vec = chunk.center - self.cam.position

        # Verifica si el chunk está fuera de los planos NEAR y FAR
        sz = glm.dot(sphere_vec, self.cam.forward)  # Proyección del vector en el eje "frontal" de la cámara
        if not (DISTANCIA_CERCANA - RADIO_ESFERA_CHUNK <= sz <= DISTANCIA_LEJANA + RADIO_ESFERA_CHUNK):
            return False  # El chunk está fuera del rango visible en profundidad

        # Verifica si el chunk está fuera de los planos TOP y BOTTOM
        sy = glm.dot(sphere_vec, self.cam.up)  # Proyección del vector en el eje "arriba" de la cámara
        dist = self.factor_y * RADIO_ESFERA_CHUNK + sz * self.tan_y  # Distancia ajustada para los planos superior e inferior
        if not (-dist <= sy <= dist):
            return False  # El chunk está fuera del rango visible en altura

        # Verifica si el chunk está fuera de los planos LEFT y RIGHT
        sx = glm.dot(sphere_vec, self.cam.right)  # Proyección del vector en el eje "derecha" de la cámara
        dist = self.factor_x * RADIO_ESFERA_CHUNK + sz * self.tan_x  # Distancia ajustada para los planos izquierdo y derecho
        if not (-dist <= sx <= dist):
            return False  # El chunk está fuera del rango visible en anchura

        # Si pasa todas las verificaciones, el chunk está dentro del frustum
        return True
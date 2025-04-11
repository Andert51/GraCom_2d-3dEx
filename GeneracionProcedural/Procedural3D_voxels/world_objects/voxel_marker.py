from settings import *  # Importa configuraciones globales del proyecto
from meshes.cube_mesh import CubeMesh  # Importa la clase CubeMesh para manejar la malla del marcador de voxel


class VoxelMarker:
    """
    Clase que representa un marcador de voxel en el mundo voxel.

    El marcador de voxel se utiliza para indicar la posición de un voxel
    que está siendo seleccionado o interactuado por el jugador. Este marcador
    puede ser visible cuando el jugador está en modo de interacción.

    Atributos:
        app (object): Referencia a la aplicación principal.
        handler (object): Referencia al manejador de voxeles (voxel_handler).
        position (glm.vec3): Posición actual del marcador en el mundo.
        m_model (glm.mat4): Matriz de modelo para transformar el marcador en el espacio del mundo.
        mesh (CubeMesh): Malla asociada al marcador para renderizarlo.
    """

    def __init__(self, voxel_handler):
        """
        Inicializa el marcador de voxel.

        Parámetros:
            voxel_handler (object): Referencia al manejador de voxeles.
        """
        self.app = voxel_handler.app  # Referencia a la aplicación principal
        self.handler = voxel_handler  # Referencia al manejador de voxeles
        self.position = glm.vec3(0)  # Posición inicial del marcador (en el origen)
        self.m_model = self.get_model_matrix()  # Matriz de modelo inicial
        self.mesh = CubeMesh(self.app)  # Crea la malla del marcador utilizando CubeMesh

    def update(self):
        """
        Actualiza la posición del marcador de voxel.

        Si el manejador de voxeles tiene un voxel seleccionado (`voxel_id`),
        este método actualiza la posición del marcador dependiendo del modo
        de interacción del jugador:
        - Si está en modo de interacción (`interaction_mode`), el marcador
          se posiciona en el voxel adyacente al seleccionado.
        - Si no está en modo de interacción, el marcador se posiciona
          directamente en el voxel seleccionado.
        """
        if self.handler.voxel_id:  # Verifica si hay un voxel seleccionado
            if self.handler.interaction_mode:  # Modo de interacción activado
                self.position = self.handler.voxel_world_pos + self.handler.voxel_normal
            else:  # Modo de interacción desactivado
                self.position = self.handler.voxel_world_pos

    def set_uniform(self):
        """
        Configura las variables uniformes en el programa de sombreado.

        Este método actualiza:
        - `mode_id`: Indica el modo de interacción (activo o inactivo).
        - `m_model`: Matriz de modelo para transformar el marcador en el espacio del mundo.
        """
        self.mesh.program['mode_id'] = self.handler.interaction_mode  # Actualiza el modo de interacción
        self.mesh.program['m_model'].write(self.get_model_matrix())  # Escribe la matriz de modelo en el shader

    def get_model_matrix(self):
        """
        Calcula la matriz de modelo para transformar el marcador en el espacio del mundo.

        La matriz de modelo se basa en la posición actual del marcador.

        Retorna:
            glm.mat4: Matriz de modelo.
        """
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position))  # Traduce la posición del marcador
        return m_model

    def render(self):
        """
        Renderiza el marcador de voxel.

        Si hay un voxel seleccionado (`voxel_id`), este método configura
        las variables uniformes y renderiza la malla del marcador.
        """
        if self.handler.voxel_id:  # Verifica si hay un voxel seleccionado
            self.set_uniform()  # Configura las variables uniformes en el shader
            self.mesh.render()  # Renderiza la malla del marcador
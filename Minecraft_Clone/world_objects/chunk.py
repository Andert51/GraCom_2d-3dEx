from settings import *  # Importa configuraciones globales del proyecto
from meshes.chunk_mesh import ChunkMesh  # Importa la clase ChunkMesh para manejar la malla del chunk
import random  # Importa la librería random para generar valores aleatorios
from terrain_gen import *  # Importa funciones relacionadas con la generación de terreno


class Chunk:
    """
    Clase que representa un chunk en el mundo voxel.

    Un chunk es una sección del mundo que contiene una colección de voxeles.
    Esta clase maneja la generación de voxeles, la creación de la malla del chunk
    y su renderizado.

    Atributos:
        app (object): Referencia a la aplicación principal.
        world (object): Referencia al mundo al que pertenece este chunk.
        position (tuple): Posición del chunk en coordenadas del mundo.
        m_model (glm.mat4): Matriz de modelo para transformar el chunk en el espacio del mundo.
        voxels (np.array): Array que contiene los datos de los voxeles del chunk.
        mesh (ChunkMesh): Malla asociada al chunk para renderizarlo.
        is_empty (bool): Indica si el chunk está vacío (sin voxeles).
        center (glm.vec3): Centro del chunk en coordenadas del mundo.
        is_on_frustum (callable): Función para verificar si el chunk está dentro del frustum de la cámara.
    """

    def __init__(self, world, position):
        """
        Inicializa un nuevo chunk.

        Parámetros:
            world (object): Referencia al mundo al que pertenece este chunk.
            position (tuple): Posición del chunk en coordenadas del mundo.
        """
        self.app = world.app  # Referencia a la aplicación principal
        self.world = world  # Referencia al mundo
        self.position = position  # Posición del chunk en el mundo
        self.m_model = self.get_model_matrix()  # Matriz de modelo para transformar el chunk
        self.voxels: np.array = None  # Array de voxeles del chunk (se inicializa más tarde)
        self.mesh: ChunkMesh = None  # Malla del chunk (se inicializa más tarde)
        self.is_empty = True  # Indica si el chunk está vacío

        # Calcula el centro del chunk en coordenadas del mundo
        self.center = (glm.vec3(self.position) + 0.5) * TAMANO_CHUNK

        # Función para verificar si el chunk está dentro del frustum de la cámara
        self.is_on_frustum = self.app.player.frustum.is_on_frustum

    def get_model_matrix(self):
        """
        Calcula la matriz de modelo para transformar el chunk en el espacio del mundo.

        Retorna:
            glm.mat4: Matriz de modelo.
        """
        # Traduce la posición del chunk al espacio del mundo
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position) * TAMANO_CHUNK)
        return m_model

    def set_uniform(self):
        """
        Configura la matriz de modelo en el programa de sombreado asociado al chunk.
        """
        self.mesh.program['m_model'].write(self.m_model)

    def build_mesh(self):
        """
        Construye la malla del chunk utilizando la clase ChunkMesh.
        """
        self.mesh = ChunkMesh(self)

    def render(self):
        """
        Renderiza el chunk si no está vacío y está dentro del frustum de la cámara.
        """
        if not self.is_empty and self.is_on_frustum(self):
            self.set_uniform()  # Configura la matriz de modelo en el shader
            self.mesh.render()  # Renderiza la malla del chunk

    def build_voxels(self):
        """
        Genera los datos de los voxeles para el chunk.

        Crea un array vacío de voxeles y utiliza la función `generate_terrain`
        para rellenarlo con datos de terreno.

        Retorna:
            np.array: Array de voxeles del chunk.
        """
        # Inicializa un array vacío para los voxeles del chunk
        voxels = np.zeros(VOLUMEN_CHUNK, dtype='uint8')

        # Calcula las coordenadas globales del chunk
        cx, cy, cz = glm.ivec3(self.position) * TAMANO_CHUNK

        # Genera el terreno para el chunk
        self.generate_terrain(voxels, cx, cy, cz)

        # Verifica si el chunk contiene algún voxel no vacío
        if np.any(voxels):
            self.is_empty = False  # Marca el chunk como no vacío
        return voxels

    @staticmethod
    @njit
    def generate_terrain(voxels, cx, cy, cz):
        """
        Genera el terreno del chunk utilizando datos de altura del mundo.

        Parámetros:
            voxels (np.array): Array donde se almacenan los datos de los voxeles.
            cx (int): Coordenada X global del chunk.
            cy (int): Coordenada Y global del chunk.
            cz (int): Coordenada Z global del chunk.
        """
        # Itera sobre cada posición en el chunk
        for x in range(TAMANO_CHUNK):
            wx = x + cx  # Coordenada X global del voxel
            for z in range(TAMANO_CHUNK):
                wz = z + cz  # Coordenada Z global del voxel

                # Obtiene la altura del terreno en las coordenadas globales (wx, wz)
                world_height = get_height(wx, wz)

                # Calcula la altura local dentro del chunk
                local_height = min(world_height - cy, TAMANO_CHUNK)

                # Rellena los voxeles hasta la altura local
                for y in range(local_height):
                    wy = y + cy  # Coordenada Y global del voxel

                    # Establece el ID del voxel en la posición actual
                    set_voxel_id(voxels, x, y, z, wx, wy, wz, world_height)
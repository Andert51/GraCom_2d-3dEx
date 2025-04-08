from settings import *  # Importa configuraciones globales del proyecto
from world_objects.chunk import Chunk  # Clase que representa un chunk del mundo
from voxel_handler import VoxelHandler  # Clase para manejar la interacción con los voxeles


class World:
    """
    Clase que representa el mundo voxel.

    El mundo está compuesto por múltiples chunks, cada uno de los cuales contiene
    una porción del terreno. Esta clase se encarga de construir los chunks, generar
    sus mallas, renderizarlos y manejar la interacción con los voxeles.

    Atributos:
        app (object): Referencia a la aplicación principal.
        chunks (list): Lista de chunks que componen el mundo.
        voxels (np.array): Array que contiene los datos de los voxeles de todos los chunks.
        voxel_handler (VoxelHandler): Objeto que maneja la interacción con los voxeles.
    """

    def __init__(self, app):
        """
        Inicializa el mundo voxel.

        Parámetros:
            app (object): Referencia a la aplicación principal.
        """
        self.app = app  # Referencia a la aplicación principal

        # Inicializa la lista de chunks con valores vacíos
        self.chunks = [None for _ in range(VOLUMEN_MUNDO)]

        # Crea un array para almacenar los datos de los voxeles de todos los chunks
        self.voxels = np.empty([VOLUMEN_MUNDO, VOLUMEN_CHUNK], dtype='uint8')

        # Construye los chunks y sus mallas
        self.build_chunks()
        self.build_chunk_mesh()

        # Inicializa el manejador de voxeles
        self.voxel_handler = VoxelHandler(self)

    def update(self):
        """
        Actualiza el estado del mundo.

        Este método actualiza el manejador de voxeles, que incluye la detección
        de interacción con los voxeles.
        """
        self.voxel_handler.update()

    def build_chunks(self):
        """
        Construye todos los chunks del mundo.

        Este método crea cada chunk en su posición correspondiente, genera los
        datos de los voxeles para cada chunk y los almacena en un array global.
        """
        for x in range(ANCHURA_MUNDO):  # Itera sobre la anchura del mundo
            for y in range(ALTURA_MUNDO):  # Itera sobre la altura del mundo
                for z in range(PROFUNDIDAD_MUNDO):  # Itera sobre la profundidad del mundo
                    # Crea un nuevo chunk en la posición (x, y, z)
                    chunk = Chunk(self, position=(x, y, z))

                    # Calcula el índice del chunk en el array global
                    chunk_index = x + ANCHURA_MUNDO * z + AREA_MUNDO * y
                    self.chunks[chunk_index] = chunk  # Almacena el chunk en la lista

                    # Genera los datos de los voxeles para el chunk y los almacena
                    self.voxels[chunk_index] = chunk.build_voxels()

                    # Asigna un puntero al array de voxeles del chunk
                    chunk.voxels = self.voxels[chunk_index]

    def build_chunk_mesh(self):
        """
        Genera las mallas para todos los chunks del mundo.

        Este método llama al método `build_mesh` de cada chunk para construir
        su malla de renderizado.
        """
        for chunk in self.chunks:
            chunk.build_mesh()

    def render(self):
        """
        Renderiza todos los chunks del mundo.

        Este método llama al método `render` de cada chunk para dibujarlo en la pantalla.
        """
        for chunk in self.chunks:
            chunk.render()
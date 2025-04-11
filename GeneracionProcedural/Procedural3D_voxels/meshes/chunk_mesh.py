from meshes.base_mesh import BaseMesh  # Importa la clase base para las mallas
from meshes.chunk_mesh_builder import build_chunk_mesh  # Importa la función para construir la malla de un chunk


class ChunkMesh(BaseMesh):
    """
    Clase que representa la malla de un chunk en el mundo voxel.
    Hereda de la clase BaseMesh y utiliza un programa de sombreado (shader) para renderizar la malla.

    Atributos:
        app (object): Referencia a la aplicación principal.
        chunk (object): Referencia al chunk asociado a esta malla.
        ctx (object): Contexto de renderizado (por ejemplo, OpenGL).
        program (object): Programa de sombreado utilizado para renderizar la malla.
        vbo_format (str): Formato del Vertex Buffer Object (VBO), en este caso '1u4'.
        format_size (int): Tamaño del formato del VBO, calculado a partir de `vbo_format`.
        attrs (tuple): Atributos de los vértices que se usarán en el VAO (Vertex Array Object).
        vao (object): Vertex Array Object que contiene la configuración de la malla.
    """

    def __init__(self, chunk):
        """
        Inicializa la malla del chunk.

        Parámetros:
            chunk (object): Chunk al que pertenece esta malla.
        """
        super().__init__()  # Llama al constructor de la clase base
        self.app = chunk.app  # Referencia a la aplicación principal
        self.chunk = chunk  # Referencia al chunk asociado
        self.ctx = self.app.ctx  # Contexto de renderizado (por ejemplo, OpenGL)
        self.program = self.app.shader_program.chunk  # Programa de sombreado para renderizar chunks

        # Configuración del formato del VBO (Vertex Buffer Object)
        self.vbo_format = '1u4'  # Formato del VBO: 1 entero sin signo de 4 bytes
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())  # Calcula el tamaño del formato
        self.attrs = ('packed_data',)  # Atributos de los vértices que se usarán en el VAO
        self.vao = self.get_vao()  # Crea el VAO inicial

    def rebuild(self):
        """
        Reconstruye el VAO (Vertex Array Object) de la malla.
        Esto es útil cuando se necesita actualizar la configuración de la malla.
        """
        self.vao = self.get_vao()  # Vuelve a generar el VAO

    def get_vertex_data(self):
        """
        Genera los datos de los vértices para la malla del chunk.

        Utiliza la función `build_chunk_mesh` para construir la malla del chunk
        basándose en los datos de los voxeles del chunk y del mundo.

        Retorna:
            array: Datos de los vértices de la malla del chunk.
        """
        # Llama a la función `build_chunk_mesh` para construir la malla del chunk
        mesh = build_chunk_mesh(
            chunk_voxels=self.chunk.voxels,  # Array de voxeles del chunk
            format_size=self.format_size,  # Tamaño del formato del VBO
            chunk_pos=self.chunk.position,  # Posición del chunk en el mundo
            world_voxels=self.chunk.world.voxels  # Array de voxeles del mundo
        )
        return mesh  # Retorna los datos de los vértices generados
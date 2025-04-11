from settings import *  # Importa configuraciones globales del proyecto
from meshes.base_mesh import BaseMesh  # Importa la clase base para las mallas


class CubeMesh(BaseMesh):
    """
    Clase que representa la malla de un cubo en el mundo voxel.
    Hereda de la clase BaseMesh y utiliza un programa de sombreado (shader) para renderizar el cubo.

    Atributos:
        app (object): Referencia a la aplicación principal.
        ctx (object): Contexto de renderizado (por ejemplo, OpenGL).
        program (object): Programa de sombreado utilizado para renderizar el cubo.
        vbo_format (str): Formato del Vertex Buffer Object (VBO), en este caso '2f2 3f2'.
        attrs (tuple): Atributos de los vértices que se usarán en el VAO (Vertex Array Object).
        vao (object): Vertex Array Object que contiene la configuración de la malla.
    """

    def __init__(self, app):
        """
        Inicializa la malla del cubo.

        Parámetros:
            app (object): Referencia a la aplicación principal.
        """
        super().__init__()  # Llama al constructor de la clase base
        self.app = app  # Referencia a la aplicación principal

        # Configuración del contexto de renderizado y el programa de sombreado
        self.ctx = self.app.ctx  # Contexto de renderizado (por ejemplo, OpenGL)
        self.program = self.app.shader_program.voxel_marker  # Programa de sombreado para renderizar el cubo

        # Configuración del formato del VBO (Vertex Buffer Object)
        self.vbo_format = '2f2 3f2'  # Formato del VBO: 2 floats para coordenadas de textura, 3 floats para posición
        self.attrs = ('in_tex_coord_0', 'in_position',)  # Atributos de los vértices que se usarán en el VAO
        self.vao = self.get_vao()  # Crea el VAO inicial

    @staticmethod
    def get_data(vertices, indices):
        """
        Genera un array de datos de vértices a partir de una lista de vértices y sus índices.

        Parámetros:
            vertices (list): Lista de vértices.
            indices (list): Lista de índices que definen los triángulos.

        Retorna:
            np.array: Array de datos de vértices en el formato especificado.
        """
        # Recorre los índices y extrae los vértices correspondientes para formar triángulos
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='float16')  # Convierte los datos a un array de tipo float16

    def get_vertex_data(self):
        """
        Genera los datos de los vértices para la malla del cubo.

        Este método define los vértices y los índices para las posiciones y las coordenadas de textura,
        y combina ambos en un único array de datos.

        Retorna:
            np.array: Datos de los vértices del cubo, incluyendo posiciones y coordenadas de textura.
        """
        # Define los vértices del cubo (coordenadas 3D)
        vertices = [
            (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1),  # Cara frontal
            (0, 1, 0), (0, 0, 0), (1, 0, 0), (1, 1, 0)   # Cara trasera
        ]

        # Define los índices que forman los triángulos del cubo
        indices = [ # Mapa de índices para los triángulos
            (0, 2, 3), (0, 1, 2),  # Cara frontal
            (1, 7, 2), (1, 6, 7),  # Cara derecha
            (6, 5, 4), (4, 7, 6),  # Cara trasera
            (3, 4, 5), (3, 5, 0),  # Cara izquierda
            (3, 7, 4), (3, 2, 7),  # Cara superior
            (0, 6, 1), (0, 5, 6)   # Cara inferior
        ]

        # Genera los datos de los vértices a partir de las posiciones y los índices
        vertex_data = self.get_data(vertices, indices)

        # Define las coordenadas de textura para cada vértice
        tex_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]  # Coordenadas UV
        tex_coord_indices = [ # Mapa de índices para las coordenadas de textura
            (0, 2, 3), (0, 1, 2),  # Cara frontal
            (0, 2, 3), (0, 1, 2),  # Cara derecha
            (0, 1, 2), (2, 3, 0),  # Cara trasera
            (2, 3, 0), (2, 0, 1),  # Cara izquierda
            (0, 2, 3), (0, 1, 2),  # Cara superior
            (3, 1, 2), (3, 0, 1)   # Cara inferior
        ]

        # Genera los datos de las coordenadas de textura a partir de los vértices y los índices
        tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)

        # Combina los datos de las coordenadas de textura y las posiciones en un único array
        vertex_data = np.hstack([tex_coord_data, vertex_data])

        # Retorna los datos combinados de los vértices
        return vertex_data
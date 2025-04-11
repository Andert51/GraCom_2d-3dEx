from settings import *  # Importa configuraciones globales del proyecto
from meshes.base_mesh import BaseMesh  # Importa la clase base para las mallas


class QuadMesh(BaseMesh):
    """
    Clase que representa la malla de un quad (un plano 2D) en el mundo voxel.
    Hereda de la clase BaseMesh y utiliza un programa de sombreado (shader) para renderizar el quad.

    Atributos:
        app (object): Referencia a la aplicación principal.
        ctx (object): Contexto de renderizado (por ejemplo, OpenGL).
        program (object): Programa de sombreado utilizado para renderizar el quad.
        vbo_format (str): Formato del Vertex Buffer Object (VBO), en este caso '2u1 3u1'.
        attrs (tuple): Atributos de los vértices que se usarán en el VAO (Vertex Array Object).
        vao (object): Vertex Array Object que contiene la configuración de la malla.
    """

    def __init__(self, app):
        """
        Inicializa la malla del quad.

        Parámetros:
            app (object): Referencia a la aplicación principal.
        """
        super().__init__()  # Llama al constructor de la clase base
        self.app = app  # Referencia a la aplicación principal

        # Configuración del contexto de renderizado y el programa de sombreado
        self.ctx = self.app.ctx  # Contexto de renderizado (por ejemplo, OpenGL)
        self.program = self.app.shader_program.water  # Programa de sombreado para renderizar agua

        # Configuración del formato del VBO (Vertex Buffer Object)
        self.vbo_format = '2u1 3u1'  # Formato del VBO: 2 enteros sin signo de 1 byte para coordenadas de textura,
                                     # y 3 enteros sin signo de 1 byte para posiciones.
        self.attrs = ('in_tex_coord', 'in_position')  # Atributos de los vértices que se usarán en el VAO
        self.vao = self.get_vao()  # Crea el VAO inicial

    def get_vertex_data(self):
        """
        Genera los datos de los vértices para la malla del quad.

        Este método define los vértices y las coordenadas de textura para el quad,
        y combina ambos en un único array de datos.

        Retorna:
            np.array: Datos de los vértices del quad, incluyendo posiciones y coordenadas de textura.
        """
        # Define las posiciones de los vértices del quad (coordenadas 3D)
        # Cada vértice está definido por su posición en el espacio 3D (x, y, z)
        vertices = np.array([
            (0, 0, 0), (1, 0, 1), (1, 0, 0),  # Triángulo 1
            (0, 0, 0), (0, 0, 1), (1, 0, 1)   # Triángulo 2
        ], dtype='uint8')

        # Define las coordenadas de textura para cada vértice
        # Estas coordenadas (u, v) se utilizan para mapear texturas al quad
        tex_coords = np.array([
            (0, 0), (1, 1), (1, 0),  # Coordenadas de textura para el Triángulo 1
            (0, 0), (0, 1), (1, 1)   # Coordenadas de textura para el Triángulo 2
        ], dtype='uint8')

        # Combina las coordenadas de textura y las posiciones de los vértices en un único array
        vertex_data = np.hstack([tex_coords, vertices])

        # Retorna los datos combinados de los vértices
        return vertex_data
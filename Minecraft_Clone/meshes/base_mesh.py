import numpy as np

# Clase BaseMesh: Representa una malla base que se utiliza para renderizar datos de vértices en OpenGL.
class BaseMesh:
    def __init__(self):
        # Contexto de OpenGL
        self.ctx = None
        # Programa de shaders que se utilizará para renderizar
        self.program = None
        # Formato del buffer de vértices (por ejemplo, "3f 3f" para posición y color)
        self.vbo_format = None
        # Nombres de los atributos según el formato del buffer (por ejemplo, "in_position", "in_color")
        # Nota: Es importante manejar el caso en que self.attrs sea None
        self.attrs: tuple[str, ...] = None
        # Objeto de arreglo de vértices (VAO)
        self.vao = None

    # Método para obtener los datos de los vértices
    def get_vertex_data(self) -> np.array:
        # Este método debe ser implementado por las subclases para proporcionar los datos de los vértices.
        pass

    # Método para crear el VAO (Vertex Array Object)
    def get_vao(self):
        # Obtener los datos de los vértices que se usarán para crear el VAO
        vertex_data = self.get_vertex_data()
        # Crear un Vertex Buffer Object (VBO) y llenarlo con los datos de los vértices
        vbo = self.ctx.buffer(vertex_data)
        # Crear un VAO que encapsula un conjunto de VBOs y configuraciones de vértices
        vao = self.ctx.vertex_array(
            self.program, [(vbo, self.vbo_format, *self.attrs)],
            skip_errors=True  # Ignorar errores si los atributos no coinciden
        )
        return vao  # Esto se puede usar para renderizar los datos de los vértices de manera eficiente

    # Método para renderizar la malla
    def render(self):
        # Renderiza el VAO asociado a esta malla
        self.vao.render()
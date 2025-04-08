from settings import *  # Importa configuraciones globales del proyecto
from meshes.base_mesh import BaseMesh  # Importa la clase base para las mallas
from noise import *  # Importa funciones para generar ruido (por ejemplo, Perlin noise)
from noise import noise2 # Importa la función de ruido 2D


class CloudMesh(BaseMesh):
    """
    Clase que representa la malla de las nubes en el mundo voxel.
    Hereda de la clase BaseMesh y utiliza un programa de sombreado (shader) para renderizar las nubes.

    Atributos:
        app (object): Referencia a la aplicación principal.
        ctx (object): Contexto de renderizado (por ejemplo, OpenGL).
        program (object): Programa de sombreado utilizado para renderizar las nubes.
        vbo_format (str): Formato del Vertex Buffer Object (VBO), en este caso '3u2'.
        attrs (tuple): Atributos de los vértices que se usarán en el VAO (Vertex Array Object).
        vao (object): Vertex Array Object que contiene la configuración de la malla.
    """

    def __init__(self, app):
        """
        Inicializa la malla de las nubes.

        Parámetros:
            app (object): Referencia a la aplicación principal.
        """
        super().__init__()  # Llama al constructor de la clase base
        self.app = app  # Referencia a la aplicación principal

        # Configuración del contexto de renderizado y el programa de sombreado
        self.ctx = self.app.ctx  # Contexto de renderizado (por ejemplo, OpenGL)
        self.program = self.app.shader_program.clouds  # Programa de sombreado para renderizar nubes

        # Configuración del formato del VBO (Vertex Buffer Object)
        self.vbo_format = '3u2'  # Formato del VBO: 3 enteros sin signo de 2 bytes
        self.attrs = ('in_position',)  # Atributos de los vértices que se usarán en el VAO
        self.vao = self.get_vao()  # Crea el VAO inicial

    def get_vertex_data(self):
        """
        Genera los datos de los vértices para la malla de las nubes.

        Este método crea un array de datos de nubes, genera las nubes utilizando ruido
        y construye la malla a partir de esos datos.

        Retorna:
            array: Datos de los vértices de la malla de las nubes.
        """
        # Inicializa un array para almacenar los datos de las nubes
        cloud_data = np.zeros(AREA_MUNDO * TAMANO_CHUNK ** 2, dtype='uint8')

        # Genera las nubes utilizando ruido
        self.gen_clouds(cloud_data)

        # Construye la malla a partir de los datos generados
        return self.build_mesh(cloud_data)

    @staticmethod
    @njit
    def gen_clouds(cloud_data):
        """
        Genera un mapa de nubes utilizando ruido.

        Parámetros:
            cloud_data (array): Array donde se almacenan los datos de las nubes.
        """
        for x in range(ANCHURA_MUNDO * TAMANO_CHUNK):
            for z in range(PROFUNDIDAD_MUNDO * TAMANO_CHUNK):
                # Genera ruido para determinar si hay una nube en la posición actual
                if noise2(0.13 * x, 0.13 * z) < 0.2:
                    continue  # Si el valor del ruido es menor a 0.2, no hay nube
                cloud_data[x + ANCHURA_MUNDO * TAMANO_CHUNK * z] = 1  # Marca la posición como nube

    @staticmethod
    @njit
    def build_mesh(cloud_data):
        """
        Construye la malla de las nubes a partir de los datos generados.

        Parámetros:
            cloud_data (array): Array que contiene los datos de las nubes.

        Retorna:
            array: Datos de los vértices de la malla de las nubes.
        """
        # Inicializa un array para almacenar los datos de la malla
        mesh = np.empty(AREA_MUNDO * AREA_CHUNK * 6 * 3, dtype='uint16')
        index = 0  # Índice actual en el array de la malla

        # Dimensiones del mundo en términos de ancho y profundidad
        width = ANCHURA_MUNDO * TAMANO_CHUNK # Ancho del mundo
        depth = PROFUNDIDAD_MUNDO * TAMANO_CHUNK # Profundidad del mundo

        # Altura fija para las nubes
        y = ALTURA_NUBES

        # Conjunto para rastrear las posiciones ya visitadas
        visited = set()

        # Itera sobre cada posición en el plano XZ
        for z in range(depth):
            for x in range(width):
                idx = x + width * z  # Calcula el índice en el array de datos de nubes

                # Si no hay nube en la posición actual o ya fue visitada, continúa
                if not cloud_data[idx] or idx in visited:
                    continue

                # Encuentra el número de quads continuos a lo largo del eje X
                x_count = 1 # Número de quads continuos en X
                idx = (x + x_count) + width * z # Calcula el índice en el array de datos de nubes
                while x + x_count < width and cloud_data[idx] and idx not in visited: # Verifica si hay nube
                    # Si hay nube, incrementa el contador y calcula el nuevo índice 
                    x_count += 1
                    idx = (x + x_count) + width * z

                # Encuentra el número de quads continuos a lo largo del eje Z para cada X
                z_count_list = []
                for ix in range(x_count):
                    z_count = 1
                    idx = (x + ix) + width * (z + z_count)
                    while (z + z_count) < depth and cloud_data[idx] and idx not in visited:
                        z_count += 1
                        idx = (x + ix) + width * (z + z_count)
                    z_count_list.append(z_count)

                # Determina el número mínimo de quads continuos en Z para formar un quad grande
                z_count = min(z_count_list) if z_count_list else 1

                # Marca todas las posiciones del quad grande como visitadas
                for ix in range(x_count):
                    for iz in range(z_count):
                        visited.add((x + ix) + width * (z + iz))

                # Define los vértices del quad grande
                v0 = x, y, z
                v1 = x + x_count, y, z + z_count
                v2 = x + x_count, y, z
                v3 = x, y, z + z_count

                # Agrega los vértices al array de la malla
                for vertex in (v0, v1, v2, v0, v3, v1): 
                    for attr in vertex:
                        mesh[index] = attr
                        index += 1

        # Recorta el array de la malla al tamaño utilizado
        mesh = mesh[:index + 1] # Devuelve el array de la malla recortado
        # Convierte el array de la malla a un tipo de dato adecuado para OpenGL
        return mesh # Devuelve la malla construida
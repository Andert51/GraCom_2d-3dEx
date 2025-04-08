from settings import *  # Importa configuraciones globales del proyecto


class ShaderProgram:
    """
    Clase que maneja los programas de sombreado (shaders) utilizados en el motor voxel.

    Esta clase carga, configura y actualiza los shaders necesarios para renderizar
    diferentes elementos del juego, como chunks, marcadores de voxeles, agua y nubes.

    Atributos:
        app (object): Referencia a la aplicación principal.
        ctx (mgl.Context): Contexto de OpenGL para manejar los shaders.
        player (Player): Referencia al jugador, utilizada para obtener las matrices de proyección y vista.
        chunk (mgl.Program): Programa de sombreado para renderizar los chunks.
        voxel_marker (mgl.Program): Programa de sombreado para renderizar el marcador de voxeles.
        water (mgl.Program): Programa de sombreado para renderizar el agua.
        clouds (mgl.Program): Programa de sombreado para renderizar las nubes.
    """

    def __init__(self, app):
        """
        Inicializa los programas de sombreado.

        Parámetros:
            app (object): Referencia a la aplicación principal.
        """
        self.app = app  # Referencia a la aplicación principal
        self.ctx = app.ctx  # Contexto de OpenGL
        self.player = app.player  # Referencia al jugador

        # Carga los shaders para diferentes elementos del juego
        self.chunk = self.get_program(shader_name='chunk')  # Shader para los chunks
        self.voxel_marker = self.get_program(shader_name='voxel_marker')  # Shader para el marcador de voxeles
        self.water = self.get_program('water')  # Shader para el agua
        self.clouds = self.get_program('clouds')  # Shader para las nubes

        # Configura las variables uniformes iniciales en los shaders
        self.set_uniforms_on_init()

    def set_uniforms_on_init(self):
        """
        Configura las variables uniformes iniciales en los shaders.

        Este método establece valores iniciales para las matrices de proyección,
        texturas, colores y otros parámetros necesarios para cada shader.
        """
        # Configuración inicial para el shader de los chunks
        self.chunk['m_proj'].write(self.player.m_proj)  # Matriz de proyección
        self.chunk['m_model'].write(glm.mat4())  # Matriz de modelo (identidad)
        self.chunk['u_texture_array_0'] = 1  # Índice de la textura
        self.chunk['bg_color'].write(COLOR_FONDO)  # Color de fondo
        self.chunk['water_line'] = NIVEL_AGUA  # Nivel del agua

        # Configuración inicial para el shader del marcador de voxeles
        self.voxel_marker['m_proj'].write(self.player.m_proj)  # Matriz de proyección
        self.voxel_marker['m_model'].write(glm.mat4())  # Matriz de modelo (identidad)
        self.voxel_marker['u_texture_0'] = 0  # Índice de la textura

        # Configuración inicial para el shader del agua
        self.water['m_proj'].write(self.player.m_proj)  # Matriz de proyección
        self.water['u_texture_0'] = 2  # Índice de la textura
        self.water['water_area'] = AREA_AGUA  # Área del agua
        self.water['water_line'] = NIVEL_AGUA  # Nivel del agua

        # Configuración inicial para el shader de las nubes
        self.clouds['m_proj'].write(self.player.m_proj)  # Matriz de proyección
        self.clouds['center'] = CENTRO_XZ  # Centro de las nubes en el plano XZ
        self.clouds['bg_color'].write(COLOR_FONDO)  # Color de fondo
        self.clouds['cloud_scale'] = ESCALA_NUBES  # Escala de las nubes

    def update(self):
        """
        Actualiza las variables uniformes dinámicas en los shaders.

        Este método actualiza la matriz de vista (`m_view`) en todos los shaders
        para reflejar la posición y orientación actual del jugador.
        """
        self.chunk['m_view'].write(self.player.m_view)  # Actualiza la matriz de vista para los chunks
        self.voxel_marker['m_view'].write(self.player.m_view)  # Actualiza la matriz de vista para el marcador de voxeles
        self.water['m_view'].write(self.player.m_view)  # Actualiza la matriz de vista para el agua
        self.clouds['m_view'].write(self.player.m_view)  # Actualiza la matriz de vista para las nubes

    def get_program(self, shader_name):
        """
        Carga un programa de sombreado (shader) desde archivos de texto.

        Parámetros:
            shader_name (str): Nombre del shader (sin extensión).

        Retorna:
            mgl.Program: Programa de sombreado compilado.
        """
        # Carga el código del shader de vértices
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()

        # Carga el código del shader de fragmentos
        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        # Compila y retorna el programa de sombreado
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
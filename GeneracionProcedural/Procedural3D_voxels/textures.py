import pygame as pg  # Biblioteca para cargar y manipular imágenes
import moderngl as mgl  # Biblioteca para renderizado moderno en OpenGL


class Textures:
    """
    Clase que maneja las texturas utilizadas en el motor voxel.

    Esta clase se encarga de cargar texturas desde archivos, configurarlas
    y asignarlas a unidades de textura para su uso en los shaders.

    Atributos:
        app (object): Referencia a la aplicación principal.
        ctx (mgl.Context): Contexto de OpenGL para manejar las texturas.
        texture_0 (mgl.Texture): Textura básica cargada desde 'frame.png'.
        texture_1 (mgl.Texture): Textura básica cargada desde 'water.png'.
        texture_array_0 (mgl.TextureArray): Array de texturas cargado desde 'tex_array_0.png'.
    """

    def __init__(self, app):
        """
        Inicializa el gestor de texturas.

        Parámetros:
            app (object): Referencia a la aplicación principal.
        """
        self.app = app  # Referencia a la aplicación principal
        self.ctx = app.ctx  # Contexto de OpenGL

        # Carga las texturas desde los archivos
        self.texture_0 = self.load('frame.png')  # Textura básica
        self.texture_1 = self.load('water.png')  # Textura de agua
        self.texture_array_0 = self.load('tex_array_0.png', is_tex_array=True)  # Array de texturas

        # Asigna las texturas a unidades de textura específicas
        self.texture_0.use(location=0)  # Asigna la textura básica a la unidad 0
        self.texture_array_0.use(location=1)  # Asigna el array de texturas a la unidad 1
        self.texture_1.use(location=2)  # Asigna la textura de agua a la unidad 2

    def load(self, file_name, is_tex_array=False):
        """
        Carga una textura desde un archivo y la configura para su uso en OpenGL.

        Parámetros:
            file_name (str): Nombre del archivo de la textura (ubicado en la carpeta 'assets').
            is_tex_array (bool): Indica si la textura es un array de texturas.

        Retorna:
            mgl.Texture o mgl.TextureArray: Textura cargada y configurada.
        """
        # Carga la imagen desde el archivo
        texture = pg.image.load(f'assets/{file_name}')
        # Invierte la imagen horizontalmente (necesario para la orientación de OpenGL)
        texture = pg.transform.flip(texture, flip_x=True, flip_y=False)

        if is_tex_array:
            # Si es un array de texturas, calcula el número de capas
            num_layers = 3 * texture.get_height() // texture.get_width()  # 3 texturas por capa
            # Crea un array de texturas en OpenGL
            texture = self.app.ctx.texture_array(
                size=(texture.get_width(), texture.get_height() // num_layers, num_layers),  # Dimensiones del array
                components=4,  # 4 componentes (RGBA)
                data=pg.image.tostring(texture, 'RGBA')  # Convierte la imagen a formato RGBA
            )
        else:
            # Si es una textura básica, crea una textura en OpenGL
            texture = self.ctx.texture(
                size=texture.get_size(),  # Dimensiones de la textura
                components=4,  # 4 componentes (RGBA)
                data=pg.image.tostring(texture, 'RGBA', False)  # Convierte la imagen a formato RGBA
            )

        # Configura la textura
        texture.anisotropy = 32.0  # Habilita el filtrado anisotrópico para mejorar la calidad
        texture.build_mipmaps()  # Genera mipmaps para la textura
        texture.filter = (mgl.NEAREST, mgl.NEAREST)  # Configura el filtro de textura (sin suavizado)

        return texture  # Retorna la textura configurada
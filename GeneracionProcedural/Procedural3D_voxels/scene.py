from settings import *  # Importa configuraciones globales del proyecto
import moderngl as mgl  # Biblioteca para renderizado moderno en OpenGL
from world import World  # Clase que representa el mundo voxel
from world_objects.voxel_marker import VoxelMarker  # Clase para manejar el marcador de voxeles
from world_objects.water import Water  # Clase para manejar el agua en la escena
from world_objects.clouds import Clouds  # Clase para manejar las nubes en la escena


class Scene:
    """
    Clase que representa la escena del juego.

    La escena contiene todos los elementos visibles e interactuables del mundo voxel,
    como el mundo, el marcador de voxeles, el agua y las nubes. También gestiona
    la actualización y renderizado de estos elementos.

    Atributos:
        app (object): Referencia a la aplicación principal.
        world (World): Representa el mundo voxel.
        voxel_marker (VoxelMarker): Marcador de voxeles para selección e interacción.
        water (Water): Representa el agua en la escena.
        clouds (Clouds): Representa las nubes en la escena.
    """

    def __init__(self, app):
        """
        Inicializa la escena del juego.

        Parámetros:
            app (object): Referencia a la aplicación principal.
        """
        self.app = app  # Referencia a la aplicación principal
        self.world = World(self.app)  # Inicializa el mundo voxel
        self.voxel_marker = VoxelMarker(self.world.voxel_handler)  # Inicializa el marcador de voxeles
        self.water = Water(app)  # Inicializa el agua en la escena
        self.clouds = Clouds(app)  # Inicializa las nubes en la escena

    def update(self):
        """
        Actualiza el estado de la escena.

        Este método actualiza todos los elementos de la escena, como el mundo,
        el marcador de voxeles y las nubes.
        """
        self.world.update()  # Actualiza el mundo voxel
        self.voxel_marker.update()  # Actualiza el marcador de voxeles
        self.clouds.update()  # Actualiza las nubes

    def render(self):
        """
        Renderiza la escena.

        Este método dibuja todos los elementos de la escena en el siguiente orden:
        1. Renderiza los chunks del mundo.
        2. Renderiza las nubes y el agua deshabilitando temporalmente el culling.
        3. Renderiza el marcador de voxeles.
        """
        # Renderiza los chunks del mundo
        self.world.render()

        # Renderiza elementos sin culling (nubes y agua)
        self.app.ctx.disable(mgl.CULL_FACE)  # Deshabilita el culling para renderizar ambos lados de los triángulos
        self.clouds.render()  # Renderiza las nubes
        self.water.render()  # Renderiza el agua
        self.app.ctx.enable(mgl.CULL_FACE)  # Vuelve a habilitar el culling

        # Renderiza el marcador de voxeles
        self.voxel_marker.render()
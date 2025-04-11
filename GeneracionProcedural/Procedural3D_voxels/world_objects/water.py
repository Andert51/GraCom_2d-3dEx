from meshes.quad_mesh import QuadMesh  # Importa la clase QuadMesh para manejar la malla del agua
from settings import *  # Importa configuraciones globales del proyecto


class Water:
    """
    Clase que representa el agua en el mundo voxel.

    Esta clase maneja la creación y renderizado de la malla del agua.
    Utiliza la clase `QuadMesh` para generar y renderizar la malla del agua.

    Atributos:
        app (object): Referencia a la aplicación principal.
        mesh (QuadMesh): Malla asociada al agua para su renderizado.
    """

    def __init__(self, app):
        """
        Inicializa el objeto de agua.

        Parámetros:
            app (object): Referencia a la aplicación principal.
        """
        self.app = app  # Referencia a la aplicación principal
        self.mesh = QuadMesh(app)  # Crea la malla del agua utilizando la clase QuadMesh

    def render(self):
        """
        Renderiza el agua.

        Este método llama al método `render` de la malla del agua para dibujarla
        en la pantalla.
        """
        self.mesh.render()  # Renderiza la malla del agua
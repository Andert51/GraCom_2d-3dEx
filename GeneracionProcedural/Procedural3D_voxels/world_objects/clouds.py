from settings import *  # Importa configuraciones globales del proyecto
from meshes.cloud_mesh import CloudMesh  # Importa la clase CloudMesh para manejar la malla de las nubes


class Clouds:
    """
    Clase que representa las nubes en el mundo voxel.

    Esta clase maneja la creación, actualización y renderizado de las nubes.
    Utiliza la clase `CloudMesh` para generar y renderizar la malla de las nubes.

    Atributos:
        app (object): Referencia a la aplicación principal.
        mesh (CloudMesh): Malla asociada a las nubes para su renderizado.
    """

    def __init__(self, app):
        """
        Inicializa las nubes.

        Parámetros:
            app (object): Referencia a la aplicación principal.
        """
        self.app = app  # Referencia a la aplicación principal
        self.mesh = CloudMesh(app)  # Crea la malla de las nubes utilizando la clase CloudMesh

    def update(self):
        """
        Actualiza las nubes.

        Este método actualiza el tiempo uniforme (`u_time`) en el programa de sombreado
        asociado a las nubes, lo que permite animar las nubes (por ejemplo, movimiento).
        """
        self.mesh.program['u_time'] = self.app.time  # Actualiza el tiempo en el shader

    def render(self):
        """
        Renderiza las nubes.

        Este método llama al método `render` de la malla de las nubes para dibujarlas
        en la pantalla.
        """
        self.mesh.render()  # Renderiza la malla de las nubes
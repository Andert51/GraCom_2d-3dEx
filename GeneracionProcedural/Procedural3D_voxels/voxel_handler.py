from settings import *  # Importa configuraciones globales del proyecto
from meshes.chunk_mesh_builder import get_chunk_index  # Función para obtener el índice de un chunk


class VoxelHandler:
    """
    Clase que maneja la interacción con los voxeles en el mundo voxel.

    Esta clase permite agregar y eliminar voxeles, reconstruir mallas de chunks
    afectados y realizar ray casting para detectar voxeles seleccionados.

    Atributos:
        app (object): Referencia a la aplicación principal.
        chunks (list): Lista de chunks en el mundo.
        chunk (Chunk): Chunk actual seleccionado por el ray casting.
        voxel_id (int): ID del voxel seleccionado.
        voxel_index (int): Índice del voxel seleccionado dentro del chunk.
        voxel_local_pos (glm.ivec3): Posición local del voxel dentro del chunk.
        voxel_world_pos (glm.ivec3): Posición global del voxel en el mundo.
        voxel_normal (glm.ivec3): Normal del voxel seleccionado (dirección de interacción).
        interaction_mode (int): Modo de interacción (0: eliminar voxel, 1: agregar voxel).
        new_voxel_id (int): ID del voxel que se agregará en modo de interacción.
    """

    def __init__(self, world):
        """
        Inicializa el manejador de voxeles.

        Parámetros:
            world (World): Referencia al mundo voxel.
        """
        self.app = world.app  # Referencia a la aplicación principal
        self.chunks = world.chunks  # Lista de chunks en el mundo

        # Resultados del ray casting
        self.chunk = None
        self.voxel_id = None
        self.voxel_index = None
        self.voxel_local_pos = None
        self.voxel_world_pos = None
        self.voxel_normal = None

        self.interaction_mode = 0  # 0: eliminar voxel, 1: agregar voxel
        self.new_voxel_id = TEXTURA_TIERRA  # ID del voxel que se agregará

    def add_voxel(self):
        """
        Agrega un voxel en la posición seleccionada si está vacía.
        """
        if self.voxel_id:
            # Verifica si la posición en la dirección de la normal está vacía
            result = self.get_voxel_id(self.voxel_world_pos + self.voxel_normal)

            if not result[0]:  # Si la posición está vacía
                _, voxel_index, _, chunk = result
                chunk.voxels[voxel_index] = self.new_voxel_id  # Asigna el nuevo ID de voxel
                chunk.mesh.rebuild()  # Reconstruye la malla del chunk

                # Si el chunk estaba vacío, actualiza su estado
                if chunk.is_empty:
                    chunk.is_empty = False

    def remove_voxel(self):
        """
        Elimina el voxel seleccionado y reconstruye los chunks afectados.
        """
        if self.voxel_id:
            self.chunk.voxels[self.voxel_index] = 0  # Elimina el voxel (ID = 0)
            self.chunk.mesh.rebuild()  # Reconstruye la malla del chunk
            self.rebuild_adjacent_chunks()  # Reconstruye los chunks adyacentes si es necesario

    def rebuild_adj_chunk(self, adj_voxel_pos):
        """
        Reconstruye la malla de un chunk adyacente.

        Parámetros:
            adj_voxel_pos (tuple): Posición global del voxel adyacente.
        """
        index = get_chunk_index(adj_voxel_pos)
        if index != -1:
            self.chunks[index].mesh.rebuild()

    def rebuild_adjacent_chunks(self):
        """
        Reconstruye las mallas de los chunks adyacentes si el voxel modificado
        está en el borde del chunk actual.
        """
        lx, ly, lz = self.voxel_local_pos
        wx, wy, wz = self.voxel_world_pos

        if lx == 0:
            self.rebuild_adj_chunk((wx - 1, wy, wz))
        elif lx == TAMANO_CHUNK - 1:
            self.rebuild_adj_chunk((wx + 1, wy, wz))

        if ly == 0:
            self.rebuild_adj_chunk((wx, wy - 1, wz))
        elif ly == TAMANO_CHUNK - 1:
            self.rebuild_adj_chunk((wx, wy + 1, wz))

        if lz == 0:
            self.rebuild_adj_chunk((wx, wy, wz - 1))
        elif lz == TAMANO_CHUNK - 1:
            self.rebuild_adj_chunk((wx, wy, wz + 1))

    def set_voxel(self):
        """
        Establece un voxel en la posición seleccionada según el modo de interacción.
        """
        if self.interaction_mode:
            self.add_voxel()
        else:
            self.remove_voxel()

    def switch_mode(self):
        """
        Cambia el modo de interacción entre agregar y eliminar voxeles.
        """
        self.interaction_mode = not self.interaction_mode

    def update(self):
        """
        Actualiza el estado del manejador de voxeles, incluyendo el ray casting.
        """
        self.ray_cast()

    def ray_cast(self):
        """
        Realiza un ray casting desde la posición del jugador para detectar
        el voxel seleccionado.

        Retorna:
            bool: True si se detecta un voxel, False en caso contrario.
        """
        # Punto inicial del rayo (posición del jugador)
        x1, y1, z1 = self.app.player.position
        # Punto final del rayo (posición hacia adelante del jugador)
        x2, y2, z2 = self.app.player.position + self.app.player.forward * DISTANCIA_MAX_RAYO

        current_voxel_pos = glm.ivec3(x1, y1, z1)
        self.voxel_id = 0
        self.voxel_normal = glm.ivec3(0)
        step_dir = -1

        # Calcula los pasos y las distancias en cada eje
        dx = glm.sign(x2 - x1)
        delta_x = min(dx / (x2 - x1), 10000000.0) if dx != 0 else 10000000.0
        max_x = delta_x * (1.0 - glm.fract(x1)) if dx > 0 else delta_x * glm.fract(x1)

        dy = glm.sign(y2 - y1)
        delta_y = min(dy / (y2 - y1), 10000000.0) if dy != 0 else 10000000.0
        max_y = delta_y * (1.0 - glm.fract(y1)) if dy > 0 else delta_y * glm.fract(y1)

        dz = glm.sign(z2 - z1)
        delta_z = min(dz / (z2 - z1), 10000000.0) if dz != 0 else 10000000.0
        max_z = delta_z * (1.0 - glm.fract(z1)) if dz > 0 else delta_z * glm.fract(z1)

        # Itera mientras el rayo no exceda el rango máximo
        while not (max_x > 1.0 and max_y > 1.0 and max_z > 1.0):
            result = self.get_voxel_id(voxel_world_pos=current_voxel_pos)
            if result[0]:  # Si se detecta un voxel
                self.voxel_id, self.voxel_index, self.voxel_local_pos, self.chunk = result
                self.voxel_world_pos = current_voxel_pos

                # Determina la normal del voxel seleccionado
                if step_dir == 0:
                    self.voxel_normal.x = -dx
                elif step_dir == 1:
                    self.voxel_normal.y = -dy
                else:
                    self.voxel_normal.z = -dz
                return True

            # Avanza en la dirección del rayo
            if max_x < max_y:
                if max_x < max_z:
                    current_voxel_pos.x += dx
                    max_x += delta_x
                    step_dir = 0
                else:
                    current_voxel_pos.z += dz
                    max_z += delta_z
                    step_dir = 2
            else:
                if max_y < max_z:
                    current_voxel_pos.y += dy
                    max_y += delta_y
                    step_dir = 1
                else:
                    current_voxel_pos.z += dz
                    max_z += delta_z
                    step_dir = 2
        return False

    def get_voxel_id(self, voxel_world_pos):
        """
        Obtiene el ID del voxel en una posición global específica.

        Parámetros:
            voxel_world_pos (glm.ivec3): Posición global del voxel.

        Retorna:
            tuple: (voxel_id, voxel_index, voxel_local_pos, chunk) si el voxel existe,
                   (0, 0, 0, 0) en caso contrario.
        """
        cx, cy, cz = chunk_pos = voxel_world_pos / TAMANO_CHUNK

        if 0 <= cx < ANCHURA_MUNDO and 0 <= cy < ALTURA_MUNDO and 0 <= cz < PROFUNDIDAD_MUNDO:
            chunk_index = cx + ANCHURA_MUNDO * cz + AREA_MUNDO * cy
            chunk = self.chunks[chunk_index]

            lx, ly, lz = voxel_local_pos = voxel_world_pos - chunk_pos * TAMANO_CHUNK

            voxel_index = lx + TAMANO_CHUNK * lz + AREA_CHUNK * ly
            voxel_id = chunk.voxels[voxel_index]

            return voxel_id, voxel_index, voxel_local_pos, chunk
        return 0, 0, 0, 0
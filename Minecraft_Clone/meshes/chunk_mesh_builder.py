from settings import *  # Importa configuraciones globales del proyecto
from numba import uint8  # Importa el tipo de dato uint8 de Numba para optimización


@njit
def get_ao(local_pos, world_pos, world_voxels, plane):
    """
    Calcula la oclusión ambiental (Ambient Occlusion, AO) para un voxel en una posición específica.

    Parámetros:
        local_pos (tuple): Posición local del voxel dentro del chunk (x, y, z).
        world_pos (tuple): Posición global del voxel en el mundo (wx, wy, wz).
        world_voxels (array): Array que contiene los datos de los voxeles del mundo.
        plane (str): El plano en el que se calcula la AO ('X', 'Y' o 'Z').

    Retorna:
        tuple: Valores de oclusión ambiental para los vértices de la cara.
    """
    x, y, z = local_pos
    wx, wy, wz = world_pos

    # Calcula la AO dependiendo del plano (Y, X o Z)
    if plane == 'Y':  # Plano horizontal (superior/inferior)
        a = is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels)
        b = is_void((x - 1, y, z - 1), (wx - 1, wy, wz - 1), world_voxels)
        c = is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels)
        d = is_void((x - 1, y, z + 1), (wx - 1, wy, wz + 1), world_voxels)
        e = is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels)
        f = is_void((x + 1, y, z + 1), (wx + 1, wy, wz + 1), world_voxels)
        g = is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels)
        h = is_void((x + 1, y, z - 1), (wx + 1, wy, wz - 1), world_voxels)

    elif plane == 'X':  # Plano vertical (izquierda/derecha)
        a = is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels)
        b = is_void((x, y - 1, z - 1), (wx, wy - 1, wz - 1), world_voxels)
        c = is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels)
        d = is_void((x, y - 1, z + 1), (wx, wy - 1, wz + 1), world_voxels)
        e = is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels)
        f = is_void((x, y + 1, z + 1), (wx, wy + 1, wz + 1), world_voxels)
        g = is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels)
        h = is_void((x, y + 1, z - 1), (wx, wy + 1, wz - 1), world_voxels)

    else:  # Plano Z (frontal/trasero)
        a = is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels)
        b = is_void((x - 1, y - 1, z), (wx - 1, wy - 1, wz), world_voxels)
        c = is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels)
        d = is_void((x + 1, y - 1, z), (wx + 1, wy - 1, wz), world_voxels)
        e = is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels)
        f = is_void((x + 1, y + 1, z), (wx + 1, wy + 1, wz), world_voxels)
        g = is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels)
        h = is_void((x - 1, y + 1, z), (wx - 1, wy + 1, wz), world_voxels)

    # Calcula los valores de AO para los vértices de la cara
    ao = (a + b + c), (g + h + a), (e + f + g), (c + d + e)
    return ao


@njit
def pack_data(x, y, z, voxel_id, face_id, ao_id, flip_id):
    # x: 6bit  y: 6bit  z: 6bit  voxel_id: 8bit  face_id: 3bit  ao_id: 2bit  flip_id: 1bit

    """
    Empaqueta los datos de un vértice en un solo entero para optimización.

    Parámetros:
        x, y, z (int): Coordenadas del vértice.
        voxel_id (int): ID del voxel.
        face_id (int): ID de la cara (0-5).
        ao_id (int): ID de la oclusión ambiental (0-3).
        flip_id (int): Indica si la cara está volteada (0 o 1).

    Retorna:
        int: Datos empaquetados en un entero.
    """
    # Define el número de bits para cada componente
    b_bit, c_bit, d_bit, e_bit, f_bit, g_bit = 6, 6, 8, 3, 2, 1
    fg_bit = f_bit + g_bit
    efg_bit = e_bit + fg_bit
    defg_bit = d_bit + efg_bit
    cdefg_bit = c_bit + defg_bit
    bcdefg_bit = b_bit + cdefg_bit

    # Empaqueta los datos en un solo entero
    packed_data = (
        x << bcdefg_bit |
        y << cdefg_bit |
        z << defg_bit |
        voxel_id << efg_bit |
        face_id << fg_bit |
        ao_id << g_bit | flip_id
    )
    return packed_data


@njit
def get_chunk_index(world_voxel_pos):
    """
    Calcula el índice del chunk al que pertenece un voxel en el mundo.

    Parámetros:
        world_voxel_pos (tuple): Posición global del voxel (wx, wy, wz).

    Retorna:
        int: Índice del chunk o -1 si está fuera de los límites del mundo.
    """
    wx, wy, wz = world_voxel_pos
    cx = wx // TAMANO_CHUNK
    cy = wy // TAMANO_CHUNK
    cz = wz // TAMANO_CHUNK

    # Verifica si el chunk está dentro de los límites del mundo
    if not (0 <= cx < ANCHURA_MUNDO and 0 <= cy < ALTURA_MUNDO and 0 <= cz < PROFUNDIDAD_MUNDO):
        return -1

    # Calcula el índice del chunk
    index = cx + ANCHURA_MUNDO * cz + AREA_MUNDO * cy
    return index


@njit
def is_void(local_voxel_pos, world_voxel_pos, world_voxels):
    """
    Determina si un voxel es vacío (no sólido).

    Parámetros:
        local_voxel_pos (tuple): Posición local del voxel dentro del chunk.
        world_voxel_pos (tuple): Posición global del voxel en el mundo.
        world_voxels (array): Array que contiene los datos de los voxeles del mundo.

    Retorna:
        bool: True si el voxel es vacío, False si es sólido.
    """
    chunk_index = get_chunk_index(world_voxel_pos)
    if chunk_index == -1:
        return False  # Fuera de los límites del mundo

    chunk_voxels = world_voxels[chunk_index]
    x, y, z = local_voxel_pos

    # Calcula el índice del voxel dentro del chunk
    voxel_index = x % TAMANO_CHUNK + z % TAMANO_CHUNK * TAMANO_CHUNK + y % TAMANO_CHUNK * AREA_CHUNK

    # Verifica si el voxel es sólido
    if chunk_voxels[voxel_index]:
        return False
    return True


@njit
def add_data(vertex_data, index, *vertices):
    """
    Agrega datos de vértices al array de datos de vértices.

    Parámetros:
        vertex_data (array): Array donde se almacenan los datos de los vértices.
        index (int): Índice actual en el array.
        *vertices: Vértices a agregar.

    Retorna:
        int: Nuevo índice después de agregar los vértices.
    """
    for vertex in vertices:
        vertex_data[index] = vertex
        index += 1
    return index


@njit
def build_chunk_mesh(chunk_voxels, format_size, chunk_pos, world_voxels):
    """
    Construye la malla de un chunk basado en los datos de los voxeles.

    Parámetros:
        chunk_voxels (array): Array de voxeles del chunk.
        format_size (int): Tamaño del formato de los datos de vértices.
        chunk_pos (tuple): Posición del chunk en el mundo (cx, cy, cz).
        world_voxels (array): Array que contiene los datos de los voxeles del mundo.

    Retorna:
        array: Datos de los vértices de la malla del chunk.
    """
    # Inicializa el array de datos de vértices
    vertex_data = np.empty(VOLUMEN_CHUNK * 18 * format_size, dtype='uint32')
    index = 0

    # Itera sobre todos los voxeles del chunk
    for x in range(TAMANO_CHUNK):
        for y in range(TAMANO_CHUNK):
            for z in range(TAMANO_CHUNK):
                voxel_id = chunk_voxels[x + TAMANO_CHUNK * z + AREA_CHUNK * y]

                if not voxel_id:  # Si el voxel está vacío, continúa
                    continue

                # Calcula la posición global del voxel
                cx, cy, cz = chunk_pos
                wx = x + cx * TAMANO_CHUNK # Posición local
                wy = y + cy * TAMANO_CHUNK # Posición local
                wz = z + cz * TAMANO_CHUNK # Posición local
                # wx, wy, wz son las posiciones globales del voxel

                # Genera las caras visibles del voxel
                # Cara superior
                if is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels):
                    ao = get_ao((x, y + 1, z), (wx, wy + 1, wz), world_voxels, plane='Y') # Calcula la AO 
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2] # Determina si la cara está volteada 

                    v0 = pack_data(x, y + 1, z, voxel_id, 0, ao[0], flip_id) # Empaqueta los datos del vértice
                    v1 = pack_data(x + 1, y + 1, z, voxel_id, 0, ao[1], flip_id) # Empaqueta los datos del vértice
                    v2 = pack_data(x + 1, y + 1, z + 1, voxel_id, 0, ao[2], flip_id) # Empaqueta los datos del vértice
                    v3 = pack_data(x, y + 1, z + 1, voxel_id, 0, ao[3], flip_id) # Empaqueta los datos del vértice
                    
                    # Agrega los datos de los vértices al array 
                    # Si flip_id es verdadero, se invierte el orden de los vértices
                    # Esto se hace para optimizar el renderizado y evitar problemas de culling

                    if flip_id:
                        index = add_data(vertex_data, index, v1, v0, v3, v1, v3, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                # (Se repite el proceso para las demás caras: inferior, derecha, izquierda, trasera y frontal)
                # Cara inferior
                # (x, y - 1, z) es la posición local del voxel 
                # (wx, wy - 1, wz) es la posición global del voxel
                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels):
                    ao = get_ao((x, y - 1, z), (wx, wy - 1, wz), world_voxels, plane='Y')
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x    , y, z    , voxel_id, 1, ao[0], flip_id)
                    v1 = pack_data(x + 1, y, z    , voxel_id, 1, ao[1], flip_id)
                    v2 = pack_data(x + 1, y, z + 1, voxel_id, 1, ao[2], flip_id)
                    v3 = pack_data(x    , y, z + 1, voxel_id, 1, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v1, v3, v0, v1, v2, v3)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # Cara derecha
                # (x + 1, y, z) es la posición local del voxel
                # (wx + 1, wy, wz) es la posición global del voxel
                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels):
                    ao = get_ao((x + 1, y, z), (wx + 1, wy, wz), world_voxels, plane='X')
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x + 1, y    , z    , voxel_id, 2, ao[0], flip_id)
                    v1 = pack_data(x + 1, y + 1, z    , voxel_id, 2, ao[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z + 1, voxel_id, 2, ao[2], flip_id)
                    v3 = pack_data(x + 1, y    , z + 1, voxel_id, 2, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Cara izquierda
                # (x - 1, y, z) es la posición local del voxel
                # (wx - 1, wy, wz) es la posición global del voxel
                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels):
                    ao = get_ao((x - 1, y, z), (wx - 1, wy, wz), world_voxels, plane='X')
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x, y    , z    , voxel_id, 3, ao[0], flip_id)
                    v1 = pack_data(x, y + 1, z    , voxel_id, 3, ao[1], flip_id)
                    v2 = pack_data(x, y + 1, z + 1, voxel_id, 3, ao[2], flip_id)
                    v3 = pack_data(x, y    , z + 1, voxel_id, 3, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # Cara trasera
                # (x, y, z - 1) es la posición local del voxel
                # (wx, wy, wz - 1) es la posición global del voxel
                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels):
                    ao = get_ao((x, y, z - 1), (wx, wy, wz - 1), world_voxels, plane='Z')
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x,     y,     z, voxel_id, 4, ao[0], flip_id)
                    v1 = pack_data(x,     y + 1, z, voxel_id, 4, ao[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z, voxel_id, 4, ao[2], flip_id)
                    v3 = pack_data(x + 1, y,     z, voxel_id, 4, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Cara frontal
                # (x, y, z + 1) es la posición local del voxel
                # (wx, wy, wz + 1) es la posición global del voxel
                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels):
                    ao = get_ao((x, y, z + 1), (wx, wy, wz + 1), world_voxels, plane='Z')
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x    , y    , z + 1, voxel_id, 5, ao[0], flip_id)
                    v1 = pack_data(x    , y + 1, z + 1, voxel_id, 5, ao[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z + 1, voxel_id, 5, ao[2], flip_id)
                    v3 = pack_data(x + 1, y    , z + 1, voxel_id, 5, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    return vertex_data[:index + 1] # Retorna los datos de los vértices construidos

from noise import noise2, noise3  # Importa funciones para generar ruido 2D y 3D
from random import random  # Importa la función para generar números aleatorios
from settings import *  # Importa configuraciones globales del proyecto


@njit
def get_height(x, z):
    """
    Calcula la altura del terreno en las coordenadas globales (x, z).

    Utiliza una combinación de ruido 2D y una máscara de isla para generar
    alturas realistas en el terreno.

    Parámetros:
        x (int): Coordenada X global.
        z (int): Coordenada Z global.

    Retorna:
        int: Altura del terreno en la posición (x, z).
    """
    # Máscara de isla para limitar el terreno a una forma circular
    island = 1 / (pow(0.0025 * math.hypot(x - CENTRO_XZ, z - CENTRO_XZ), 20) + 0.0001)
    island = min(island, 1)

    # Amplitudes para diferentes niveles de detalle
    a1 = CENTRO_Y
    a2, a4, a8 = a1 * 0.5, a1 * 0.25, a1 * 0.125

    # Frecuencias para diferentes niveles de detalle
    f1 = 0.005
    f2, f4, f8 = f1 * 2, f1 * 4, f1 * 8

    # Ajusta la amplitud principal si el ruido inicial es negativo
    if noise2(0.1 * x, 0.1 * z) < 0:
        a1 /= 1.07

    # Calcula la altura combinando diferentes niveles de ruido
    height = 0
    height += noise2(x * f1, z * f1) * a1 + a1
    height += noise2(x * f2, z * f2) * a2 - a2
    height += noise2(x * f4, z * f4) * a4 + a4
    height += noise2(x * f8, z * f8) * a8 - a8

    # Asegura que la altura mínima sea mayor que un valor base
    height = max(height, noise2(x * f8, z * f8) + 2)
    height *= island  # Aplica la máscara de isla

    return int(height)


@njit
def get_index(x, y, z):
    """
    Calcula el índice lineal en el array de voxeles para las coordenadas (x, y, z).

    Parámetros:
        x (int): Coordenada X local dentro del chunk.
        y (int): Coordenada Y local dentro del chunk.
        z (int): Coordenada Z local dentro del chunk.

    Retorna:
        int: Índice lineal en el array de voxeles.
    """
    return x + TAMANO_CHUNK * z + AREA_CHUNK * y


@njit
def set_voxel_id(voxels, x, y, z, wx, wy, wz, world_height):
    """
    Establece el ID del voxel en la posición (x, y, z) dentro del chunk.

    Parámetros:
        voxels (np.array): Array que contiene los datos de los voxeles.
        x (int): Coordenada X local dentro del chunk.
        y (int): Coordenada Y local dentro del chunk.
        z (int): Coordenada Z local dentro del chunk.
        wx (int): Coordenada X global.
        wy (int): Coordenada Y global.
        wz (int): Coordenada Z global.
        world_height (int): Altura del terreno en la posición global (wx, wz).
    """
    voxel_id = 0

    if wy < world_height - 1:
        # Genera cuevas si se cumplen las condiciones de ruido
        if (noise3(wx * 0.09, wy * 0.09, wz * 0.09) > 0 and
                noise2(wx * 0.1, wz * 0.1) * 3 + 3 < wy < world_height - 10):
            voxel_id = 0  # Voxel vacío (cueva)
        else:
            voxel_id = TEXTURA_PIEDRA  # Voxel de piedra
    else:
        # Determina el tipo de voxel en la superficie
        rng = int(7 * random())
        ry = wy - rng
        if NIVEL_NIEVE <= ry < world_height:
            voxel_id = TEXTURA_NIEVE
        elif NIVEL_PIEDRA <= ry < NIVEL_NIEVE:
            voxel_id = TEXTURA_PIEDRA
        elif NIVEL_TIERRA <= ry < NIVEL_PIEDRA:
            voxel_id = TEXTURA_TIERRA
        elif NIVEL_HIERBA <= ry < NIVEL_TIERRA:
            voxel_id = TEXTURA_HIERBA
        else:
            voxel_id = TEXTURA_ARENA

    # Asigna el ID del voxel al array
    voxels[get_index(x, y, z)] = voxel_id

    # Intenta colocar un árbol si el voxel es de hierba
    if wy < NIVEL_TIERRA:
        place_tree(voxels, x, y, z, voxel_id)


@njit
def place_tree(voxels, x, y, z, voxel_id):
    """
    Coloca un árbol en la posición (x, y, z) si se cumplen las condiciones.

    Parámetros:
        voxels (np.array): Array que contiene los datos de los voxeles.
        x (int): Coordenada X local dentro del chunk.
        y (int): Coordenada Y local dentro del chunk.
        z (int): Coordenada Z local dentro del chunk.
        voxel_id (int): ID del voxel en la posición actual.
    """
    rnd = random() # Genera un número aleatorio entre 0 y 1
    # Verifica si se puede colocar un árbol
    # y si está dentro de los límites del chunk
    # y si el voxel actual es de hierba
    # y si cumple con la probabilidad de generación
    if voxel_id != TEXTURA_HIERBA or rnd > PROBABILIDAD_ARBOL: # Verifica si el voxel es hierba
        # y si cumple con la probabilidad de generación
        return None  # No coloca un árbol si no es hierba o no cumple la probabilidad
    if y + ALTURA_ARBOL >= TAMANO_CHUNK:
        return None  # No coloca un árbol si excede la altura del chunk
    if x - MITAD_ANCHURA_ARBOL < 0 or x + MITAD_ANCHURA_ARBOL >= TAMANO_CHUNK:
        return None  # No coloca un árbol si excede los límites en X
    if z - MITAD_ANCHURA_ARBOL < 0 or z + MITAD_ANCHURA_ARBOL >= TAMANO_CHUNK:
        return None  # No coloca un árbol si excede los límites en Z

    # Coloca tierra debajo del árbol
    voxels[get_index(x, y, z)] = TEXTURA_TIERRA

    # Coloca las hojas del árbol
    m = 0
    for n, iy in enumerate(range(MITAD_ALTURA_ARBOL, ALTURA_ARBOL - 1)):
        k = iy % 2
        rng = int(random() * 2)
        for ix in range(-MITAD_ANCHURA_ARBOL + m, MITAD_ANCHURA_ARBOL - m * rng):
            for iz in range(-MITAD_ANCHURA_ARBOL + m * rng, MITAD_ANCHURA_ARBOL - m):
                if (ix + iz) % 4:
                    voxels[get_index(x + ix + k, y + iy, z + iz + k)] = TEXTURA_HOJAS
        m += 1 if n > 0 else 3 if n > 1 else 0

    # Coloca el tronco del árbol
    for iy in range(1, ALTURA_ARBOL - 2):
        voxels[get_index(x, y + iy, z)] = TEXTURA_MADERA

    # Coloca hojas en la parte superior del árbol
    voxels[get_index(x, y + ALTURA_ARBOL - 2, z)] = TEXTURA_HOJAS
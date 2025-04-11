from settings import SEMILLA  # Importa la semilla global definida en la configuración
from numba import njit  # Importa el decorador `njit` para optimización con Numba
from opensimplex.internals import _noise2, _noise3, _init  # Importa funciones internas de OpenSimplex

# Inicializa las tablas de permutación y gradientes utilizando la semilla definida
perm, perm_grad_index3 = _init(seed=SEMILLA)


@njit(cache=True)
def noise2(x, y):
    """
    Genera ruido 2D utilizando el algoritmo OpenSimplex.

    Parámetros:
        x (float): Coordenada X en el espacio 2D.
        y (float): Coordenada Y en el espacio 2D.

    Retorna:
        float: Valor de ruido en el rango [-1, 1] para las coordenadas dadas.
    """
    return _noise2(x, y, perm)  # Llama a la función interna de OpenSimplex para ruido 2D


@njit(cache=True)
def noise3(x, y, z):
    """
    Genera ruido 3D utilizando el algoritmo OpenSimplex.

    Parámetros:
        x (float): Coordenada X en el espacio 3D.
        y (float): Coordenada Y en el espacio 3D.
        z (float): Coordenada Z en el espacio 3D.

    Retorna:
        float: Valor de ruido en el rango [-1, 1] para las coordenadas dadas.
    """
    return _noise3(x, y, z, perm, perm_grad_index3)  # Llama a la función interna de OpenSimplex para ruido 3D
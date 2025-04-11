from numba import njit # Importa la biblioteca numba para optimización de código
import numpy as np # Importa la biblioteca numpy para operaciones numéricas
import glm # Importa la biblioteca glm para operaciones matemáticas en 3D y matrices
import math # Importa la biblioteca math para operaciones matemáticas 

# Configuración de OpenGL
VERSION_MAYOR, VERSION_MENOR = 3, 3  # Versión de OpenGL
TAMANO_PROFUNDIDAD = 24  # Tamaño del buffer de profundidad
MUESTRAS_ANTIALIASING = 1  # Antialiasing (número de muestras)

# Resolución de la ventana
RESOLUCION_VENTANA = glm.vec2(1600, 900)

# Configuración de generación del mundo
SEMILLA = 16  # Semilla para la generación del mundo

# Configuración de ray casting
DISTANCIA_MAX_RAYO = 6  # Distancia máxima para el ray casting

# Configuración de chunks
TAMANO_CHUNK = 48  # Tamaño de un chunk
MITAD_TAMANO_CHUNK = TAMANO_CHUNK // 2  # Mitad del tamaño del chunk
AREA_CHUNK = TAMANO_CHUNK * TAMANO_CHUNK  # Área de un chunk
VOLUMEN_CHUNK = AREA_CHUNK * TAMANO_CHUNK  # Volumen de un chunk
RADIO_ESFERA_CHUNK = MITAD_TAMANO_CHUNK * math.sqrt(3)  # Radio de la esfera circunscrita al chunk

# Configuración del mundo
ANCHURA_MUNDO, ALTURA_MUNDO = 20, 2  # Dimensiones del mundo
PROFUNDIDAD_MUNDO = ANCHURA_MUNDO  # Profundidad del mundo
AREA_MUNDO = ANCHURA_MUNDO * PROFUNDIDAD_MUNDO  # Área del mundo
VOLUMEN_MUNDO = AREA_MUNDO * ALTURA_MUNDO  # Volumen del mundo

# Centro del mundo
CENTRO_XZ = ANCHURA_MUNDO * MITAD_TAMANO_CHUNK  # Coordenadas XZ del centro
CENTRO_Y = ALTURA_MUNDO * MITAD_TAMANO_CHUNK  # Coordenada Y del centro

# Configuración de la cámara
RELACION_ASPECTO = RESOLUCION_VENTANA.x / RESOLUCION_VENTANA.y  # Relación de aspecto
FOV_VERTICAL_GRADOS = 50  # Campo de visión vertical en grados
FOV_VERTICAL_RADIANES = glm.radians(FOV_VERTICAL_GRADOS)  # Campo de visión vertical en radianes
FOV_HORIZONTAL = 2 * math.atan(math.tan(FOV_VERTICAL_RADIANES * 0.5) * RELACION_ASPECTO)  # Campo de visión horizontal
DISTANCIA_CERCANA = 0.1  # Distancia cercana del plano de recorte
DISTANCIA_LEJANA = 2000.0  # Distancia lejana del plano de recorte
MAX_PITCH = glm.radians(89)  # Máximo ángulo de inclinación de la cámara

# Configuración del jugador
VELOCIDAD_JUGADOR = 0.005  # Velocidad de movimiento del jugador
VELOCIDAD_ROTACION_JUGADOR = 0.003  # Velocidad de rotación del jugador
POSICION_INICIAL_JUGADOR = glm.vec3(CENTRO_XZ, TAMANO_CHUNK, CENTRO_XZ)  # Posición inicial del jugador
SENSIBILIDAD_MOUSE = 0.002  # Sensibilidad del ratón

# Colores
COLOR_FONDO = glm.vec3(0.58, 0.83, 0.99)  # Color de fondo del cielo

# Texturas
TEXTURA_ARENA = 1
TEXTURA_HIERBA = 2
TEXTURA_TIERRA = 3
TEXTURA_PIEDRA = 4
TEXTURA_NIEVE = 5
TEXTURA_HOJAS = 6
TEXTURA_MADERA = 7

# Niveles del terreno
NIVEL_NIEVE = 54
NIVEL_PIEDRA = 49
NIVEL_TIERRA = 40
NIVEL_HIERBA = 8
NIVEL_ARENA = 7

# Configuración de árboles
PROBABILIDAD_ARBOL = 0.02  # Probabilidad de generar un árbol
ANCHURA_ARBOL, ALTURA_ARBOL = 4, 8  # Dimensiones del árbol
MITAD_ANCHURA_ARBOL, MITAD_ALTURA_ARBOL = ANCHURA_ARBOL // 2, ALTURA_ARBOL // 2  # Mitades de las dimensiones del árbol

# Configuración del agua
NIVEL_AGUA = 5.6  # Nivel del agua
AREA_AGUA = 5 * TAMANO_CHUNK * ANCHURA_MUNDO  # Área del agua

# Configuración de nubes
ESCALA_NUBES = 25  # Escala de las nubes
ALTURA_NUBES = ALTURA_MUNDO * TAMANO_CHUNK * 2  # Altura de las nubes
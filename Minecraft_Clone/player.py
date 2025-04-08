import pygame as pg  # Biblioteca para manejar eventos y entrada del usuario
from camera import Camera  # Clase base para manejar la cámara
from settings import *  # Importa configuraciones globales del proyecto


class Player(Camera):
    """
    Clase que representa al jugador en el mundo voxel.

    Hereda de la clase `Camera` para manejar la posición, orientación y movimiento
    del jugador en el mundo. Además, gestiona la interacción del jugador con el entorno,
    como agregar o eliminar voxeles.

    Atributos:
        app (object): Referencia a la aplicación principal.
    """

    def __init__(self, app, position=POSICION_INICIAL_JUGADOR, yaw=-90, pitch=0):
        """
        Inicializa al jugador.

        Parámetros:
            app (object): Referencia a la aplicación principal.
            position (tuple): Posición inicial del jugador en el mundo.
            yaw (float): Ángulo inicial de rotación horizontal (en grados).
            pitch (float): Ángulo inicial de rotación vertical (en grados).
        """
        self.app = app  # Referencia a la aplicación principal
        super().__init__(position, yaw, pitch)  # Inicializa la cámara con la posición y orientación iniciales

    def update(self):
        """
        Actualiza el estado del jugador.

        Este método maneja el control del teclado y el mouse, y actualiza
        la posición y orientación del jugador.
        """
        self.keyboard_control()  # Maneja el movimiento del jugador con el teclado
        self.mouse_control()  # Maneja la rotación del jugador con el mouse
        super().update()  # Llama al método de actualización de la cámara

    def handle_event(self, event):
        """
        Maneja los eventos de entrada del usuario relacionados con el jugador.

        Este método permite al jugador interactuar con los voxeles, como agregar
        o eliminar voxeles con clics del mouse.

        Parámetros:
            event (pg.event.Event): Evento de entrada capturado por Pygame.
        """
        if event.type == pg.MOUSEBUTTONDOWN:  # Si se presiona un botón del mouse
            voxel_handler = self.app.scene.world.voxel_handler  # Referencia al manejador de voxeles
            if event.button == 1:  # Botón izquierdo del mouse
                voxel_handler.set_voxel()  # Agrega un voxel en la posición seleccionada
            if event.button == 3:  # Botón derecho del mouse
                voxel_handler.switch_mode()  # Cambia el modo de interacción del jugador

    def mouse_control(self):
        """
        Maneja la rotación del jugador utilizando el movimiento del mouse.

        Este método ajusta los ángulos de rotación horizontal (`yaw`) y vertical (`pitch`)
        en función del movimiento del mouse.
        """
        mouse_dx, mouse_dy = pg.mouse.get_rel()  # Obtiene el movimiento relativo del mouse
        if mouse_dx:  # Si hay movimiento horizontal
            self.rotate_yaw(delta_x=mouse_dx * SENSIBILIDAD_MOUSE)  # Ajusta el ángulo horizontal
        if mouse_dy:  # Si hay movimiento vertical
            self.rotate_pitch(delta_y=mouse_dy * SENSIBILIDAD_MOUSE)  # Ajusta el ángulo vertical

    def keyboard_control(self):
        """
        Maneja el movimiento del jugador utilizando el teclado.

        Este método permite al jugador moverse en las direcciones adelante, atrás,
        izquierda, derecha, arriba y abajo en función de las teclas presionadas.
        """
        key_state = pg.key.get_pressed()  # Obtiene el estado actual de las teclas
        vel = VELOCIDAD_JUGADOR * self.app.delta_time  # Calcula la velocidad de movimiento basada en el tiempo entre frames

        # Movimiento hacia adelante
        if key_state[pg.K_w]:
            self.move_forward(vel)
        # Movimiento hacia atrás
        if key_state[pg.K_s]:
            self.move_back(vel)
        # Movimiento hacia la derecha
        if key_state[pg.K_d]:
            self.move_right(vel)
        # Movimiento hacia la izquierda
        if key_state[pg.K_a]:
            self.move_left(vel)
        # Movimiento hacia arriba
        if key_state[pg.K_q]:
            self.move_up(vel)
        # Movimiento hacia abajo
        if key_state[pg.K_e]:
            self.move_down(vel)
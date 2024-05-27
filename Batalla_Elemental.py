import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import math
import random
import imageio
import threading
import pygame  # Importa el módulo pygame
from PIL import Image, ImageTk, ImageDraw, ImageFont

# Configuración inicial
TAMAÑO_CASILLA = 80  # Tamaño de la casilla del tablero
COLOR_FUEGO = "#ff4500"  # Naranja
COLOR_AGUA = "#1e90ff"   # Azul dodger
COLOR_AIRE = "#00ced1"   # Turquesa oscuro
COLOR_REY = "#ffd700"    # Oro
COLOR_VACIO = "#f0f0f0"
DIMENSION_TABLERO = 8
FUENTE = ('Verdana', 20, 'bold')  # Tamaño y estilo de la fuente mejorados
COLOR_CASILLA_CLARA = "#f0d9b5"  # Un color claro para una casilla
COLOR_CASILLA_OSCURA = "#b58863"  # Un color oscuro para la otra casilla
Cantidad=0

# Inicializa pygame
pygame.init()

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Juego Elemental")
ventana.configure(bg='black')


# Crear una etiqueta para mostrar el turno
label_turno = tk.Label(ventana, text="Turno: Jugador", font=FUENTE, fg='white', bg='black')
label_turno.pack()

# Cargar sonido de fondo
sonido_fondo = pygame.mixer.Sound("sonidos/batalla_fondo.wav")  # Asegúrate de tener un archivo de sonido en la carpeta sonidos
sonido_fondo.set_volume(5)  # Ajusta el volumen del sonido de fondo (0.0 a 1.0)

# Cargar sonido de captura
sonido_captura = pygame.mixer.Sound("sonidos/muerte.wav")  # Asegúrate de tener un archivo de sonido en la carpeta sonidos
sonido_captura.set_volume(1.2)  # Ajusta el volumen del sonido de captura

# Cargar sonido de ganar partida
sonido_win_game = pygame.mixer.Sound("sonidos/win_game.wav")  # Asegúrate de tener un archivo de sonido en la carpeta sonidos
sonido_win_game.set_volume(1.2)  # Ajusta el volumen del sonido de ganar partida

# Cargar sonido de mover ficha
sonido_mover_ficha = pygame.mixer.Sound("sonidos/mover_ficha_.wav")  # Asegúrate de tener un archivo de sonido en la carpeta sonidos
sonido_mover_ficha.set_volume(1.2)  # Ajusta el volumen del sonido de mover ficha

# Cargar sonido de convertir rey
sonido_convertir_rey = pygame.mixer.Sound("sonidos/convertir_rey.wav")  # Asegúrate de tener un archivo de sonido en la carpeta sonidos
sonido_convertir_rey.set_volume(1.2)  # Ajusta el volumen del sonido de convertir rey

# Función para reproducir el sonido de captura
def reproducir_sonido_captura():
    pygame.mixer.Sound.play(sonido_captura)

# Función para reproducir el sonido de ganar partida
def reproducir_sonido_win_game():
    pygame.mixer.Sound.play(sonido_win_game)

# Función para reproducir el sonido de mover ficha
def reproducir_sonido_mover_ficha():
    pygame.mixer.Sound.play(sonido_mover_ficha)

# Función para reproducir el sonido de convertir rey
def reproducir_sonido_convertir_rey():
    pygame.mixer.Sound.play(sonido_convertir_rey)

# Reproducir sonido de fondo en bucle
pygame.mixer.Sound.play(sonido_fondo, loops=-1)

# Cargar imágenes usando Pillow
def cargar_imagen(ruta):
    img = Image.open(ruta)  # Abre la imagen usando Pillow
    img = img.resize((TAMAÑO_CASILLA, TAMAÑO_CASILLA), Image.Resampling.LANCZOS)  # Redimensionar imagen usando LANCZOS
    return ImageTk.PhotoImage(img)  # Convierte la imagen para que Tkinter pueda usarla
profundidad=4
imagenes = {
    'Fj': cargar_imagen("Imágenes/FuegoJugador2.jpg"),
    'Aj': cargar_imagen("Imágenes/AireJugador2.jpg"),
    'Wj': cargar_imagen("Imágenes/AguaJugador2.jpg"),
    'Rj': cargar_imagen("Imágenes/Rey_Elemental_Jugador2.jpg"),
    'Fia': cargar_imagen("Imágenes/Fuego_IA2.jpg"),
    'Aia': cargar_imagen("Imágenes/Aire_IA2.jpg"),
    'Wia': cargar_imagen("Imágenes/Agua_IA2.jpg"),
    'Ria': cargar_imagen("Imágenes/Rey_Elemental_IA2.jpg"),
    'V': None  # No imagen para casillas vacías
}

# Generar un número aleatorio entre 100 y 250 en incrementos de 20
def generar_numero_aleatorio():
    # Lista de valores posibles
    valores_posibles = list(range(-100, 251, 20))
    return random.choice(valores_posibles)

# Variables para manejar el estado del juego
origen = None

def generar_aleatorio():
    return random.choice([0, 1])

# Variables globales
nivel_dificultad = None

def menu_principal():
    def set_nivel(dificultad):
        global nivel_dificultad
        nivel_dificultad = dificultad
        ventana_dificultad.destroy()
        iniciar_juego()

    def mostrar_ayuda():
        reglas = (
            "Reglas del Juego Elemental:\n"
            "1. Cada jugador tiene fichas de fuego, agua y aire.\n"
            "2. Las fichas se mueven diagonalmente hacia adelante.\n"
            "3. Las fichas pueden capturar las fichas del oponente saltando sobre ellas.\n"
            "4. El objetivo es capturar todas las fichas del oponente  o dejarlo sin movimiento alguno.\n"
            "5. Las fichas que llegan al otro extremo del tablero se convierten en reyes y pueden moverse en ambas direcciones."
        )
        messagebox.showinfo("Ayuda", reglas)

    ventana_dificultad = tk.Toplevel(ventana)
    ventana_dificultad.title("Menú Principal")
    ventana_dificultad.geometry("800x600")  # Tamaño de la ventana ajustado para el video

    # Crear una etiqueta para el video
    video_label_dificultad = tk.Label(ventana_dificultad)
    video_label_dificultad.pack(fill="both", expand=True)

    def play_video_dificultad():
        video_name = "videos/galaxia.mp4"  # Ruta del video
        video = imageio.get_reader(video_name)
        original_delay = int(1000 / video.get_meta_data()['fps'])
        speedup_factor = 100  # Aumentar la velocidad del video (2x)
        delay = max(1, original_delay // speedup_factor)

        def stream(label):
            while True:  # Bucle infinito para repetir el video
                for image in video.iter_data():
                    frame_image = ImageTk.PhotoImage(Image.fromarray(image))
                    label.config(image=frame_image)
                    label.image = frame_image
                    label.update()
                    label.after(delay)

        thread = threading.Thread(target=stream, args=(video_label_dificultad,))
        thread.daemon = True
        thread.start()

   

    # Iniciar la reproducción del video
    play_video_dificultad()

    style_config = {
        "font": ("Helvetica", 16, "bold"),
        "bg": "#1e0c42",  # Azul oscuro, relacionado con el agua y el espacio
        "fg": "white",
        "activebackground": "#1e0c42",  # Azul más oscuro
        "width": 30,  # Ancho del botón aumentado
        "height": 2,
        "bd": 5,
        "relief": "raised",
        "highlightthickness": 0,
        "highlightbackground": "#000000"  # Fondo negro para el borde
    }

    # Crear un frame para la etiqueta del título
    frame_titulo = tk.Frame(ventana_dificultad, bg='black', bd=10, relief="ridge")
    frame_titulo.place(relx=0.5, rely=0.1, anchor="center")

    label = tk.Label(frame_titulo, text="Batalla Elemental", font=FUENTE, bg='black', fg='white')
    label.pack(pady=10, padx=20)


    def mostrar_niveles():
        # Ocultar el botón de seleccionar dificultad
        boton_seleccionar_nivel.place_forget()

        # Mostrar los botones de niveles de dificultad
        boton_principiante = tk.Button(ventana_dificultad, text="Principiante", command=lambda: set_nivel("Principiante"), **nivel_style_config)
        boton_intermedio = tk.Button(ventana_dificultad, text="Intermedio", command=lambda: set_nivel("Intermedio"), **nivel_style_config)
        boton_experto = tk.Button(ventana_dificultad, text="Experto", command=lambda: set_nivel("Experto"), **nivel_style_config)
        boton_principiante.place(relx=0.5, rely=0.25, anchor="center")
        boton_intermedio.place(relx=0.5, rely=0.35, anchor="center")
        boton_experto.place(relx=0.5, rely=0.45, anchor="center")

    # Botón para seleccionar nivel de dificultad
    boton_seleccionar_nivel = tk.Button(ventana_dificultad, text="Seleccionar nivel de dificultad", command=mostrar_niveles, **style_config)
    boton_seleccionar_nivel.place(relx=0.5, rely=0.3, anchor="center")

    # Configuración para los botones de niveles de dificultad
    nivel_style_config = style_config.copy()
    nivel_style_config.update({
        "bg": "#7d144c",  
        "activebackground": "#7d144c"
    })
    
    boton_ayuda = tk.Button(ventana_dificultad, text="Ayuda", command=mostrar_ayuda, **style_config)
    boton_ayuda.place(relx=0.5, rely=0.6, anchor="center")

    boton_salir = tk.Button(ventana_dificultad, text="Salir de Juego", command=ventana.quit, **style_config)
    boton_salir.place(relx=0.5, rely=0.75, anchor="center")

    
# Función para alternar el turno
def alternar_turno():
    global turno
    turno = 'IA' if turno == 'J' else 'J'
    actualizar_label_turno()
    ventana.update_idletasks()  # Forzar actualización de la interfaz
    if turno == 'IA':
        ventana.after(1000, turno_ia)
    # Incrementar el contador de turnos sin captura y verificar empate
    turnos_sin_captura += 1
    if turnos_sin_captura >= 50:
        mostrar_mensaje_empate()

def mostrar_mensaje_empate():
    messagebox.showinfo("Empate", "El juego ha terminado en empate después de 50 turnos sin capturas.")
    reiniciar_juego()
 

# Función para dibujar el tablero
def dibujar_tablero(estado_tablero):
    for fila in range(DIMENSION_TABLERO):
        for columna in range(DIMENSION_TABLERO):
            color_fondo = color_casilla(fila, columna)
            tipo_ficha = estado_tablero[fila][columna]
            imagen = imagenes.get(tipo_ficha, None)
            casilla = tk.Button(tablero, bg=color_fondo, image=imagen, command=lambda f=fila, c=columna: movimiento(f, c), bd=0, highlightthickness=0)
            casilla.grid(row=fila, column=columna, sticky='nsew')
            tablero.grid_rowconfigure(fila, weight=1, uniform='casilla')
            tablero.grid_columnconfigure(columna, weight=1, uniform='casilla')

# Función para obtener el prefijo de ficha según el turno
def prefijo_turno():
    return 'j' if turno == 'J' else 'ia'

turno = 'J'  # El jugador J comienza
estado_inicial = [
         ['V', 'Fia', 'V', 'Aia', 'V', 'Aia', 'V', 'Wia'],
        ['Fia', 'V', 'Fia', 'V', 'Aia', 'V', 'Wia', 'V'],
        ['V', 'Fia', 'V', 'Aia', 'V', 'Wia', 'V', 'Wia'],
        ['V'] * 8,
        ['V'] * 8,
        ['Fj', 'V', 'Fj', 'V', 'Aj', 'V', 'Wj', 'V'],
        ['V', 'Fj', 'V', 'Aj', 'V', 'Wj', 'V', 'Wj'],
        ['Fj', 'V', 'Aj', 'V', 'Aj', 'V', 'Wj', 'V']
]

# Contador de turnos sin captura
turnos_sin_captura = 0
#------------------------------------------------
def reiniciar_juego():
    global estado_inicial, turno

    # Restaurar el estado inicial del tablero
    estado_inicial = [
        ['V', 'Fia', 'V', 'Aia', 'V', 'Aia', 'V', 'Wia'],
        ['Fia', 'V', 'Fia', 'V', 'Aia', 'V', 'Wia', 'V'],
        ['V', 'Fia', 'V', 'Aia', 'V', 'Wia', 'V', 'Wia'],
        ['V'] * 8,
        ['V'] * 8,
        ['Fj', 'V', 'Fj', 'V', 'Aj', 'V', 'Wj', 'V'],
        ['V', 'Fj', 'V', 'Aj', 'V', 'Wj', 'V', 'Wj'],
        ['Fj', 'V', 'Aj', 'V', 'Aj', 'V', 'Wj', 'V']
    ]

    # Reiniciar el turno
    turno = 'J'

    # Actualizar el tablero y la etiqueta de turno
    dibujar_tablero(estado_inicial)
    actualizar_label_turno()

# Crear un botón de reinicio con estilo mejorado
boton_reiniciar = tk.Button(ventana, text="Reiniciar Juego", command=reiniciar_juego, 
                            bg="#1e3d59", fg="white", font=("Helvetica", 14, "bold"),
                            activebackground="#2d5f77", activeforeground="white",
                            bd=5, relief="raised")
boton_reiniciar.pack(pady=10, padx=20)

# -----------------------------------------------

# Función para obtener el color de la ficha
def obtener_color_ficha(tipo_ficha):
    colores = {
        'Fia': COLOR_FUEGO,
        'Fj': COLOR_FUEGO,
        'Aia': COLOR_AIRE,
        'Aj': COLOR_AIRE,
        'Wia': COLOR_AGUA,
        'Wj': COLOR_AGUA,
        'Ria': COLOR_REY,
        'Rj': COLOR_REY,
        'V': COLOR_VACIO
    }
    return colores.get(tipo_ficha, COLOR_VACIO)

# Función para obtener el color de fondo de la casilla
def color_casilla(fila, columna):
    if (fila + columna) % 2 == 0:
        return COLOR_CASILLA_CLARA
    else:
        return COLOR_CASILLA_OSCURA
    
# Función para dibujar el tablero con colores alternos
def dibujar_tablero(estado_tablero):
    for fila in range(DIMENSION_TABLERO):
        for columna in range(DIMENSION_TABLERO):
            color_fondo = color_casilla(fila, columna)
            tipo_ficha = estado_tablero[fila][columna]
            imagen = imagenes.get(tipo_ficha, None)
            casilla = tk.Button(tablero, bg=color_fondo, image=imagen, command=lambda f=fila, c=columna: movimiento(f, c), bd=0, highlightthickness=0)
            casilla.grid(row=fila, column=columna, sticky='nsew')
            # Asegúrate de que todas las casillas tienen el mismo 'weight' para que se escalen uniformemente
            tablero.grid_rowconfigure(fila, weight=1, uniform='casilla')
            tablero.grid_columnconfigure(columna, weight=1, uniform='casilla')

# Función para copiar el estado del tablero
def copiar_tablero(estado_tablero):
    return [fila[:] for fila in estado_tablero]


def evaluar_estado(estado_tablero):
    puntuacion = 0
    for fila in range(DIMENSION_TABLERO):
        for columna in range(DIMENSION_TABLERO):
            ficha = estado_tablero[fila][columna]
            if ficha == 'V':
                continue
            base_puntos = 0
            es_jugador = ficha.endswith('j')
            # Valores base para fichas y rey elemental
            if es_jugador:
                peso_ficha_jugador = 150  # Valor básico para una ficha de jugador
                base_puntos = base_puntos - peso_ficha_jugador
                if ficha.startswith('R'):
                    peso_ficha_jugador_rey = 180  # Valor adicional para un Rey Elemental
                    base_puntos = base_puntos - peso_ficha_jugador_rey
            else:
                peso_ficha_IA = 150  # Valor básico para una ficha de IA
                base_puntos = base_puntos + peso_ficha_IA
                if ficha.startswith('R'):
                    peso_ficha_IA_rey = 180  # Valor adicional para un Rey Elemental
                    base_puntos = base_puntos + peso_ficha_IA_rey

                if nivel_dificultad == "Experto":
                    # Evaluar si la ficha de IA está en riesgo
                    if esta_en_riesgo(fila, columna, estado_tablero, 'IA'):
                        base_puntos = base_puntos - 1000  # Penalización alta si la ficha está en riesgo

            # Añadir bonificación por control de centro y penalización por esquinas
            if 2 <= fila <= 5 and 2 <= columna <= 5:
                base_puntos = base_puntos + 100
            elif fila == 0 or fila == DIMENSION_TABLERO - 1 or columna == 0 or columna == DIMENSION_TABLERO - 1:
                base_puntos = base_puntos - 100

            puntuacion += base_puntos

    return puntuacion

# Función para obtener todos los movimientos posibles
def obtener_movimientos(estado_tablero, turno):
    movimientos = []
    for fila in range(DIMENSION_TABLERO):
        for columna in range(DIMENSION_TABLERO):
            if estado_tablero[fila][columna].endswith(prefijo_turno()):
                if nivel_dificultad == "Principiante":
                    movimientos.extend(obtener_movimientos_validos_principiante(fila, columna, estado_tablero, turno))
                elif nivel_dificultad == "Intermedio":
                    movimientos.extend(obtener_movimientos_validos(fila, columna, estado_tablero, turno))
                else:
                    movimientos.extend(obtener_movimientos_validos(fila, columna, estado_tablero, turno))

    if not movimientos:
       for fila in range(DIMENSION_TABLERO):
        for columna in range(DIMENSION_TABLERO):
            if estado_tablero[fila][columna].endswith(prefijo_turno()):
                    movimientos.extend(obtener_movimientos_validos_principiante(fila, columna, estado_tablero, turno))

    return movimientos

# Función para obtener los movimientos válidos desde una posición dada


def obtener_movimientos_validos(fila, columna, estado_tablero, turno):
    
    movimientos = []
    # Verificar movimientos simples primero
    for df, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        destino_fila, destino_columna = fila + df, columna + dc
        if 0 <= destino_fila < DIMENSION_TABLERO and 0 <= destino_columna < DIMENSION_TABLERO:
            if puede_moverse(fila, columna, destino_fila, destino_columna, estado_tablero, turno):
                # Simula el movimiento para ver si pone la pieza en riesgo
                ficha_original = estado_tablero[fila][columna]
                destino_original = estado_tablero[destino_fila][destino_columna]
                estado_tablero[fila][columna] = 'V'
                estado_tablero[destino_fila][destino_columna] = ficha_original
                if not esta_en_riesgo(destino_fila, destino_columna, estado_tablero, turno):
                    movimientos.append(((fila, columna), (destino_fila, destino_columna)))
                
                # Revierte el movimiento
                estado_tablero[fila][columna] = ficha_original
                estado_tablero[destino_fila][destino_columna] = destino_original
    


    # Ahora verificar movimientos de captura
    for df, dc in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
        destino_fila, destino_columna = fila + df, columna + dc
        if 0 <= destino_fila < DIMENSION_TABLERO and 0 <= destino_columna < DIMENSION_TABLERO:
            if puede_comer(fila, columna, destino_fila, destino_columna, estado_tablero, turno):
                # Asume que las capturas son siempre beneficiosas (o maneja riesgos específicos aquí si es necesario)
                movimientos.append(((fila, columna), (destino_fila, destino_columna)))

    return movimientos

def esta_en_riesgo(fila, columna, estado_tablero, turno):
    global Cantidad 
    direcciones = [(-1, -1), (-1, 1), (1, -1), (1, 1)] 
    for df, dc in direcciones:
        atacante_fila_inicio = fila + df
        atacante_columna_inicio = columna + dc
        if True: 
            if 0 <= atacante_fila_inicio < DIMENSION_TABLERO and 0 <= atacante_columna_inicio < DIMENSION_TABLERO and estado_tablero[atacante_fila_inicio][atacante_columna_inicio].endswith('j'):
                if ((atacante_fila_inicio ==  fila -1) and (atacante_columna_inicio==columna-1)):
                    atacante_fila_destino = fila + 1
                    atacante_columna_destino = columna + 1
                    atacante_fila_destino = atacante_fila_inicio+2
                    atacante_columna_destino= atacante_columna_inicio+2
                    
                    if 0 <= atacante_fila_destino < DIMENSION_TABLERO and 0 <= atacante_columna_destino < DIMENSION_TABLERO:
                        if jugador_puede_comer_ia(atacante_fila_inicio, atacante_columna_inicio, atacante_fila_destino, atacante_columna_destino, estado_tablero):
                            print(f"Riesgo detectado desde {atacante_fila_inicio}, {atacante_columna_inicio} hacia {atacante_fila_destino}, {atacante_columna_destino}")
                            return True
                if ((atacante_fila_inicio ==  fila -1) and (atacante_columna_inicio==columna+1)):  
                    atacante_fila_destino = fila + 1
                    atacante_columna_destino = columna - 1
                    atacante_fila_destino = atacante_fila_inicio+2
                    atacante_columna_destino= atacante_columna_inicio-2

                    if 0 <= atacante_fila_destino < DIMENSION_TABLERO and 0 <= atacante_columna_destino < DIMENSION_TABLERO:
                        if jugador_puede_comer_ia(atacante_fila_inicio, atacante_columna_inicio, atacante_fila_destino, atacante_columna_destino, estado_tablero):
                            print(f"Riesgo detectado desde {atacante_fila_inicio}, {atacante_columna_inicio} hacia {atacante_fila_destino}, {atacante_columna_destino}")
                            return True
                if ((atacante_fila_inicio ==  fila +1) and (atacante_columna_inicio==columna-1)):
                    atacante_fila_destino = fila - 1
                    atacante_columna_destino = columna + 1
                    atacante_fila_destino = atacante_fila_inicio-2
                    atacante_columna_destino= atacante_columna_inicio+2

                    if 0 <= atacante_fila_destino < DIMENSION_TABLERO and 0 <= atacante_columna_destino < DIMENSION_TABLERO:
                        if jugador_puede_comer_ia(atacante_fila_inicio, atacante_columna_inicio, atacante_fila_destino, atacante_columna_destino, estado_tablero):
                            print(f"Riesgo detectado desde {atacante_fila_inicio}, {atacante_columna_inicio} hacia {atacante_fila_destino}, {atacante_columna_destino}")
                            return True
                if ((atacante_fila_inicio ==  fila +1) and (atacante_columna_inicio==columna+1)):
                    atacante_fila_destino = fila - 1
                    atacante_columna_destino = columna - 1
                    atacante_fila_destino = atacante_fila_inicio-2
                    atacante_columna_destino= atacante_columna_inicio-2
                    if 0 <= atacante_fila_destino < DIMENSION_TABLERO and 0 <= atacante_columna_destino < DIMENSION_TABLERO:
                
                        if jugador_puede_comer_ia(atacante_fila_inicio, atacante_columna_inicio, atacante_fila_destino, atacante_columna_destino, estado_tablero):
                            print(f"Riesgo detectado desde {atacante_fila_inicio}, {atacante_columna_inicio} hacia {atacante_fila_destino}, {atacante_columna_destino}")
                            Cantidad += 1
                            print(Cantidad)
                            return True
    return False



def jugador_puede_comer_ia(origen_fila, origen_columna, destino_fila, destino_columna, estado_tablero):
    ficha_origen = estado_tablero[origen_fila][origen_columna]
    ficha_destino = estado_tablero[destino_fila][destino_columna]
    
    if ficha_origen.endswith('ia'):
        return False
     
    if ficha_destino != 'V':
        print(f"No puede comer porque el destino no está vacío: {destino_fila}, {destino_columna}")
        return False

    pos_intermedia_fila = (origen_fila + destino_fila) // 2
    pos_intermedia_columna = (origen_columna + destino_columna) // 2
    ficha_intermedia = estado_tablero[pos_intermedia_fila][pos_intermedia_columna]

    if ficha_intermedia == 'V' or ficha_intermedia.endswith('j'):
        print(f"No puede comer porque la intermedia no es del oponente: {pos_intermedia_fila}, {pos_intermedia_columna}")
        return False

    if abs(origen_fila - destino_fila) != 2 or abs(origen_columna - destino_columna) != 2:
        print(f"No puede comer porque no es un salto diagonal válido: {origen_fila}, {origen_columna} -> {destino_fila}, {destino_columna}")
        return False

    puede_comer_a = {
        'fj': ['aia', 'fia', 'ria'],
        'aj': ['wia', 'aia', 'ria'],
        'wj': ['fia', 'wia', 'ria'],
        'rj': ['aia', 'fia', 'wia', 'ria'],
    }

    tipo_ficha_origen = ficha_origen.lower()
    tipo_ficha_intermedia = ficha_intermedia.lower()

    es_comible = tipo_ficha_intermedia in puede_comer_a.get(tipo_ficha_origen, [])

    if 'r' in tipo_ficha_origen:
        print( 'intermedia:',pos_intermedia_fila,',',pos_intermedia_columna)
        return es_comible
    else:
        #direccion_correcta = destino_fila > origen_fila  # Jugador siempre debe moverse hacia arriba (decreciente)
        print( 'intermedia:',pos_intermedia_fila,'-',pos_intermedia_columna)
        return es_comible #and direccion_correcta





def obtener_movimientos_validos_principiante(fila, columna, estado_tablero, turno):
    movimientos = []
    for df, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        destino_fila, destino_columna = fila + df, columna + dc
        if 0 <= destino_fila < DIMENSION_TABLERO and 0 <= destino_columna < DIMENSION_TABLERO:
            if puede_moverse(fila, columna, destino_fila, destino_columna, estado_tablero, turno):
                movimientos.append(((fila, columna), (destino_fila, destino_columna)))
    
    for df, dc in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
        destino_fila, destino_columna = fila + df, columna + dc
        if 0 <= destino_fila < DIMENSION_TABLERO and 0 <= destino_columna < DIMENSION_TABLERO:
            if puede_comer(fila, columna, destino_fila, destino_columna, estado_tablero, turno):
                movimientos.append(((fila, columna), (destino_fila, destino_columna)))
    
    return movimientos

  

def hacer_movimiento(estado_tablero, movimiento):
    origen, destino = movimiento
    origen_fila, origen_columna = origen
    destino_fila, destino_columna = destino
    ficha = estado_tablero[origen_fila][origen_columna]
    estado_tablero[destino_fila][destino_columna] = ficha
    estado_tablero[origen_fila][origen_columna] = 'V'
   
     # Eliminar la ficha que se está saltando en caso de captura
    pos_intermedia_fila = (origen_fila + destino_fila) // 2
    pos_intermedia_columna = (origen_columna + destino_columna) // 2
    estado_tablero[pos_intermedia_fila][pos_intermedia_columna] = 'V'

    # Promoción a Rey Elemental si alcanza la fila correspondiente
    if destino_fila == 0 and ficha.endswith('j'):  # Fila superior para el jugador
        estado_tablero[destino_fila][destino_columna] = 'Rj'  # Promociona a Rey Elemental Jugador
    elif destino_fila == DIMENSION_TABLERO - 1 and ficha.endswith('ia'):  # Fila inferior para la IA
        estado_tablero[destino_fila][destino_columna] = 'Ria'  # Promociona a Rey Elemental IA



def hacer_movimiento(estado_tablero, movimiento):
    origen, destino = movimiento
    origen_fila, origen_columna = origen
    destino_fila, destino_columna = destino
    ficha = estado_tablero[origen_fila][origen_columna]
    
    # Verifica si el movimiento es una captura
    if puede_comer(origen_fila, origen_columna, destino_fila, destino_columna, estado_tablero, turno):
        # Captura la pieza
        estado_tablero[destino_fila][destino_columna] = ficha
        estado_tablero[origen_fila][origen_columna] = 'V'
        # Elimina la ficha que se está saltando
        pos_intermedia_fila = (origen_fila + destino_fila) // 2
        pos_intermedia_columna = (origen_columna + destino_columna) // 2
        estado_tablero[pos_intermedia_fila][pos_intermedia_columna] = 'V'
        
        # Promoción a Rey Elemental si alcanza la fila correspondiente
        if destino_fila == 0 and ficha.endswith('j'):  # Fila superior para el jugador
            estado_tablero[destino_fila][destino_columna] = 'Rj'  # Promociona a Rey Elemental Jugador
        elif destino_fila == DIMENSION_TABLERO - 1 and ficha.endswith('ia'):  # Fila inferior para la IA
            estado_tablero[destino_fila][destino_columna] = 'Ria'  # Promociona a Rey Elemental IA
    else:
        # Si no es captura, simplemente mueve la pieza
        estado_tablero[destino_fila][destino_columna] = ficha
        estado_tablero[origen_fila][origen_columna] = 'V'
        
        # Promoción a Rey Elemental si alcanza la fila correspondiente
        if destino_fila == 0 and ficha.endswith('j'):  # Fila superior para el jugador
            estado_tablero[destino_fila][destino_columna] = 'Rj'  # Promociona a Rey Elemental Jugador
        elif destino_fila == DIMENSION_TABLERO - 1 and ficha.endswith('ia'):  # Fila inferior para la IA
            estado_tablero[destino_fila][destino_columna] = 'Ria'  # Promociona


# Función para deshacer un movimiento en el tablero
def deshacer_movimiento(estado_tablero, movimiento):
    origen, destino = movimiento
    origen_fila, origen_columna = origen
    destino_fila, destino_columna = destino
    ficha = estado_tablero[destino_fila][destino_columna]
    estado_tablero[origen_fila][origen_columna] = ficha
    estado_tablero[destino_fila][destino_columna] = 'V'

# Función para determinar si un jugador puede moverse
def puede_moverse(origen_fila, origen_columna, destino_fila, destino_columna, estado_tablero, turno):
    ficha = estado_tablero[origen_fila][origen_columna]
    destino = estado_tablero[destino_fila][destino_columna]
    if ficha == 'V' or destino != 'V':
        return False  # No se puede mover si la casilla de origen está vacía o la de destino está ocupada

    # La dirección de avance para las fichas del jugador es hacia arriba (fila decrece), y para la IA hacia abajo (fila aumenta)
    direccion_avance = -1 if ficha.endswith('j') else 1

    # Movimiento diagonal
    mov_diagonal = abs(destino_fila - origen_fila) == 1 and abs(destino_columna - origen_columna) == 1

    if ficha.startswith('R'):
        # Los reyes elementales pueden moverse en cualquier dirección diagonal
        return mov_diagonal
    elif ficha.startswith('F') or ficha.startswith('W') or ficha.startswith('A'):
        # Movimiento válido para fichas de fuego, agua y aire (solo diagonal)
        return mov_diagonal and (destino_fila - origen_fila) == direccion_avance
    else:
        return False  # En caso de fichas desconocidas o vacías, no puede moverse

# Función para manejar el movimiento de las fichas
def movimiento(fila, columna):
    global origen, estado_inicial, turno
    if origen:
        origen_fila, origen_columna = origen
        ficha = estado_inicial[origen_fila][origen_columna]
        
        # Verifica si el movimiento es una captura
        if ficha.endswith(prefijo_turno()) and puede_comer(origen_fila, origen_columna, fila, columna, estado_inicial, turno):
            # Captura la pieza
            estado_inicial[fila][columna] = ficha
            estado_inicial[origen_fila][origen_columna] = 'V'
            # Si hay una pieza intermedia, debe ser eliminada
            estado_inicial[(origen_fila + fila) // 2][(origen_columna + columna) // 2] = 'V'
            # Promoción a Rey Elemental si alcanza la fila correspondiente
            if fila == 0 and ficha.endswith('j'):  # Fila superior para el jugador
                estado_inicial[fila][columna] = 'Rj'  # Promociona a Rey Elemental Jugador
            elif fila == DIMENSION_TABLERO - 1 and ficha.endswith('ia'):  # Fila inferior para la IA
                estado_inicial[fila][columna] = 'Ria'  # Promociona a Rey Elemental IA
            dibujar_tablero(estado_inicial)

            # Verifica si hay más capturas posibles
            if not puede_seguir_comiendo(fila, columna,estado_inicial, turno):
                alternar_turno()
            origen = (fila, columna) if puede_seguir_comiendo(fila, columna, estado_inicial, turno) else None

        # Si no es captura, verifica si el movimiento es válido
        elif ficha.endswith(prefijo_turno()) and puede_moverse(origen_fila, origen_columna, fila, columna, estado_inicial, turno):
            # Mueve la pieza
            estado_inicial[fila][columna] = ficha
            estado_inicial[origen_fila][origen_columna] = 'V'
            # Promoción a Rey Elemental si alcanza la fila correspondiente
            if fila == 0 and ficha.endswith('j'):  # Fila superior para el jugador
                estado_inicial[fila][columna] = 'Rj'  # Promociona a Rey Elemental Jugador
            elif fila == DIMENSION_TABLERO - 1 and ficha.endswith('ia'):  # Fila inferior para la IA
                estado_inicial[fila][columna] = 'Ria'  # Promociona a Rey Elemental IA
            dibujar_tablero(estado_inicial)
            alternar_turno()

        # Verificar si el jugador no tiene movimientos posibles
        if turno == 'J' and not obtener_movimientos(estado_inicial, 'J'):
            mostrar_mensaje_ganador("La IA(Jugador sin movimientos)")
            return
        
        if revisar_estado_meta():
            mostrar_mensaje_ganador()  # Implementar esta función para mostrar un mensaje en la GUI
            return  # Termina la ejecución adicional en la función para evitar más movimientos

        origen = None

    else:
        if estado_inicial[fila][columna].endswith(prefijo_turno()):
            origen = (fila, columna)

def puede_comer(origen_fila, origen_columna, destino_fila, destino_columna, estado_tablero, turno):
    ficha_origen = estado_tablero[origen_fila][origen_columna]
    ficha_destino = estado_tablero[destino_fila][destino_columna]

    if ficha_destino != 'V':
        return False

    pos_intermedia_fila = (origen_fila + destino_fila) // 2
    pos_intermedia_columna = (origen_columna + destino_columna) // 2
    ficha_intermedia = estado_tablero[pos_intermedia_fila][pos_intermedia_columna]

    if ficha_intermedia == 'V' or ficha_intermedia.endswith(prefijo_turno()):
        return False

    if abs(origen_fila - destino_fila) != 2 or abs(origen_columna - destino_columna) != 2:
        return False

    puede_comer_a = {
        'fj': ['aia', 'fia', 'ria'],
        'fia': ['aj', 'fj', 'rj'],
        'aj': ['wia', 'aia', 'ria'],
        'aia': ['wj', 'aj', 'rj'],
        'wj': ['fia', 'wia', 'ria'],
        'wia': ['fj', 'wj', 'rj'],
        'rj': ['aia', 'fia', 'wia', 'ria'],
        'ria': ['aj', 'fj', 'wj', 'rj'],
    }

    tipo_ficha_origen = ficha_origen.lower()
    tipo_ficha_intermedia = ficha_intermedia.lower()

    es_comible = tipo_ficha_intermedia in puede_comer_a.get(tipo_ficha_origen, [])

    if 'r' in tipo_ficha_origen:
        return es_comible
    else:
        es_turno_jugador = turno == 'J'
        direccion_correcta = (destino_fila < origen_fila if es_turno_jugador else destino_fila > origen_fila)
        return es_comible and direccion_correcta
    


# Función para determinar si hay más capturas posibles desde una posición dada
def puede_seguir_comiendo(fila, columna, estado_tablero, turno):
    """ Verifica si hay más capturas posibles desde una posición dada """
    direcciones = [(-2, 2), (-2, -2), (2, 2), (2, -2)]  # Diagonales
    for df, dc in direcciones:
        destino_fila, destino_columna = fila + df, columna + dc
        if 0 <= destino_fila < DIMENSION_TABLERO and 0 <= destino_columna < DIMENSION_TABLERO:
            if puede_comer(fila, columna, destino_fila, destino_columna, estado_tablero, turno):
                return True
    return False

def revisar_estado_meta():
    # Contar las fichas de cada tipo
    fichas_jugador = sum(ficha.endswith('j') for fila in estado_inicial for ficha in fila)
    fichas_ia = sum(ficha.endswith('ia') for fila in estado_inicial for ficha in fila)
    
    # Determinar el ganador
    if fichas_jugador == 0:
        mostrar_mensaje_ganador("IA")
        return True
    elif fichas_ia == 0:
        mostrar_mensaje_ganador("Jugador")
        return True
    
    # Si ninguno gana, el juego continúa
    return False


def mostrar_mensaje_ganador(ganador):
    reproducir_sonido_win_game()
    mensaje_ganador = f"¡Felicidades, {ganador}! Eres el campeón elemental del juego."
    messagebox.showinfo("¡Juego terminado!", mensaje_ganador)

# Función para el algoritmo minimax con poda alfa-beta
def minimax(estado_tablero, profundidad, alpha, beta, es_maximizando):
    if profundidad == 0 or revisar_estado_meta():
        return evaluar_estado(estado_tablero)

    if es_maximizando:
        max_eval = -math.inf
        for movimiento in obtener_movimientos(estado_tablero, 'IA'):
            tablero_copia = copiar_tablero(estado_tablero)
            hacer_movimiento(tablero_copia, movimiento)
            eval = minimax(tablero_copia, profundidad - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for movimiento in obtener_movimientos(estado_tablero, 'J'):
            tablero_copia = copiar_tablero(estado_tablero)
            hacer_movimiento(tablero_copia, movimiento)
            eval = minimax(tablero_copia, profundidad - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


# Función para el turno de la IA
'''
def turno_ia():
    mejor_movimiento = None
    mejor_eval = -math.inf
    
    global profundidad 
    # Obtener todos los movimientos posibles para la IA
    movimientos = obtener_movimientos(estado_inicial, 'IA')
    
    if nivel_dificultad == "Principiante":
        # Elegir aleatoriamente entre movimientos normales y movimientos de captura
        if random.choice([True, False]):
            movimientos = [movimiento for movimiento in movimientos if not puede_comer(*movimiento[0], *movimiento[1], estado_inicial, 'IA')]
        else:
            movimientos = [movimiento for movimiento in movimientos if puede_comer(*movimiento[0], *movimiento[1], estado_inicial, 'IA')]

        # Si no hay movimientos disponibles en la elección aleatoria, usar todos los movimientos
        if not movimientos:
            movimientos = obtener_movimientos(estado_inicial, 'IA')

    else:
        if nivel_dificultad == "Intermedio":
            profundidad = 1
        if nivel_dificultad == "Experto":
            profundidad = 4
        
        # Filtrar los movimientos para capturas
        movimientos_captura = [movimiento for movimiento in movimientos if puede_comer(*movimiento[0], *movimiento[1], estado_inicial, 'IA')]

        if movimientos_captura:
            movimientos = movimientos_captura

    if movimientos:
        # Evaluar los movimientos disponibles
        for movimiento in movimientos:
            tablero_copia = copiar_tablero(estado_inicial)
            hacer_movimiento(tablero_copia, movimiento)
            eval = minimax(tablero_copia, profundidad, -math.inf, math.inf, False)
            if eval > mejor_eval:
                mejor_eval = eval
                mejor_movimiento = movimiento

        if mejor_movimiento:
            # Realizar el movimiento seleccionado
            hacer_movimiento(estado_inicial, mejor_movimiento)
            if puede_comer(*mejor_movimiento[0], *mejor_movimiento[1], estado_inicial, 'IA'):
                reproducir_sonido_captura()
                fila, columna = mejor_movimiento[1]
                # Mientras haya más capturas posibles, sigue capturando
                while puede_seguir_comiendo(fila, columna, estado_inicial, 'IA'):
                    capturas_posibles = obtener_movimientos_validos(fila, columna, estado_inicial, 'IA')
                    siguiente_captura = next((m for m in capturas_posibles if puede_comer(fila, columna, *m[1], estado_inicial, 'IA')), None)
                    if siguiente_captura:
                        hacer_movimiento(estado_inicial, siguiente_captura)
                        reproducir_sonido_captura()
                        fila, columna = siguiente_captura[1]
                    else:
                        break
            else:
                reproducir_sonido_mover_ficha()

    dibujar_tablero(estado_inicial)
    alternar_turno()
    revisar_estado_meta()

    '''

def turno_ia():
    mejor_movimiento = None
    mejor_eval = -math.inf
    global profundidad 
    movimientos = obtener_movimientos(estado_inicial, 'IA')

    if nivel_dificultad=='Principiante':
         # En nivel principiante, elegir un movimiento aleatorio entre todos los movimientos posibles
        mejor_movimiento = random.choice(movimientos)
        hacer_movimiento(estado_inicial, mejor_movimiento)
        fila, columna = mejor_movimiento[1]
        reproducir_sonido_mover_ficha()

        if puede_comer(*mejor_movimiento[0], *mejor_movimiento[1], estado_inicial, 'IA') :
        
            # Mientras haya más capturas posibles, sigue capturando
            while puede_seguir_comiendo(fila, columna, estado_inicial, 'IA'):
                    capturas_posibles = obtener_movimientos_validos(fila, columna, estado_inicial, 'IA')
                    siguiente_captura = next((m for m in capturas_posibles if puede_comer(fila, columna, *m[1], estado_inicial, 'IA')), None)
                    if siguiente_captura:
                        hacer_movimiento(estado_inicial, siguiente_captura)
                        reproducir_sonido_captura()
                        fila, columna = siguiente_captura[1]
                    else:
                        break

    # Obtener todos los movimientos de captura posibles para la IA
    else:
        if nivel_dificultad == "Intermedio":
            profundidad=1
        if nivel_dificultad == "Experto":
            profundidad=4
        # Filtrar los movimientos para capturas
        movimientos_captura = [movimiento for movimiento in movimientos if puede_comer(*movimiento[0], *movimiento[1], estado_inicial, 'IA')]

        if movimientos_captura:
            # Evaluar sólo los movimientos de captura
            for movimiento in movimientos_captura:
                tablero_copia = copiar_tablero(estado_inicial)
                hacer_movimiento(tablero_copia, movimiento)
                eval = minimax(tablero_copia, 3, -math.inf, math.inf, False)
                if eval > mejor_eval:
                    mejor_eval = eval
                    mejor_movimiento = movimiento

            if mejor_movimiento:
                # Realizar la primera captura
                hacer_movimiento(estado_inicial, mejor_movimiento)
                reproducir_sonido_captura()
                fila, columna = mejor_movimiento[1]

                # Mientras haya más capturas posibles, sigue capturando
                while puede_seguir_comiendo(fila, columna, estado_inicial, 'IA'):
                    capturas_posibles = obtener_movimientos_validos(fila, columna, estado_inicial, 'IA')
                    siguiente_captura = next((m for m in capturas_posibles if puede_comer(fila, columna, *m[1], estado_inicial, 'IA')), None)
                    if siguiente_captura:
                        hacer_movimiento(estado_inicial, siguiente_captura)
                        reproducir_sonido_captura()
                        fila, columna = siguiente_captura[1]
                    else:
                        break

        else:
            # Si no hay capturas posibles, evaluar otros movimientos
            for movimiento in movimientos:
                tablero_copia = copiar_tablero(estado_inicial)
                hacer_movimiento(tablero_copia, movimiento)
                eval = minimax(tablero_copia, profundidad, -math.inf, math.inf, False)
                if eval > mejor_eval:
                    mejor_eval = eval
                    mejor_movimiento = movimiento
            reproducir_sonido_mover_ficha()

            if mejor_movimiento:
                hacer_movimiento(estado_inicial, mejor_movimiento)

    dibujar_tablero(estado_inicial)
    alternar_turno()
    revisar_estado_meta()








         

# Función para volver al menú principal
def volver_al_menu_principal():
    global ventana_tablero, tablero, boton_volver_menu, boton_reiniciar, canvas_turno

    # Destruir elementos del juego
    if ventana_tablero:
        ventana_tablero.destroy()
    tablero = None
    boton_volver_menu = None
    boton_reiniciar = None
    canvas_turno = None

    # Volver al menú principal
    menu_principal()
    
# Guardar las posiciones iniciales de los elementos
posicion_inicial_label_turno = (1000, 0)
posicion_inicial_boton_reiniciar = (325, 716)
posicion_inicial_boton_volver_menu = (520, 716)

def reposicionar_elementos(event):
    ventana_width = ventana_tablero.winfo_width()
    ventana_height = ventana_tablero.winfo_height()

    # Calcula los nuevos valores 'x' y 'y' para la etiqueta del turno basándose en las dimensiones actuales de la ventana
    nuevo_x_label_turno = posicion_inicial_label_turno[0] + (ventana_width - 1024) // 2
    nuevo_y_label_turno = posicion_inicial_label_turno[1] + (ventana_height - 768) // 2
    label_turno.place(x=nuevo_x_label_turno, y=nuevo_y_label_turno)

    # Reposicionar botón de reinicio
    nuevo_x_boton_reiniciar = posicion_inicial_boton_reiniciar[0] + (ventana_width - 1024) // 2
    nuevo_y_boton_reiniciar = posicion_inicial_boton_reiniciar[1] + (ventana_height - 768) // 2
    boton_reiniciar.place(x=nuevo_x_boton_reiniciar, y=nuevo_y_boton_reiniciar)

    # Reposicionar botón de volver al menú principal
    nuevo_x_boton_volver_menu = posicion_inicial_boton_volver_menu[0] + (ventana_width - 1024) // 2
    nuevo_y_boton_volver_menu = posicion_inicial_boton_volver_menu[1] + (ventana_height - 768) // 2
    boton_volver_menu.place(x=nuevo_x_boton_volver_menu, y=nuevo_y_boton_volver_menu)

    # Reposicionar el canvas de turno
    nuevo_x_canvas_turno = 390 + (ventana_width - 1024) // 2  # Ajusta esta posición según sea necesario
    canvas_turno.place(x=nuevo_x_canvas_turno, y=10)  # Asegura que 'y' sea la posición vertical deseada

# Llama a la función para reposicionar los elementos al cambiar el tamaño de la ventana
#ventana.bind("<Configure>", reposicionar_elementos)


# Modificar la función para iniciar el juego
def iniciar_juego():
    global ventana_tablero, tablero, boton_volver_menu, boton_reiniciar, canvas_turno

    # Crear una nueva ventana para el tablero
    ventana_tablero = tk.Toplevel(ventana)
    ventana_tablero.title("Tablero de Juego")
    ventana_tablero.geometry("1024x768")  # Tamaño adecuado para visualizar todos los componentes
    ventana_tablero.minsize(1024, 790)  # Establecer tamaño mínimo

    # Crear una etiqueta para el video
    video_label_juego = tk.Label(ventana_tablero)
    video_label_juego.place(x=0, y=0, relwidth=1, relheight=1)

    def play_video_juego():
        video_name = "videos/galaxia.mp4"  # Ruta del video
        video = imageio.get_reader(video_name)
        original_delay = int(1000 / video.get_meta_data()['fps'])
        speedup_factor = 100  # Aumentar la velocidad del video (2x)
        delay = max(1, original_delay // speedup_factor)

        def stream(label):
            while True:  # Bucle infinito para repetir el video
                for image in video.iter_data():
                    frame_image = ImageTk.PhotoImage(Image.fromarray(image))
                    label.config(image=frame_image)
                    label.image = frame_image
                    label.update()
                    label.after(delay)

        thread = threading.Thread(target=stream, args=(video_label_juego,))
        thread.daemon = True
        thread.start()

    # Iniciar la reproducción del video
    play_video_juego()
    

    # Crear el tablero con un efecto de marco
    marco = tk.Frame(ventana_tablero, bg='#1a1a1a', bd=10, relief="raised")  # Color oscuro de galaxia
    marco.place(relx=0.5, rely=0.5, anchor="center", width=660, height=660)

    # Crear el tablero dentro del marco
    tablero = tk.Frame(marco, bg='black')
    tablero.place(relx=0.5, rely=0.5, anchor="center", width=640, height=640)

    # Dibujar el tablero
    dibujar_tablero(estado_inicial)

    # Crear un botón para volver al menú principal
    boton_volver_menu = tk.Button(ventana_tablero, text="Volver al Menú Principal", command=volver_al_menu_principal, 
                                  bg="#1e3d59", fg="white", font=("Helvetica", 14, "bold"),
                                  activebackground="#2d5f77", activeforeground="white",
                                  bd=5, relief="raised")
    boton_volver_menu.place(x=20, y=20)

    # Crear un botón de reinicio con estilo mejorado
    boton_reiniciar = tk.Button(ventana_tablero, text="Reiniciar Juego", command=reiniciar_juego, 
                                bg="#1e3d59", fg="white", font=("Helvetica", 14, "bold"),
                                activebackground="#2d5f77", activeforeground="white",
                                bd=5, relief="raised")
    boton_reiniciar.place(x=20, y=700)

    # Crear un Canvas para el label de turno
    canvas_turno = tk.Canvas(ventana_tablero, width=300, height=50, highlightthickness=0)  # Aumentar el ancho total
    canvas_turno.place(x=390, y=10)

    # Dibujar el fondo del label de turno con colores oscuros de temática galaxia
    canvas_turno.create_rectangle(0, 0, 150, 50, fill='#1e0c42')  # Color oscuro de galaxia
    canvas_turno.create_rectangle(150, 0, 300, 50, fill='#7d144c')  # Otro color oscuro de galaxia

    # Añadir el texto del label de turno
    canvas_turno.create_text(75, 25, text="Turno", font=('Helvetica', 14, 'bold'), fill='white')  # Centrar el texto del primer rectángulo
    canvas_turno.create_text(225, 25, text="Jugador", font=('Helvetica', 14, 'bold'), fill='white', tag="turno_actual")  # Centrar el texto del segundo rectángulo
     # Llama a la función para reposicionar los elementos al cambiar el tamaño de la ventana del tablero
    ventana_tablero.bind("<Configure>", reposicionar_elementos)

    # Si el turno es de la IA, que realice su movimiento
    if turno == 'IA':
        turno_ia()

def actualizar_label_turno():
    if turno == 'J':
        canvas_turno.itemconfig("turno_actual", text="Jugador", fill='white')  # Color blanco
    else:
        canvas_turno.itemconfig("turno_actual", text="IA", fill='white')  # Color blanco
    reposicionar_elementos(None)  # Asegurar que la posición del canvas_turno se actualice

# Llamar a la función para seleccionar la dificultad al iniciar el juego
ventana.after(100, menu_principal)

# Ejecutar la ventana
ventana.mainloop()





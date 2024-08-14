import tkinter as tk
from tkinter import messagebox
from tkinter import font
from tkinter import ttk  # Importar ttk para la barra de progreso
from tkinter import simpledialog  # Importar simpledialog para ingresar texto
import os
from PIL import Image, ImageTk
import pygame  # Importar pygame para la música
import sys  # Importar sys para manejar el path en ejecutables

# Determinar el directorio actual o del ejecutable
if getattr(sys, 'frozen', False):
    directorio_actual = sys._MEIPASS
else:
    directorio_actual = os.path.dirname(__file__)

# Inicializar Pygame
pygame.init()

# Inicializar pygame y la música
pygame.mixer.init()
pygame.mixer.music.load(os.path.join(directorio_actual, 'musica_fondo.wav'))
pygame.mixer.music.play(-1)  # Reproducir en bucle (-1 significa infinito)

# Función para leer preguntas desde un archivo
def cargar_preguntas_desde_archivo(ruta_archivo):
    preguntas = []
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        bloques = archivo.read().split('\n\n')
        for bloque in bloques:
            partes = bloque.strip().split('\n')
            pregunta = partes[0]
            opciones = partes[1:]
            preguntas.append({"pregunta": pregunta, "opciones": opciones})
    return preguntas

# Función para leer respuestas desde un archivo
def cargar_respuestas_desde_archivo(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        respuestas = archivo.read().strip().split('\n')
    return respuestas

# Función para guardar la puntuación en un archivo
def guardar_puntuacion(nombre, puntuacion):
    ruta_archivo = os.path.join(os.path.dirname(sys.executable), 'puntuacion.txt')
    with open(ruta_archivo, 'a', encoding='utf-8') as archivo:
        archivo.write(f"{nombre}: {puntuacion} - {fecha_actual}\n")

# Función para mostrar la ventana de puntuaciones
def mostrar_puntuaciones():
    ventana_puntuaciones = tk.Toplevel(root)
    ventana_puntuaciones.title("Puntuaciones")
    ventana_puntuaciones.geometry("400x300")
    
    try:
        with open(os.path.join(os.path.dirname(sys.executable), 'puntuacion.txt'), 'r', encoding='utf-8') as archivo:
            puntuaciones = archivo.read()
    except FileNotFoundError:
        puntuaciones = "No hay puntuaciones registradas."
    
    texto_puntuaciones = tk.Text(ventana_puntuaciones, wrap='word', font=("Helvetica", 12))
    texto_puntuaciones.insert(tk.END, puntuaciones)
    texto_puntuaciones.pack(expand=True, fill='both', padx=10, pady=10)
    
    boton_volver = tk.Button(ventana_puntuaciones, text="Volver al Menú", command=ventana_puntuaciones.destroy, font=("Helvetica", 14))
    boton_volver.pack(pady=10)

# Determinar el directorio actual y construir las rutas relativas
ruta_imagen_fondo = os.path.join(directorio_actual, 'imagen.jpg')
ruta_musica_fondo = os.path.join(directorio_actual, 'musica_fondo.wav')

# Variables globales
preguntas = []
respuestas = []
pregunta_actual = 0
puntaje = 0
nombre_jugador = ""
fecha_actual = "2024-08-12"  # Actualizar con la fecha actual en formato deseado

# Función para mostrar el menú de inicio
def mostrar_menu_inicio():
    marco_menu_principal.pack(pady=20)

# Función para comenzar el juego
def iniciar_juego():
    global pregunta_actual, puntaje
    pregunta_actual = 0
    puntaje = 0
    marco_menu_dificultad.pack_forget()
    marco_cuestionario.pack(pady=20)
    actualizar_progreso()
    mostrar_pregunta()

# Función para evaluar la respuesta y avanzar a la siguiente pregunta
def siguiente_pregunta():
    global pregunta_actual, puntaje
    opcion_seleccionada = opcion_seleccionada_var.get()
    if opcion_seleccionada == respuestas[pregunta_actual]:
        puntaje += 1
    pregunta_actual += 1
    if pregunta_actual < len(preguntas):
        mostrar_pregunta()
        actualizar_progreso()
    else:
        actualizar_progreso()  # Asegurar que la barra se llene al 100% al final
        if puntaje == len(preguntas):
            mensaje = "¡Puntuación perfecta! ¡Felicidades!"
        elif puntaje >= 14:
            mensaje = f"Tu puntuación es: {puntaje}/{len(preguntas)}. ¡Buen trabajo!"
        else:
            mensaje = f"Tu puntuación es: {puntaje}/{len(preguntas)}. Sigue estudiando."
        
        messagebox.showinfo("Resultados", mensaje)
        
        # Guardar la puntuación
        nombre_jugador = simpledialog.askstring("Nombre", "Ingresa tu nombre:")
        if nombre_jugador:
            guardar_puntuacion(nombre_jugador, puntaje)
        
        root.quit()

# Función para mostrar la pregunta
def mostrar_pregunta():
    etiqueta_pregunta.config(text=preguntas[pregunta_actual]["pregunta"])
    opcion_seleccionada_var.set(None)  # Desseleccionar las opciones
    for idx, opcion in enumerate(preguntas[pregunta_actual]["opciones"]):
        botones_radio[idx].config(text=opcion, value=opcion)

# Función para seleccionar dificultad
def seleccionar_dificultad(dificultad):
    global preguntas, respuestas
    if dificultad == "facil":
        ruta_preguntas = os.path.join(directorio_actual, 'preguntas_faciles.txt')
        ruta_respuestas = os.path.join(directorio_actual, 'respuestas_faciles.txt')
    elif dificultad == "normal":
        ruta_preguntas = os.path.join(directorio_actual, 'preguntas_normales.txt')
        ruta_respuestas = os.path.join(directorio_actual, 'respuestas_normales.txt')
    elif dificultad == "dificil":
        ruta_preguntas = os.path.join(directorio_actual, 'preguntas_dificiles.txt')
        ruta_respuestas = os.path.join(directorio_actual, 'respuestas_dificiles.txt')

    preguntas = cargar_preguntas_desde_archivo(ruta_preguntas)
    respuestas = cargar_respuestas_desde_archivo(ruta_respuestas)

    marco_menu_dificultad.pack_forget()
    iniciar_juego()

# Función para mostrar el menú de dificultad
def mostrar_menu_dificultad():
    marco_menu_principal.pack_forget()
    marco_menu_dificultad.pack(pady=20)

# Función para salir del juego
def salir_juego():
    pygame.mixer.music.stop()  # Detener la música al salir
    root.quit()

# Función para actualizar la barra de progreso
def actualizar_progreso():
    progreso['value'] = (pregunta_actual + 1) / len(preguntas) * 100

# Configuración de la ventana principal
root = tk.Tk()
root.title("Juego de Preguntas sobre Redes")
root.geometry("800x600")  # Tamaño de la ventana aumentado

# Cargar y establecer la imagen de fondo
imagen_fondo = Image.open(ruta_imagen_fondo)
imagen_fondo = imagen_fondo.resize((800, 600), Image.Resampling.LANCZOS)
foto_fondo = ImageTk.PhotoImage(imagen_fondo)
etiqueta_fondo = tk.Label(root, image=foto_fondo)
etiqueta_fondo.place(relwidth=1, relheight=1)

# Crear un marco para el menú principal
marco_menu_principal = tk.Frame(root, bg='lightgray')

# Botones del menú principal
boton_iniciar = tk.Button(marco_menu_principal, text="Iniciar Juego", command=mostrar_menu_dificultad, font=("Helvetica", 18), bg='lightblue')
boton_iniciar.pack(pady=20)
boton_puntuaciones = tk.Button(marco_menu_principal, text="Puntuaciones", command=mostrar_puntuaciones, font=("Helvetica", 18), bg='lightyellow')
boton_puntuaciones.pack(pady=20)
boton_salir = tk.Button(marco_menu_principal, text="Salir", command=salir_juego, font=("Helvetica", 18), bg='lightcoral')
boton_salir.pack(pady=20)

# Crear un marco para el menú de dificultad
marco_menu_dificultad = tk.Frame(root, bg='lightgray')

# Botones para seleccionar la dificultad
boton_facil = tk.Button(marco_menu_dificultad, text="Fácil", command=lambda: seleccionar_dificultad("facil"), font=("Helvetica", 18), bg='lightgreen')
boton_facil.pack(pady=20)
boton_normal = tk.Button(marco_menu_dificultad, text="Normal", command=lambda: seleccionar_dificultad("normal"), font=("Helvetica", 18), bg='yellow')
boton_normal.pack(pady=20)
boton_dificil = tk.Button(marco_menu_dificultad, text="Difícil", command=lambda: seleccionar_dificultad("dificil"), font=("Helvetica", 18), bg='orange')
boton_dificil.pack(pady=20)

# Crear un marco para las preguntas del cuestionario
marco_cuestionario = tk.Frame(root, bg='white')

# Etiqueta para la pregunta
etiqueta_pregunta = tk.Label(marco_cuestionario, text="", font=("Helvetica", 16), wraplength=700, justify="center", bg='white')
etiqueta_pregunta.pack(pady=20)

# Variable para la opción seleccionada
opcion_seleccionada_var = tk.StringVar()

# Botones de radio para las opciones
botones_radio = []
for i in range(4):
    boton = tk.Radiobutton(marco_cuestionario, text="", variable=opcion_seleccionada_var, font=("Helvetica", 14), wraplength=600, bg='white', anchor='w', padx=20)
    boton.pack(fill='x', pady=5)
    botones_radio.append(boton)

# Botón para enviar la respuesta y pasar a la siguiente pregunta
boton_siguiente = tk.Button(marco_cuestionario, text="Siguiente", command=siguiente_pregunta, font=("Helvetica", 16), bg='lightblue')
boton_siguiente.pack(pady=20)

# Barra de progreso
progreso = ttk.Progressbar(marco_cuestionario, orient="horizontal", length=400, mode="determinate")
progreso.pack(pady=10)

# Mostrar el menú de inicio al iniciar el programa
mostrar_menu_inicio()

# Iniciar el bucle principal de la ventana
root.mainloop()

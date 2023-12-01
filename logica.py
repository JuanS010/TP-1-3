import gamelib
import png
from Pila import Pila

ANCHO = 20 #Pixels de ancho
ALTO = 20 #Pixels de alto
LADO_CASILLA = 20 #Tamaño del pixel

def tamaño_ventana(ancho_pixels, alto_pixels):
    """Define el tamaño que tendra la ventana"""
    alto_ventana = (alto_pixels*LADO_CASILLA) + (LADO_CASILLA*7)
    if ancho_pixels < 20:
        ancho_ventana = 20*LADO_CASILLA
    else:
        ancho_ventana = ancho_pixels*LADO_CASILLA
    return ancho_ventana, alto_ventana

def paint_nuevo(ancho_pixels, alto_pixels):
    '''inicializa el estado del programa con una imagen vacía de ancho x alto pixels'''

    balde = False
    pila_deshacer = Pila()
    pila_rehacer = Pila()
    colores = ['0000FF', 'FF0000', '00FF00', 'FFFF00', 'FF8000', 'FF00FF', 'FFFFFF', '800000','808080']
    paint = []
    for i in range(alto_pixels):
        paint.append([])
        for j in range(ancho_pixels):
            paint[i].append('FFFFFF')
    return paint, colores, pila_deshacer, pila_rehacer, balde

def cargar_ppm(ruta, pila_deshacer, pila_rehacer):
    """Carga un archivo PPM desde la ubicacion que se le pase"""
    
    with open(ruta) as f:
        
        imagen = []
        fila = []
        n_linea = 0
        for i in f:
            n_linea += 1
            if n_linea == 2:
                tamaño = i.strip().split()
                ancho_pixels = int(tamaño[0])
                alto_pixels = int(tamaño[1])
            if n_linea >= 4:
                registro = i.strip().split()
                hexa = ""
                for j in range(len(registro)):
                    color = int(registro[j])
                    hexa += f'{color:02x}'
                    if len(hexa) == 6:
                        fila.append(hexa)
                        hexa = ""
                    if len(fila) == ancho_pixels:
                        imagen.insert(len(imagen)+1,fila.copy())
                        fila = []

    while not pila_deshacer.esta_vacia():
        pila_deshacer.desapilar()

    while not pila_rehacer.esta_vacia():
        pila_rehacer.desapilar()

    return imagen, ancho_pixels, alto_pixels, pila_deshacer, pila_rehacer

def guardar_ppm(paint, ancho_pixels, alto_pixels):
    """Guarda el dibujo actual en un archivo PPM"""

    ruta = gamelib.input("Ingrese la ruta con el nombre del archivo (sin el .PPM)")
    if ruta == None or ruta == "":
        gamelib.say("No se pudo guardar el archivo")
        return
    try:
        imagen = []
        for i in range(len(paint)):
            for j in range(len(paint[i])):
                rojo = f'{paint[i][j][0]}{paint[i][j][1]}'
                verde = f'{paint[i][j][2]}{paint[i][j][3]}'
                azul = f'{paint[i][j][4]}{paint[i][j][5]}'
                color_pixel = (int(rojo, 16), int(verde, 16), int(azul, 16))
                imagen.append(color_pixel)

        with open(f'{ruta}.ppm', 'w') as f:
            f.write('P3\n')
            f.write(f'{ancho_pixels} {alto_pixels}\n')
            f.write('255\n')
            for i in range((ancho_pixels*alto_pixels)):
                    rgb = ""
                    for j in imagen[i]:
                        rgb += f'{j} '
                    rgb += "\n"
                    f.write(rgb)

        gamelib.say("El archivo se guardo correctamente")
    
    except FileNotFoundError:
        gamelib.say("No se pudo guardar el archivo")


def guardar_png(paint):
    """Guarda el dibujo actual en un archivo PNG"""

    ruta = gamelib.input("Ingrese la ruta con el nombre del archivo (sin el .PNG)")
    if ruta == None or ruta == "":
        gamelib.say("No se pudo guardar el archivo")
        return
    try:
        colores_rgb = {}    
        imagen = []
        n_color = 0
        for i in range(len(paint)):
            imagen.append([])
            for j in range(len(paint[i])):
                color_pixel = obtener_color_pixel(paint[i][j])

                if color_pixel in colores_rgb:
                    imagen[i].append(colores_rgb[color_pixel])
                else:
                    colores_rgb[color_pixel] = colores_rgb.get(color_pixel, n_color)
                    imagen[i].append(colores_rgb[color_pixel])
                    n_color += 1

        png.escribir(f'{ruta}.png', colores_rgb, imagen)

        gamelib.say("El archivo se guardo correctamente")

    except FileNotFoundError:
        gamelib.say("No se pudo guardar el archivo")

def obtener_color_pixel(color):
    rojo = f'{color[0]}{color[1]}'
    verde = f'{color[2]}{color[3]}'
    azul = f'{color[4]}{color[5]}'
    color_pixel = (int(rojo, 16), int(verde, 16), int(azul, 16))
    return color_pixel

def deshacer(pila_rehacer, pila_deshacer, paint):
    """ Permite deshacer el ultimo cambio """

    if pila_deshacer.esta_vacia():
        return paint

    anterior = pila_deshacer.desapilar()

    actualizacion_registro = []

    for i in range(len(anterior)):
        y = anterior[i][0]
        x = anterior[i][1]
        ant_color = paint[y][x]
        color = anterior[i][2]
        paint[y][x] = color
        actualizacion_registro.append([y,x,ant_color])

    pila_rehacer.apilar(actualizacion_registro)

    return paint


def rehacer(pila_rehacer, pila_deshacer, paint):
    """ Permite rehacer el ultimo deshacer """
    
    if pila_rehacer.esta_vacia():
        return paint

    anterior = pila_rehacer.desapilar()

    actualizacion_registro = []

    for i in range(len(anterior)):
        y = anterior[i][0]
        x = anterior[i][1]
        ant_color = paint[y][x]
        color = anterior[i][2]
        paint[y][x] = color
        actualizacion_registro.append([y,x,ant_color])

    pila_deshacer.apilar(actualizacion_registro)
    
    return paint

def definir_color(colores):
    """Define un color personalizado"""

    color_elegido = gamelib.input("Ingrese un color hexadecimal completo (sin #):")
    if color_elegido == None or color_elegido == "":
        seleccion = 0
        return colores, seleccion
    if len(color_elegido) != 6:
        seleccion = 0
        gamelib.say("El color no existe")
        return colores, seleccion
    for caracter in color_elegido:
        if caracter not in "0123456789AaBbCcDdEeFf":
            gamelib.say("El color no existe")
            seleccion = 0
            colores[8] = '808080'
            return colores, seleccion
    colores[8] = color_elegido
    seleccion = len(colores)-1          
    return colores, seleccion

def paint_actualizar(x, y, paint, ancho_pixels, alto_pixels, pila_deshacer, pila_rehacer, balde, seleccion, colores):
    """Actualiza la matriz del dibujo con los cambios que se le hicieron"""

    coordenada_a = 0
    coordenada_b = LADO_CASILLA

    for i in range(ancho_pixels):
        if coordenada_a <= x <= coordenada_b:
            x = i
            break
        coordenada_a += LADO_CASILLA
        coordenada_b += LADO_CASILLA   

    coordenada_a = 0
    coordenada_b = LADO_CASILLA

    for i in range(alto_pixels):
        if coordenada_a <= y <= coordenada_b:
            y = i
            break
        coordenada_a += LADO_CASILLA
        coordenada_b += LADO_CASILLA   

    if x > ancho_pixels or y > alto_pixels or x < 0 or y < 0:
        return paint

    actualizaciones = []
    ant_color = paint[y][x]

    if ant_color != colores[seleccion]:
        if balde == True:
                paint_referencia = []
                for i in range(len(paint)):
                    paint_referencia.append([])
                    for j in range(len(paint[i])):
                        paint_referencia[i].append(paint[i][j][:])
                balde_pintar(y, x, paint, ant_color, ancho_pixels, alto_pixels, colores, seleccion)
                for i in range(len(paint)):
                    for j in range(len(paint)):
                        if paint[i][j] != paint_referencia[i][j]:
                            actualizaciones.append([i, j, ant_color])
        else:
            actualizaciones.append([y,x,ant_color])
            paint[y][x] = colores[seleccion]
    else:
        return paint

    pila_deshacer.apilar(actualizaciones)

    while not pila_rehacer.esta_vacia():
        pila_rehacer.desapilar()

    return paint

def balde_pintar(y, x, paint, ant_color, ancho_pixels, alto_pixels, colores, seleccion):
    
    if -1 < y < alto_pixels and -1 < x < ancho_pixels:
        
        if paint[y][x] == ant_color:
            paint[y][x] = colores[seleccion]

            balde_pintar(y-1, x, paint, ant_color, ancho_pixels, alto_pixels, colores, seleccion)
            balde_pintar(y+1, x, paint, ant_color, ancho_pixels, alto_pixels, colores, seleccion)
            balde_pintar(y, x-1, paint, ant_color, ancho_pixels, alto_pixels, colores, seleccion)
            balde_pintar(y, x+1, paint, ant_color, ancho_pixels, alto_pixels, colores, seleccion)

            return
    return


def paint_mostrar(paint, ancho_ventana, alto_ventana, seleccion, colores, ancho_pixels, alto_pixels, balde):
    '''dibuja la interfaz en la ventana'''
    gamelib.draw_begin()
    gamelib.draw_rectangle(0,0, ancho_ventana, alto_ventana, outline='gray', fill='gray')
    
    #Dibuja la cuadricula
    parametro_x = 0
    parametro_y = 0
    for i in range(alto_pixels):
        for j in range(ancho_pixels): 
            gamelib.draw_rectangle(parametro_x, parametro_y, parametro_x+LADO_CASILLA, parametro_y+LADO_CASILLA, outline='black', fill=f"#{paint[i][j]}")
            parametro_x += LADO_CASILLA
        parametro_y += LADO_CASILLA
        parametro_x = 0

    #Dibuja las opciones de colores
    parametro_x = LADO_CASILLA
    parametro_y = LADO_CASILLA*alto_pixels+LADO_CASILLA
    for i in range(len(colores)):
        if seleccion == i:
            gamelib.draw_rectangle(parametro_x, parametro_y, parametro_x+LADO_CASILLA, parametro_y+LADO_CASILLA, outline='white', width=3, fill=f"#{colores[i]}")
        else:    
            gamelib.draw_rectangle(parametro_x, parametro_y, parametro_x+LADO_CASILLA, parametro_y+LADO_CASILLA, outline='gray', fill=f"#{colores[i]}")
        gamelib.draw_text(i+1, parametro_x+LADO_CASILLA/2, parametro_y+LADO_CASILLA/2, fill='black', size=int(LADO_CASILLA/1.5))
        parametro_x += LADO_CASILLA*2

    #Dibuja las opciones de balde, rehacer y deshacer
    opciones = ["Deshacer 'Z'", "Rehacer 'X'", "Balde 'B'"]
    parametro_x = LADO_CASILLA
    parametro_y = LADO_CASILLA*alto_pixels+(LADO_CASILLA*3)
    for i in range(len(opciones)):
        if i == len(opciones)-1 and balde == True:
            gamelib.draw_rectangle(parametro_x, parametro_y, parametro_x+LADO_CASILLA*5, parametro_y+LADO_CASILLA, outline=f"#{colores[seleccion]}", width=3, fill="silver")
        else:
            gamelib.draw_rectangle(parametro_x, parametro_y, parametro_x+LADO_CASILLA*5, parametro_y+LADO_CASILLA, outline='black', fill="silver")
        gamelib.draw_text(opciones[i], parametro_x+LADO_CASILLA*2.5, parametro_y+LADO_CASILLA/2, fill='black', size=int(LADO_CASILLA/2))
        parametro_x += LADO_CASILLA*6

    #Dibuja las opciones de guardado
    opciones = ["Cargar PPM 'C'", "Guardar PPM 'G'", "Guardar PNG 'P'"]
    parametro_x = LADO_CASILLA
    parametro_y = LADO_CASILLA*alto_pixels+(LADO_CASILLA*5)
    for i in range(len(opciones)):
        gamelib.draw_rectangle(parametro_x, parametro_y, parametro_x+LADO_CASILLA*5, parametro_y+LADO_CASILLA, outline='black', fill="silver")
        gamelib.draw_text(opciones[i], parametro_x+LADO_CASILLA*2.5, parametro_y+LADO_CASILLA/2, fill='black', size=int(LADO_CASILLA/2))
        parametro_x += LADO_CASILLA*6

    gamelib.draw_end()


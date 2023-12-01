import logica
import gamelib

def main():
    gamelib.title("AlgoPaint")
    ancho_pixels, alto_pixels = logica.ANCHO, logica.ALTO
    ancho_ventana, alto_ventana = logica.tamaño_ventana(ancho_pixels, alto_pixels)
    seleccion = 0
    gamelib.resize(ancho_ventana, alto_ventana)

    paint, colores, pila_deshacer, pila_rehacer, balde = logica.paint_nuevo(ancho_pixels, alto_pixels)

    while gamelib.is_alive():
        logica.paint_mostrar(paint, ancho_ventana, alto_ventana, seleccion, colores, ancho_pixels, alto_pixels, balde)

        ev = gamelib.wait()
        if not ev:
            break

        if ev.type == gamelib.EventType.ButtonPress and ev.mouse_button == 1:

            if balde == True:
                paint = logica.paint_actualizar(ev.x, ev.y, paint, ancho_pixels, alto_pixels, pila_deshacer, pila_rehacer, balde, seleccion, colores)
            else:
                while True:
                    ev = gamelib.wait()
                    if ev.type == gamelib.EventType.Motion:
                        paint = logica.paint_actualizar(ev.x, ev.y, paint, ancho_pixels, alto_pixels, pila_deshacer, pila_rehacer, balde, seleccion, colores)
                        logica.paint_mostrar(paint, ancho_ventana, alto_ventana, seleccion, colores, ancho_pixels, alto_pixels, balde)
                    elif ev.type == gamelib.EventType.ButtonRelease and ev.mouse_button == 1:
                        paint = logica.paint_actualizar(ev.x, ev.y, paint, ancho_pixels, alto_pixels, pila_deshacer, pila_rehacer, balde, seleccion, colores)
                        break

        if ev.type == gamelib.EventType.KeyPress:
            if '1' <= ev.key <= str(len(colores)):
                seleccion = int(ev.key) -1
                if seleccion == 8:
                    colores, seleccion = logica.definir_color(colores)
            elif ev.key in "Cc":
                ruta = gamelib.input("Ingrese la ruta del archivo PPM")
                try:
                    paint, ancho_pixels, alto_pixels, pila_deshacer, pila_rehacer = logica.cargar_ppm(ruta, pila_deshacer, pila_rehacer)
                    ancho_ventana, alto_ventana = logica.tamaño_ventana(ancho_pixels, alto_pixels)
                    gamelib.resize(ancho_ventana, alto_ventana)
                except FileNotFoundError:
                    gamelib.say("No se encontro el archivo")
            elif ev.key in "Gg":
                logica.guardar_ppm(paint, ancho_pixels, alto_pixels)
            elif ev.key in "Pp":
                logica.guardar_png(paint)
            elif ev.key in "Zz":
                paint = logica.deshacer(pila_rehacer, pila_deshacer, paint)
            elif ev.key in "Xx":
                paint = logica.rehacer(pila_rehacer, pila_deshacer, paint)
            elif ev.key in "Bb":
                if balde:
                    balde = False
                else:
                    balde = True

gamelib.init(main)
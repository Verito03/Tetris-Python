import pygame #IMPORTAMOS DE LA API
import random

pygame.font.init() #PARA INICIAR PYGAME
 
# VARIABLE GLOBALES
pantalla_ancho = 800
pantalla_alto = 700
ancho_juego = 300  #DONDE SE VA HA VER EL JUEGO 
alto_juego = 600  
tamano_bloque = 30

arriba_izquierda_x = (pantalla_ancho - ancho_juego) // 2 #PARA COLOCAR DONDE ESTA LA SIGUIENTE FORMA
arriba_izquierda_y = pantalla_alto - alto_juego
 
 
# FORMA DE LOS BLOQUES EXISTENTES
S = [['.....', '.....', '..00.', '.00..', '.....'], ['.....', '..0..', '..00.', '...0.', '.....']]
Z = [['.....', '.....', '.00..', '..00.', '.....'], ['.....', '..0..', '.00..', '.0...', '.....']]
I = [['..0..', '..0..', '..0..', '..0..', '.....'], ['.....', '0000.', '.....', '.....', '.....']]
O = [['.....', '.....', '.00..', '.00..', '.....']]
J = [['.....', '.0...', '.000.', '.....', '.....'], ['.....', '..00.', '..0..', '..0..', '.....'], ['.....', '.....', '.000.', '...0.', '.....'], ['.....', '..0..', '..0..', '.00..', '.....']]
L = [['.....', '...0.', '.000.', '.....', '.....'], ['.....', '..0..', '..0..', '..00.', '.....'], ['.....', '.....', '.000.', '.0...', '.....'], ['.....', '.00..', '..0..', '..0..', '.....']]
T = [['.....', '..0..', '.000.', '.....', '.....'], ['.....', '..0..', '..00.', '..0..', '.....'], ['.....', '.....', '.000.', '..0..', '.....'], ['.....', '..0..', '.00..', '..0..', '.....']]

 
bloques = [S, Z, I, O, J, L, T]
bloques_color = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

 
 
class Pieza(object):
    filas = 20  # y
    columnas = 10  # x
 
    def __init__(self, columnas, filas, forma):#DECLARAMOS EL OBJETO
        self.x = columnas
        self.y = filas
        self.forma = forma
        self.color = bloques_color[bloques.index(forma)]
        self.rotacion = 0  # DEL 0 AL 3
 
 
def crear_cuadricula(posiciones={}):
    cuadricula = [[(0,0,0) for x in range(10)] for x in range(20)]#CREAMOS EL FONDO DE LA CUADRICULA
 
    for i in range(len(cuadricula)):
        for j in range(len(cuadricula[i])):#DECLARAMOS LA CUADRICULA
            if (j,i) in posiciones:
                c = posiciones[(j,i)]
                cuadricula[i][j] = c
    return cuadricula
 
 
def convertir_bloque_formato(forma):#PARA CUANDO SE POSICIONE EL BLOQUE, SE CONVIERTA
    posicion = []
    formato = forma.forma[forma.rotacion % len(forma.forma)]
 
    for i, linea in enumerate(formato):
        fila = list(linea)
        for j, columna in enumerate(fila):
            if columna == '0':
                posicion.append((forma.x + j, forma.y + i))
 
    for i, pos in enumerate(posicion):
        posicion[i] = (pos[0], pos[1])
 
    return posicion
 
 
def espacio_valido(forma, cuadricula):#PARA QUE NO SE SOBREPONGA ENTRE OTRAS FICHAS 
    espacio_valido = [[(j, i) for j in range(10) if cuadricula[i][j] == (0,0,0)] for i in range(20)] #EL COLOR TIENE QUE SER IGUAL QUE LA CUADRICULA
    espacio_valido = [j for sub in espacio_valido for j in sub]
    cambio_forma = convertir_bloque_formato(forma)
 
    for pos in cambio_forma:
        if pos not in espacio_valido:
            if pos[1] > -1:
                return False
 
    return True
 
 
def check_game_over(posicion):#COMPORBAMOS SI HAY HUECO TODAVIA PARA COLOCAR BLOQUES
    for pos in posicion:
        x, y = pos
        if y < 1:
            return True
    return False
 
 
def get_forma():#IR PONIENDO BLOQUES CON UN RANDOM CON LOS COLORES 
    global bloques, bloques_color
 
    return Pieza(5, 0, random.choice(bloques))
 
 
def texto_medio(texto, tamano, color, superficie):#DECLARAR LOS TEXTOS
    font = pygame.font.SysFont('comicsans', tamano, bold=True)
    label = font.render(texto, 1, color)
 
    superficie.blit(label, (arriba_izquierda_x + ancho_juego/2 - (label.get_width() / 2), arriba_izquierda_y + alto_juego/2 - label.get_height()/2))
 
 
def hacer_cuadricula(superficie, linea, col):#DECLARAR LA CUADRICULA ANTERIOR
    sx = arriba_izquierda_x
    sy = arriba_izquierda_y
    for i in range(linea):
        pygame.draw.line(superficie, (128,128,128), (sx, sy+ i*30), (sx + ancho_juego, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(superficie, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + alto_juego))  # vertical lines
 
 
def eliminar_lineas(cuadricula, bloqueo):
    # need to see if linea is clear the shift every other linea above down one
 
    inc = 0
    for i in range(len(cuadricula)-1,-1,-1):
        linea = cuadricula[i]
        if (0, 0, 0) not in linea:
            inc += 1
            # add posicion to remove from bloqueo
            ind = i
            for j in range(len(linea)):
                try:
                    del bloqueo[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(bloqueo), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                bloqueo[newKey] = bloqueo.pop(key)
 
 
def dibujar_siguiente_bloque(forma, superficie):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Siguiente:', 1, (255,255,255))
 
    sx = arriba_izquierda_x + ancho_juego + 50
    sy = arriba_izquierda_y + alto_juego/2 - 100
    formato = forma.forma[forma.rotacion % len(forma.forma)]
 
    for i, linea in enumerate(formato):
        fila = list(linea)
        for j, column in enumerate(linea):
            if column == '0':
                pygame.draw.rect(superficie, forma.color, (sx + j*30, sy + i*30, 30, 30), 0)
 
    superficie.blit(label, (sx + 10, sy- 30))
 
 
def ventana(superficie):
    superficie.fill((0,0,0))
    # Tetris Title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('JUEGO TETRIS', 1, (255,255,255))
 
    superficie.blit(label, (arriba_izquierda_x + ancho_juego / 2 - (label.get_width() / 2), 30))
 
    for i in range(len(cuadricula)):
        for j in range(len(cuadricula[i])):
            pygame.draw.rect(superficie, cuadricula[i][j], (arriba_izquierda_x + j* 30, arriba_izquierda_y + i * 30, 30, 30), 0)
 
    # draw cuadricula and bordehacer(superficie, 20, 10)
    pygame.draw.rect(superficie, (255, 0, 0), (arriba_izquierda_x, arriba_izquierda_y, ancho_juego, alto_juego), 5)
    # pygame.display.update()
 
 
def main():
    global cuadricula
 
    bloqueo_posicion = {}  # (x,y):(255,0,0)
    cuadricula = crear_cuadricula(bloqueo_posicion)
 
    cambiar_pieza = False
    run = True
    pieza_actual = get_forma()
    siguiente_pieza = get_forma()
    clock = pygame.time.Clock()
    tiempo_caida = 0
 
    while run:
        tiempo_caido = 0.27
 
        cuadricula = crear_cuadricula(bloqueo_posicion)
        tiempo_caida += clock.get_rawtime()
        clock.tick()
 
        # pieza FALLING CODE
        if tiempo_caida/1000 >= tiempo_caido:
            tiempo_caida = 0
            pieza_actual.y += 1
            if not (espacio_valido(pieza_actual, cuadricula)) and pieza_actual.y > 0:
                pieza_actual.y -= 1
                cambiar_pieza = True
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pieza_actual.x -= 1
                    if not espacio_valido(pieza_actual, cuadricula):
                        pieza_actual.x += 1
 
                elif event.key == pygame.K_RIGHT:
                    pieza_actual.x += 1
                    if not espacio_valido(pieza_actual, cuadricula):
                        pieza_actual.x -= 1
                elif event.key == pygame.K_UP:
                    # rotate forma
                    pieza_actual.rotacion = pieza_actual.rotacion + 1 % len(pieza_actual.forma)
                    if not espacio_valido(pieza_actual, cuadricula):
                        pieza_actual.rotacion = pieza_actual.rotacion - 1 % len(pieza_actual.forma)
 
                if event.key == pygame.K_DOWN:
                    # move forma down
                    pieza_actual.y += 1
                    if not espacio_valido(pieza_actual, cuadricula):
                        pieza_actual.y -= 1
 
                if event.key == pygame.K_SPACE:
                   while espacio_valido(pieza_actual, cuadricula):
                       pieza_actual.y += 1
                   pieza_actual.y -= 1
                   print(convertir_bloque_formato(pieza_actual))  # todo fix
 
        forma_pos = convertir_bloque_formato(pieza_actual)
 
        # add pieza to the cuadricula for drawing
        for i in range(len(forma_pos)):
            x, y = forma_pos[i]
            if y > -1:
                cuadricula[y][x] = pieza_actual.color
 
        # IF pieza HIT GROUND
        if cambiar_pieza:
            for pos in forma_pos:
                p = (pos[0], pos[1])
                bloqueo_posicion[p] = pieza_actual.color
            pieza_actual = siguiente_pieza
            siguiente_pieza = get_forma()
            cambiar_pieza = False
 
            # call four times to check for multiple clear filas
            eliminar_lineas(cuadricula, bloqueo_posicion)
 
        ventana(win)
        dibujar_siguiente_bloque(siguiente_pieza, win)
        pygame.display.update()
 
        # Check if user lost
        if check_game_over(bloqueo_posicion):
            run = False
 
    texto_medio("Perdiste", 40, (255,255,255), win)
    pygame.display.update()
    pygame.time.delay(2000)
 
 
def main_menu():
    run = True
    while run:
        win.fill((0,0,0))
        texto_medio('Presiona cualquier letra.', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
 
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()
 
 
win = pygame.display.set_mode((pantalla_ancho, pantalla_alto))
pygame.display.set_caption('Tetris') 
main_menu()
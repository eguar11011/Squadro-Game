class Ficha:
    def __init__(self, color_jugador, row, column):
        self.color_jugador:str = color_jugador
        self.row:int = row
        self.column:int = column
        self.movimiento_tipo = self.tipo_movimiento_inicial()

    def tipo_movimiento_inicial(self):
        '''
                   1 3
            ↓	|x|r|r|x| ↓
            → 3	|a| | |	| ← 1
            → 1	|a| | |	| ← 3
                |x| | |x| 
            ↑      3 1    ↑

        Posicion inical amarillo
        [a, movimiento_1]: (2,0)
        [a, movimiento_3]: (1,0)

        Posicion inicial rojo
        [r, movimiento_1]: (0,1)
        [r, movimiento_3]: (0,2)
        '''
        
        
        # amarillo
        if (self.row, self.column) == (2,0):  
            return 1  # Movimiento de 1 casilla 
        elif (self.row, self.column) == (1,0):  
            return 3  # Movimiento de 3 casillas
        # rojo
        if (self.row, self.column) == (0,1):  
            return 1  
        elif (self.row, self.column) == (0,2): 
            return 3  
    

    def cambiar_direccion(self):
        '''
                   1 3
            ↓	|x|r|r|x| ↓
            → 3	|a| | |	| ← 1
            → 1	|a| | |	| ← 3
                |x| | |x| 
            ↑      3 1    ↑

        Posicion para cambio amarillo
        [a,movimiento_1 -> movimineto_3]: (2,3)
        [a,movimiento_3 -> movimineto_1]: (1,3)

        Posicion para cambio rojo
        [r, movimiento_1 -> movimineto_3]: (3,1)
        [r, movimiento_3 -> movimineto_1]: (3,2)
        '''
        
        # Definir una posición especial en el tablero donde cambia el movimiento

        # Cambio para amarillo
        if (self.row, self.column) == (2, 3):  # Posición especial
            self.movimiento_tipo = -3  # Cambia a movimiento de 3 casillas
        elif (self.row, self.column) == (1, 3):  # Otra posición especial
            self.movimiento_tipo = -1  # Cambia a movimiento de 1 casilla

        # Cambio para rojo
        if (self.row, self.column) == (3, 1):  # Posición especial
            self.movimiento_tipo = -3  # Cambia a movimiento de 3 casillas
        elif (self.row, self.column) == (3, 2):  # Otra posición especial
            self.movimiento_tipo = -1  # Cambia a movimiento de 1 casilla

    def mover(self):
        # Movimiento en horizontal: amarillo
        if abs(self.movimiento_tipo) == 1 and self.color_jugador == "amarillo":
            self.row += self.movimiento_tipo
        
        elif abs(self.movimiento_tipo) == 3 and self.color_jugador == "amarillo":
            self.row += self.movimiento_tipo

        # Movimineto en vertical: rojo
        if abs(self.movimiento_tipo) == 1 and self.color_jugador == "rojo":
            self.column += self.movimiento_tipo
        
        elif abs(self.movimiento_tipo) == 3 and self.color_jugador == "rojo":
            self.column += self.movimiento_tipo  
        

        self.cambiar_direccion()

class Juego:
    def __init__(self):
        '''
        Board:
        [['X', '-', '-', 'X'],
         ['-', '-', '-', '-'],
         ['-', '-', '-', '-'],
         ['X', '- , '-', 'X']]
        '''
        self.tablero = [[None for _ in range(4)] for _ in range(4)]
        self.jugadores = [[], []]
        self.turno = 0  # Comienza el jugador 0
        
        # Inicializar fichas de los jugadores
        self.jugadores[0] = [Ficha(0, 0, 1), Ficha(0, 0, 2)] # (x,y)
        self.jugadores[1] = [Ficha(1, 1, 3), Ficha(1, 2, 2)]
        self.actualizar_tablero()

    def actualizar_tablero(self):
        self.tablero = [[None for _ in range(4)] for _ in range(4)]
        for jugador in self.jugadores:
            for ficha in jugador:
                self.tablero[ficha.row][ficha.column] = ficha.jugador

    def mostrar_tablero(self):
        for fila in self.tablero:
            print(" | ".join([str(celda) if celda is not None else " " for celda in fila]))
            print("-" * 13)

    def mover_ficha(self, jugador, ficha_index, dx, dy):
        ficha = self.jugadores[jugador][ficha_index]
        ficha.mover(dx, dy)
        self.actualizar_tablero()

        # Verificar condiciones de victoria
        if self.verificar_victoria(jugador):
            print(f"¡Jugador {jugador} ha ganado!")
            return True
        return False

    def verificar_victoria(self, jugador):
        if jugador == 0:
            return all(f.row == 3 and f.column == 3 for f in self.jugadores[0]) or \
                   all(f.row == 0 and f.column == 0 for f in self.jugadores[0])
        elif jugador == 1:
            return all(f.row == 0 and f.column == 0 for f in self.jugadores[1]) or \
                   all(f.row == 3 and f.column == 3 for f in self.jugadores[1])

    def jugar(self):
        while True:
            self.mostrar_tablero()
            jugador = self.turno
            ficha_index = int(input(f"Jugador {jugador}, selecciona la ficha a mover (0 o 1): "))
            dx = int(input("Ingrese el cambio en x (1, -1 o 0): "))
            dy = int(input("Ingrese el cambio en y (1, -1 o 0): "))
            
            if self.mover_ficha(jugador, ficha_index, dx, dy):
                break
            
            self.turno = 1 - self.turno  # Cambia de turno

# Iniciar el juego
juego = Juego()
juego.jugar()

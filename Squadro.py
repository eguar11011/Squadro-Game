from __future__ import annotations
from typing import List, Tuple

# Representa una pieza en el juego
class Piece:
    def __init__(self, player: int, position: Tuple[int, int], forward_steps: int, backward_steps: int):
        self.player = player  # 0 o 1 para indicar el jugador
        self.position = position  # Posición actual de la pieza en el tablero (fila, columna)
        self.forward_steps = forward_steps  # Número de casillas que avanza en la ida
        self.backward_steps = backward_steps  # Número de casillas que avanza en la vuelta

        self.direction = False  # Indica si la direccion de la pieza 
        self.movement_info = {} # Información de los movimientos realizados
        self.out_piece = 0 # Si llega a 3 es porque esta afuera
 
    def move(self, board: Board):
        
        for _ in range (self.forward_steps): # Movemos de un solo salto para poder verificar que la casilla este vacia
            self.check_turn(board)
            self._move(board)
            if not self.direction and self.position in board.check_point_backward: break
            elif self.direction and self.position in board.check_point_forward: break
        self.restore_piece(board)

    def _move(self, board: Board):
        row, col = self.position
        advance_or_regres = 1 if not self.direction else -1 # Avanza o retrocede 

        if self.player == 0:  # Movimiento horizontal
            for i in range(1, 10):
                self.movement_info.add(row, col)
                col = col + i*advance_or_regres
                if board.grid[row][col] is None:
                    self.position = (row, col)

                    break

        elif self.player == 1:  # Movimiento vertical
            for i in range(1, 10):
                self.movement_info.add(row, col)
                row = row + i*advance_or_regres
                if board.grid[row][col] is None:
                    self.position = (row, col)
                    break
    
    def check_turn(self, board):
        # Verificar si tiene que cambiar de direccion.
        if not self.direction:
            if self.position in board.check_point_backward:
                self.turn(board)
    def turn(self, board):
        # Gira la pieza cuando llega al final del carril
        self.out_piece += 1
        self.direction = True

    def restore_piece(self, board: Board):
        row, col = self.position
        if self.player == 0:
            for piece in board.pieces_p2:
                check_point = 0 if not piece.direction else 7
                if piece.position in self.movement_info:
                    piece.position = (row,check_point)
                    
        if self.player == 1:
            for piece in board.pieces_p1:
                check_point = 0 if not piece.direction else 7
                if piece.position in self.movement_info:
                    piece.position = (check_point,col)

    def check_out_piece(self,board):
        if self.out_piece == 3:
            if self.player == 0:
                board.out_pieces_p1 +=1
            elif self.player == 1:
                 board.out_pieces_p2 +=1




                
# Representa el tablero del juego
class Board:
    def __init__(self):
        _steps_p1 = [3, 1 ,2, 1, 3]
        _steps_p2 = [1, 3 ,2, 3, 1]
        
        self.out_pieces_p1 = 0
        self.out_pieces_p2 = 0
        # Inicia un tablero vacío de 7x7
        self.grid = [[None for _ in range(7)] for _ in range(7)]
        # Configura las piezas de cada jugador
        self.pieces_p1 = [Piece(0, (i + 1, 0), _steps_p1  , _steps_p2) for i in range(5)]
        self.pieces_p2 = [Piece(1, (0, i + 1), _steps_p2 , _steps_p1) for i in range(5)]
        # Posiciones clave en el tablero
        self.check_point_forward = {(i, 0) for i in range(1, 7)} | {(0, j) for j in range(1, 7)}
        self.check_point_backward = {(i, 7) for i in range(1, 7)} | {(7, j) for j in range(1, 7)}

        
        # Coloca las piezas en la posición inicial
        for i, piece in enumerate(self.pieces_p1):
            self.grid[i + 1][0] = piece  # (row, column)
        for i, piece in enumerate(self.pieces_p2):
            self.grid[0][i + 1] = piece

    def is_win(self, player: int) -> bool:
        if self.out_pieces_p1 == 4 or self.out_pieces_p2 == 4: return True
        else: return False

    def display(self):
        # Muestra el estado actual del tablero
        for row in self.grid:
            print(" | ".join(['X' if piece is not None else '.' for piece in row]))
            print('-' * 29)

# Representa el juego en sí
class SquadroGame:
    def __init__(self):
        self.board = Board()
        self.current_player = 0  # Comienza el jugador 1

    def play_turn(self):
        # Lógica para que el jugador actual haga un movimiento
        pass

    def start(self):
        while True:
            self.board.display()
            self.play_turn()
            if self.board.is_win(self.current_player):
                print(f"Jugador {self.current_player + 1} ha ganado!")
                break
            # Cambiar de jugador
            self.current_player = 1 - self.current_player

# Inicia el juego
if __name__ == "__main__":
    game = SquadroGame()
    game.start()

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
        self.movement_info = set() # Información de los movimientos realizados
        self.out_piece = 0 # Si llega a 3 es porque esta afuera
        self.killed = False
 
    def move(self, board: Board):

        if is_out:=self.is_out():  

            if not self.direction:
                for _ in range(self.forward_steps): # Movemos de un solo salto para poder verificar que la casilla este vacia
                    self._move(board)
                    self.check_turn(board)
                    if self.check_kill(): break
                    if not self.direction and self.position in board.check_point_backward: break # Stop si acaba de llegar a un checkpoint
                    elif self.direction and self.position in board.check_point_forward: break
            else:
                for _ in range(self.backward_steps): # Movemos de un solo salto para poder verificar que la casilla este vacia
                    self._move(board)
                    self.check_turn(board)
                    if self.check_kill(): break
                    if not self.direction and self.position in board.check_point_backward: break # Stop si acaba de llegar a un checkpoint
                    elif self.direction and self.position in board.check_point_forward: break
                
            self.restore_piece(board)

            return is_out
        else: return is_out

    def _move(self, board: Board):
        row, col = self.position
        advance_or_regres = 1 if not self.direction else -1 # Avanza o retrocede 

        if self.player == 0:  # Movimiento horizontal
            for i in range(1, 10): # Solo es un rango
                self.movement_info.add((row, col))
                col = col + 1*advance_or_regres
                if i>1: self.killed = True
                if board.grid[row][col] is None:
                    self.position = (row, col)

                    break

        elif self.player == 1:  # Movimiento vertical
            for i in range(1, 10):
                self.movement_info.add((row, col))
                row = row + 1*advance_or_regres
                if i>1: self.killed = True
                if board.grid[row][col] is None:
                    self.position = (row, col)
                    break
    
    def check_turn(self, board):
        # Verificar si tiene que cambiar de direccion.
        if not self.direction:
            if self.position in board.check_point_backward: # Verificar si llego a un checkpoint
                self.direction_change(board)  
        else:
            if self.position in board.check_point_forward:
                self.direction_change(board)

    def check_kill(self):
        if self.killed:  self.killed = False; return True
        else: False
    def direction_change(self, board):
        # Gira la pieza cuando llega al final del carril
        self.out_piece += 1
        self.direction = True

        if self.out_piece == 2:
            if self.player == 0:
                board.out_pieces_p1 +=1
            elif self.player == 1:
                 board.out_pieces_p2 +=1


    def restore_piece(self, board: Board):
        #row, col = self.position
        if self.player == 0:
            for piece in board.pieces_p2:
                row, col = piece.position
                check_point = 0 if not piece.direction else 7
                if piece.position in self.movement_info:
                    piece.position = (check_point,col)
                    
        if self.player == 1:
            for piece in board.pieces_p1:
                row, col = piece.position
                check_point = 0 if not piece.direction else 7
                if piece.position in self.movement_info:
                    piece.position = (row,check_point)

        self.movement_info = set()

    def is_out(self) -> bool:
        """Comprueba si la pieza está fuera del tablero."""
        if self.out_piece >= 2:
            self.is_active = False  # Marca la pieza como inactiva si está fuera
            print(f"Pieza del Jugador {self.player + 1} ha salido del tablero.")
            return False
        return True




                
# Representa el tablero del juego
class Board:
    def __init__(self):
        steps_p1 = [3, 1 ,2, 1, 3]
        steps_p2 = [1, 3 ,2, 3, 1]
        
        self.out_pieces_p1 = 0
        self.out_pieces_p2 = 0
        # Inicia un tablero vacío de 7x7
        self.grid = [[None for _ in range(7)] for _ in range(7)]
        # Configura las piezas de cada jugador
        self.pieces_p1 = [Piece(0, (i + 1, 0), steps_p1[i]  , steps_p2[i]) for i in range(5)]
        self.pieces_p2 = [Piece(1, (0, i + 1), steps_p2[i] , steps_p1[i]) for i in range(5)]
        # Posiciones clave en el tablero
        self.check_point_forward = {(i, 0) for i in range(1, 7)} | {(0, j) for j in range(1, 7)}
        self.check_point_backward = {(i, 6) for i in range(1, 7)} | {(6, j) for j in range(1, 7)}
        # Coloca las piezas iniciales en la cuadrícula
        self.update_grid()  

    def is_win(self, player: int) -> bool:
        if self.out_pieces_p1 == 4 or self.out_pieces_p2 == 4: return True
        else: return False

    def update_grid(self):
        """Reinicia y actualiza el tablero con las posiciones actuales de las piezas."""
        # Reiniciar la cuadrícula vacía
        self.grid = [[None for _ in range(7)] for _ in range(7)]
        
        # Colocar las piezas del jugador 1 en la cuadrícula
        for piece in self.pieces_p1:
            row, col = piece.position
            self.grid[row][col] = piece
        
        # Colocar las piezas del jugador 2 en la cuadrícula
        for piece in self.pieces_p2:
            row, col = piece.position
            self.grid[row][col] = piece

    def display(self):
        # Movimientos del tablero por jugador
        steps_p1 = [3, 1, 2, 1, 3]  
        steps_p2 = [1, 3, 2, 3, 1]  

        # Parte superior - Movimientos forwards jugador dos
        print("\t" + "   ".join(map(str, steps_p2)))

        # Piezas de la parte superior
        print("x | " + " | ".join(['↓' if piece is not None and piece.player == 1 and not piece.direction else '↑' if piece is not None and piece.player == 1 and piece.direction else '.' for piece in self.grid[0]]) + " | x")
        print("-" * 29)

        # Piezas de cada fila
        for i in range(1, 6):
            row = f"{steps_p1[i - 1]} | "  # Parte lateral izquierdo - Movimientos Forward jugador uno
            # Agregar pieza en su posicion actual o colocar un punto '.'
            row += " | ".join([('→' if piece is not None and piece.player == 0 and not piece.direction else
                                '←' if piece is not None and piece.player == 0 and piece.direction else
                                '↓' if piece is not None and piece.player == 1 and not piece.direction else
                                '↑' if piece is not None and piece.player == 1 and piece.direction else '.') 
                            for piece in self.grid[i]])
            row += f" | {steps_p1[i - 1]}"  # Parte lateral derecho - Movimientos Backward jugador uno
            print(row)
            print("-" * 29)

        # Imprimir la fila inferior del tablero
        print("x | " + " | ".join(['.' for _ in range(7)]) + " | x")

        # Fila inferior - Movimientos Backward jugador dos
        print("\t" + "   ".join(map(str, steps_p1)))



# Representa el juego en sí
class SquadroGame:
    def __init__(self):
        self.board = Board()
        self.current_player = 0  # Comienza el jugador 1

    def play_turn(self):
        # Obtener las piezas del jugador actual
        current_pieces = self.board.pieces_p1 if self.current_player == 0 else self.board.pieces_p2

        
        print(f"\n\tTurno del Jugador {self.current_player + 1}\n")
        self.board.display()
        # Solicitar al jugador que seleccione una pieza (en este caso, elegimos automáticamente para simplificar)
        selected_piece = None
        while True:
            piece_idx = int(input(f"Selecciona una pieza para mover (1-{len(current_pieces)}): ")) - 1
            if 0 <= piece_idx < len(current_pieces):
                selected_piece = current_pieces[piece_idx]
            if selected_piece.move(self.board) and (selected_piece is not None): break
        self.board.update_grid()

    def start(self):
        while True:
            # self.board.display()
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

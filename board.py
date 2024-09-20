from __future__ import annotations
from typing import List, Tuple
from piece import Piece

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


class BoardRenderer:
    @staticmethod
    def display(board: Board):
        steps_p1 = [3, 1, 2, 1, 3]  
        steps_p2 = [1, 3, 2, 3, 1]  

        # Parte superior - Movimientos forwards jugador dos
        print("\t" + "   ".join(map(str, steps_p2)))

        # Piezas de la parte superior
        print("x | " + " | ".join(['↓' if piece is not None and piece.player == 1 and not piece.direction else '↑' if piece is not None and piece.player == 1 and piece.direction else '.' for piece in board.grid[0]]) + " | x")
        print("-" * 29)

        # Piezas de cada fila
        for i in range(1, 6):
            row = f"{steps_p1[i - 1]} | "  # Parte lateral izquierdo - Movimientos Forward jugador uno
            row += " | ".join([('→' if piece is not None and piece.player == 0 and not piece.direction else
                                '←' if piece is not None and piece.player == 0 and piece.direction else
                                '↓' if piece is not None and piece.player == 1 and not piece.direction else
                                '↑' if piece is not None and piece.player == 1 and piece.direction else '.') 
                            for piece in board.grid[i]])
            row += f" | {steps_p2[i - 1]}"  # Parte lateral derecho - Movimientos Backward jugador uno
            print(row)
            print("-" * 29)

        # Imprimir la fila inferior del tablero
        print("x | " + " | ".join(['↓' if piece is not None and piece.player == 1 and not piece.direction else '↑' if piece is not None and piece.player == 1 and piece.direction else '.' for piece in board.grid[6]]) + " | x")
        print("\t" + "   ".join(map(str, steps_p1)))

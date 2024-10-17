from __future__ import annotations
from piece import Piece

class Board:
    
    BOARD_SIZE = 7
    WINNING_PIECES = 4
    STEPS_P1 = [3, 1, 2, 1, 3]
    STEPS_P2 = [1, 3, 2, 3, 1]

    def __init__(self):
        """
        Initializes the game board and sets up the pieces for both players.

        Attributes:
            out_pieces_p1 (int): Counter for Player 1's pieces that have been removed from the board.
            out_pieces_p2 (int): Counter for Player 2's pieces that have been removed from the board.
            grid (List[List[Optional[Piece]]]): A 7x7 game board initialized with None, representing empty spaces.
            pieces_p1 (List[Piece]): A list of Player 1's pieces, each placed in its starting position with corresponding movement steps.
            pieces_p2 (List[Piece]): A list of Player 2's pieces, each placed in its starting position with corresponding movement steps.
            check_point_forward (Set[Tuple[int, int]]): Set of board positions representing checkpoints for forward movement.
            check_point_backward (Set[Tuple[int, int]]): Set of board positions representing checkpoints for backward movement.

        The method sets up an empty 7x7 board, initializes the pieces for both players, and defines key checkpoints for forward and backward movement. 
        It then calls `update_grid` to place the pieces on the board.
        """
        self.out_pieces_p1 = 0
        self.out_pieces_p2 = 0
        self.grid = [[None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.pieces_p1 = [Piece(0, (i + 1, 0), self.STEPS_P1[i], self.STEPS_P2[i]) for i in range(5)]
        self.pieces_p2 = [Piece(1, (0, i + 1), self.STEPS_P2[i], self.STEPS_P1[i]) for i in range(5)]
        self.check_point_forward = {(i, 0) for i in range(1, 7)} | {(0, j) for j in range(1, 7)}
        self.check_point_backward = {(i, 6) for i in range(1, 7)} | {(6, j) for j in range(1, 7)}
        self.update_grid()  
        
    @property
    def is_win(self) -> bool:
        return self.out_pieces_p1 == 4 or self.out_pieces_p2 == 4

    
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
        print("x | " + " | ".join([get_colored_piece(piece) for piece in board.grid[0]]) + " | x")
        print("-" * 29)

        # Piezas de cada fila
        for i in range(1, 6):
            row = f"{steps_p1[i - 1]} | "  # Parte lateral izquierdo - Movimientos Forward jugador uno
            row += " | ".join([get_colored_piece(piece) for piece in board.grid[i]])
            row += f" | {steps_p2[i - 1]}"  # Parte lateral derecho - Movimientos Backward jugador uno
            print(row)
            print("-" * 29)

        # Imprimir la fila inferior del tablero
        print("x | " + " | ".join([get_colored_piece(piece) for piece in board.grid[6]]) + " | x")
        print("\t" + "   ".join(map(str, steps_p1)))


def get_colored_piece(piece):
    """
    Returns a string representing the player's piece with appropriate color and direction.
    
    Player 1's pieces (code 033) are displayed in yellow, and Player 2's pieces (code 031) are displayed in red.
    
    - Player 1: 
        - Upward direction is shown as '↑' (yellow).
        - Downward direction is shown as '↓' (yellow).
    
    - Player 0 (Player 2): 
        - Left direction is shown as '←' (red).
        - Right direction is shown as '→' (red).
    
    If there is no piece, a '.' is returned.
    
    Args:
        piece (Piece): The piece object to be represented.

    Returns:
        str: A string with the colored symbol for the piece.
    
    """
    if piece is None:
        return '.'

    colors = {1: '\033[33m', 0: '\033[31m'}
    directions = {
        (1, True): '↑', (1, False): '↓',
        (0, True): '←', (0, False): '→'
    }
    
    return f"{colors[piece.player]}{directions[(piece.player, piece.direction)]}\033[0m"

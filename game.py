from board import Board, BoardRenderer
from piece import Piece


# Representa el juego en sí
class SquadroGame:
    def __init__(self):
        self.board = Board()
        self.current_player = 0  # Comienza el jugador 1

    def play_turn(self):
        # Obtener las piezas del jugador actual
        current_pieces = self.board.pieces_p1 if self.current_player == 0 else self.board.pieces_p2

        
        print(f"\n\tTurno del Jugador {self.current_player + 1}\n")
        BoardRenderer.display(self.board)
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
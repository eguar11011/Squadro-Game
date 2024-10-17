from board import Board, BoardRenderer
from piece import Piece
import time
import sys

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
            try:
                # Solicitar entrada y convertir a entero
                piece_idx = int(input(f"Selecciona una pieza para mover (1-{len(current_pieces)}): ")) - 1
                
                # Verificar que el índice esté dentro del rango permitido
                if 0 <= piece_idx < len(current_pieces):
                    selected_piece = current_pieces[piece_idx]
                else:
                    print(f"Error: Elige un número entre 1 y {len(current_pieces)}.")
                    continue
                
                # Verificar que selected_piece no sea None y que el movimiento sea válido
                if selected_piece is not None and selected_piece.move(self.board):
                    break  # Si el movimiento es válido, salir del bucle
                else:
                    print("Error: No se puede mover la pieza seleccionada. Intenta otra vez.")
            
            except ValueError:
                # Manejar el caso donde la entrada no es un número válido
                print("Error: Ingresa un número válido.")

    
        self.board.update_grid()

    def start(self):
        
        self.tutorial_general_information
        input("Are you ready?")
        while True:
            self.play_turn()
            if self.board.is_win:
                print(f"Jugador {self.current_player + 1} ha ganado!")
                break
            # Cambiar de jugador
            self.current_player = 1 - self.current_player

    @property
    def tutorial_general_information(self):
        """
        Prints a general overview of the game mechanics in Squadro in an aesthetically pleasing format.
        """
        self.loading_bar

        instructions = """
        ╔══════════════════════════════════════════════════════════════════════════════════╗
        ║                      🎲 General Instructions for Squadro 🎲                      ║
        ╠══════════════════════════════════════════════════════════════════════════════════╣
        ║                                                                                  ║
        ║ In Squadro, each player has 5 pieces, and the goal is to get all your pieces to  ║
        ║ the opposite side and back.                                                      ║
        ║                                                                                  ║
        ║ Player 1 (starting on the left side of the board):                               ║
        ║ - Moves pieces to the right (→) along their row.                                 ║
        ║ - Once a piece reaches the far right corner, it reverses direction and moves to  ║
        ║   the left (←) to return home.                                                   ║
        ║                                                                                  ║
        ║ Player 2 (starting on the top side of the board):                                ║
        ║ - Moves pieces downward (↓) along their column.                                  ║
        ║ - Once a piece reaches the bottom corner, it reverses direction and moves upward ║
        ║   (↑) to return to its starting position.                                        ║
        ║                                                                                  ║
        ║ The game alternates turns between Player 1 and Player 2. On each turn, a player  ║
        ║ selects one of their pieces to move.                                             ║
        ║                                                                                  ║
        ║                          📦 Piece Selection 📦                                   ║
        ║ - Players select a piece by choosing a number between [1-5],                     ║
        ║   corresponding to the piece’s position.                                         ║
        ║ - The selected piece moves based on its current direction                        ║
        ║   (either towards the goal or back to the starting side).                        ║
        ║                                                                                  ║
        ║                         🛠 Movement Rules 🛠                                       ║
        ║ - Each piece has a predefined movement speed, representing how many spaces it    ║
        ║   moves in a turn.                                                               ║
        ║ - When a piece reaches its goal (far side of the board),                         ║
        ║   its movement speed changes as it reverses direction.                           ║
        ║                                                                                  ║
        ║ The first player to get all of their pieces to the opposite side                 ║
        ║ and back to the starting position wins.                                          ║
        ║                                                                                  ║
        ║ For detailed examples of how moves work, refer to the `tutorial_sampler_moves`   ║
        ║ section.                                                                         ║
        ║                                                                                  ║
        ╚══════════════════════════════════════════════════════════════════════════════════╝
        """
        print(instructions)
    
    @property
    def loading_bar(self, total = 100):
        """
        Displays a loading bar that fills up to 100%.
        """
        print("\nLoading game...")
        for i in range(total + 1):
            # Calculate percentage
            percent = (i / total) * 100
            # Create the loading bar
            bar_length = 50  # Length of the loading bar
            filled_length = int(bar_length * i // total)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            # Print the loading bar
            sys.stdout.write(f'\r|{bar}| {percent:.2f}%')
            sys.stdout.flush()
            time.sleep(0.04)  # Simulate loading time (adjust as needed)

        print()  # Move to the next line after loading completes

    @property
    def tutorial_sampler_moves(self):
        ...
# Inicia el juego
if __name__ == "__main__":
    game = SquadroGame()
    game.start()
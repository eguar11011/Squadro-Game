from __future__ import annotations
from typing import NewType, List, TypeVar, Generic
from abc import ABC, abstractmethod

# Definición de un nuevo tipo para representar un movimiento en el juego
Move = NewType('Move', int)

# Clase base abstracta para una pieza del juego
class Piece(ABC):
    
    @property
    @abstractmethod
    def direction(self) -> bool:
        """
        Devuelve la dirección de la pieza.
        La dirección determina si la pieza avanza o retrocede.
        """
        pass

    @abstractmethod    
    def number_of_jumps(self) -> int:
        """
        Devuelve la cantidad de saltos que la pieza puede realizar.
        La cantidad de saltos puede depender de factores como el tipo de pieza o su ID.
        """
        pass

# Clase base abstracta para representar el tablero de juego
class Board(ABC):
    
    @property
    @abstractmethod
    def turn(self) -> Piece:
        """
        Devuelve la pieza que tiene el turno actual.
        """
        pass

    @abstractmethod
    def move(self, location: Move) -> Board:
        """
        Realiza un movimiento en la ubicación especificada y actualiza el estado del tablero.
        
        :param location: Un objeto de tipo Move que indica la ubicación del movimiento.
        :return: Un nuevo estado del tablero después del movimiento.
        """
        pass

    @property
    @abstractmethod
    def pieces_out(self) -> List[Piece]:
        """
        Devuelve una lista de piezas que han sido eliminadas o están fuera del tablero.
        
        :return: Lista de objetos de tipo Piece.
        """
        pass

    @property
    @abstractmethod
    def is_win(self) -> bool:
        """
        Verifica si el estado actual del tablero representa una victoria.
        
        :return: True si hay una victoria, False en caso contrario.
        """
        pass

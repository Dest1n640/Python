from abc import ABC, abstractmethod

class ChessPiece(ABC):
    def __init__(self, vertical, horizontal):
        if horizontal not in "abcdefgh" or not (1 <= vertical <= 8):
            raise ValueError("Invalid coordinates.")
        self.horizontal = horizontal
        self.vertical = vertical

    @abstractmethod
    def can_move(self, target_vertical, target_horizontal):
        pass

    @abstractmethod
    def __str__(self):
        pass

class King(ChessPiece):
    def __init__(self, vertical, horizontal):
        ChessPiece.__init__(self, vertical, horizontal)

    def can_move(self, king_vertical, king_horizontal):
        if king_horizontal not in "abcdefgh" or not (1 <= king_vertical <= 8):
            return False
        horizontal_list = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
        current_x = horizontal_list[self.horizontal]
        target_x = horizontal_list[king_horizontal]
        if abs(current_x - target_x) <= 1 and abs(self.vertical - king_vertical) <= 1:
            return True
        return False

    def __str__(self):
        return f"King - {self.vertical}{self.horizontal}"

class Knight(ChessPiece):
    def __init__(self, vertical, horizontal):
        ChessPiece.__init__(self, vertical, horizontal)

    def can_move(self, knight_vertical, knight_horizontal):
        if knight_horizontal not in "abcdefgh" or not (1 <= knight_vertical <= 8):
            return False
        horizontal_list = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
        current_x = horizontal_list[self.horizontal]
        target_x = horizontal_list[knight_horizontal]
        dx = abs(current_x - target_x)
        dy = abs(self.vertical - knight_vertical)
        if (dx == 2 and dy == 1) or (dx == 1 and dy == 2):
            return True
        return False

    def __str__(self):
        return f"Knight - {self.vertical}{self.horizontal}"

def test_pieces():
    king = King(4, "e")
    knight = Knight(5, "g")
    moves = [(5, "e"), (4, "f"), (5, "f"), (6, "h"), (3, "e"), (7, "g")]

    print(str(king))
    for move in moves:
        print(f"Can King move to {move[0]}{move[1]}? {king.can_move(move[0], move[1])}")

    print("\n" + str(knight))
    for move in moves:
        print(f"Can Knight move to {move[0]}{move[1]}? {knight.can_move(move[0], move[1])}")

test_pieces()

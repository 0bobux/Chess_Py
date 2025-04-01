class Piece:
    """
    Базовый класс для шашечных фигур.
    """
    def __init__(self, color):
        self.color = color  # 'white' или 'black'
        self.symbol = '⛀' if color == 'white' else '⛂'  # Символ для обычной шашки

    def get_valid_moves(self, board, start_row, start_col):
        raise NotImplementedError("Этот метод должен быть переопределен в дочерних классах.")

    def __str__(self):
        return self.symbol


class Checker(Piece):
    """
    Обычная шашка.
    """
    def get_valid_moves(self, board, start_row, start_col):
        moves = []
        direction = -1 if self.color == 'white' else 1  # Белые ходят вверх, черные вниз

        # Обычные ходы по диагонали
        for dc in [-1, 1]:
            new_row, new_col = start_row + direction, start_col + dc
            if board.is_on_board(new_row, new_col) and not board.get_piece(new_row, new_col):
                moves.append((new_row, new_col))

        # Ходы с взятием (перепрыгивание через соседнюю вражескую шашку)
        for dc in [-1, 1]:
            mid_row, mid_col = start_row + direction, start_col + dc
            end_row, end_col = start_row + 2 * direction, start_col + 2 * dc
            if board.is_on_board(end_row, end_col):
                mid_piece = board.get_piece(mid_row, mid_col)
                end_piece = board.get_piece(end_row, end_col)
                if mid_piece and mid_piece.color != self.color and not end_piece:
                    moves.append((end_row, end_col))
        return moves


class KingChecker(Piece):
    """
    Шашка, ставшая дамкой (фlying king).
    Дамка ходит по диагонали как слон в шахматах и может захватывать вражескую шашку,
    только если прыжок (перешагивание) возможен.
    """
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '⛁' if color == 'white' else '⛃'

    def get_valid_moves(self, board, start_row, start_col):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            row, col = start_row, start_col
            enemy_found = False  # Флаг: в этой диагонали уже встретили вражескую шашку
            while True:
                row += dr
                col += dc
                if not board.is_on_board(row, col):
                    break

                current = board.get_piece(row, col)
                if not enemy_found:
                    # Пока по пути пусто, дамка может ходить
                    if not current:
                        moves.append((row, col))
                    else:
                        # Если встречаем фигуру
                        if current.color != self.color:
                            # Это потенциальное захватывающее движение.
                            enemy_found = True
                            # Теперь ищем пустые клетки сразу за врагом
                            jump_row, jump_col = row + dr, col + dc
                            while board.is_on_board(jump_row, jump_col) and not board.get_piece(jump_row, jump_col):
                                moves.append((jump_row, jump_col))
                                jump_row += dr
                                jump_col += dc
                        # В любом случае останавливаем дальнейшее движение по этой диагонали.
                        break
                else:
                    # Если уже встретили врага, не продолжаем движение.
                    break
        return moves


class Board:
    def __init__(self):
        self.grid = {}
        self.setup_pieces()

    def setup_pieces(self):
        """
        Расстановка шашек в начальной позиции.
        Шашки ставятся только на клетках с (row+col) % 2 == 1.
        """
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[(row, col)] = Checker('black')
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[(row, col)] = Checker('white')

    def is_on_board(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def get_piece(self, row, col):
        return self.grid.get((row, col))

    def remove_piece(self, row, col):
        if (row, col) in self.grid:
            del self.grid[(row, col)]

    def move_piece(self, start, end):
        """
        Двигает фигуру с клетки start в end.
        Если ход является захватывающим (jump), удаляет первую встреченную вражескую шашку.
        """
        piece = self.grid.get(start)
        if not piece:
            return

        # Определяем, является ли ход захватывающим: если разница по строкам больше 1.
        if abs(start[0] - end[0]) > 1 and abs(start[1] - end[1]) > 1:
            dr = 1 if end[0] > start[0] else -1
            dc = 1 if end[1] > start[1] else -1
            row, col = start[0] + dr, start[1] + dc
            # Ищем первую занятую клетку на пути
            while (row, col) != end:
                if (row, col) in self.grid and self.grid[(row, col)].color != piece.color:
                    # Это съеденная шашка
                    del self.grid[(row, col)]
                    break
                row += dr
                col += dc

        self.grid[end] = piece
        del self.grid[start]

        # Превращение обычной шашки в дамку, если она дошла до конца поля.
        if isinstance(piece, Checker):
            if (piece.color == 'white' and end[0] == 0) or (piece.color == 'black' and end[0] == 7):
                self.grid[end] = KingChecker(piece.color)

    def print_board(self):
        print("   a  b c  d  e f  g  h")
        for row in range(8):
            print(8 - row, end="  ")
            for col in range(8):
                piece = self.get_piece(row, col)
                # Выводим символы шашек или пустые клетки (для шахматных полей используем разные символы)
                if piece:
                    print(str(piece), end=" ")
                else:
                    # Цвет клетки определяется по (row+col) % 2:
                    print('▭' if (row+col) % 2 == 0 else '▬', end=" ")
            print("", 8 - row)
        print("   a  b c  d  e f  g  h")


class Game:
    def __init__(self):
        self.board = Board()
        self.current_turn = 'white'

    def switch_turn(self):
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def algebraic_to_coords(self, pos):
        if len(pos) != 2 or pos[0] not in "abcdefgh" or pos[1] not in "12345678":
            return None
        col = ord(pos[0]) - ord('a')
        row = 8 - int(pos[1])
        return row, col

    def is_valid_move(self, start, end):
        piece = self.board.get_piece(start[0], start[1])
        if not piece or piece.color != self.current_turn:
            return False
        return end in piece.get_valid_moves(self.board, start[0], start[1])

    def play(self):
        while True:
            self.board.print_board()
            print(f"Ходит {'белый' if self.current_turn == 'white' else 'чёрный'}.")

            start_pos = input("Введите позицию шашки (например, b6): ")
            end_pos = input("Введите конечную позицию (например, c5): ")

            start = self.algebraic_to_coords(start_pos)
            end = self.algebraic_to_coords(end_pos)

            if start and end and self.is_valid_move(start, end):
                self.board.move_piece(start, end)
                self.switch_turn()
            else:
                print("Некорректный ход, попробуйте снова.")


if __name__ == "__main__":
    game = Game()
    game.play()

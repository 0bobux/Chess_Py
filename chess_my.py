class Piece:
    """
    Базовый класс для фигур.
    """
    def __init__(self, color):
        self.color = color # color: 'white' или 'black'
        self.symbol = '?' # Переопределяется в потомках

    def get_valid_moves(self, board, start_row, start_col):
        """
        Возвращает список (row, col), куда может пойти фигура с начального положения(start_row, start_col).
        :param board:
        :param start_row:
        :param start_col:
        :return:
        """
        raise NotImplementedError("Этот метод нужно переопределить в дочерних классах.")

    def __str__(self):
        """
        Определяет как фигура будет печататься ("♙" или "p")
        :return:
        """
        return self.symbol

class Pawn(Piece): # пешка
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♙' if color == 'white' else '♟'

    def get_valid_moves(self, board, start_row, start_col):
        moves = []
        # У белых пешка движется "вверх" (row уменьшается), у чёрных — "вниз" (row увеличивается).
        # Но как именно – зависит от того, как вы решили считать координаты.
        # Допустим, row=0 вверху, row=7 внизу, тогда белая пешка ходит от row=6 к row=5 и т.д.
        direction = -1 if self.color == 'white' else 1

        # 1) Ход вперёд на 1 клетку (если она свободна)
        forward_row = start_row + direction
        if board.is_on_board(forward_row, start_col) and not board.get_piece(forward_row, start_col):
            moves.append((forward_row, start_col))

            # 2) Если пешка в начальной позиции, может сделать ход на 2 клетки (если свободно)
            if self.color == 'white' and start_row == 6:
                two_forward = start_row + 2 * direction
                if not board.get_piece(two_forward, start_col):
                    moves.append((two_forward, start_col))
            if self.color == 'black' and start_row == 1:
                two_forward = start_row + 2 * direction
                if not board.get_piece(two_forward, start_col):
                    moves.append((two_forward, start_col))

        # 3) Съесть фигуру по диагоналям
        for dc in [-1, 1]:
            diag_row = start_row + direction
            diag_col = start_col + dc
            if board.is_on_board(diag_row, diag_col):
                piece = board.get_piece(diag_row, diag_col)
                # Если там фигура противоположного цвета, можно её "съесть"
                if piece and piece.color != self.color:
                    moves.append((diag_row, diag_col))

        return moves

class Rook(Piece): # ладья
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♖' if color == 'white' else '♜'

    def get_valid_moves(self, board, start_row, start_col):
        moves = []
        # Ладья ходит по вертикали и горизонтали
        directions = [(1, 0),(-1, 0),(0, 1),(0, -1)]
        for d_row, d_col in directions:
            # Для каждого направления получаем все ходы вдоль линии
            line_moves = board.get_line_moves(self, start_row, start_col, d_row, d_col)
            moves.extend(line_moves)
        return moves

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♘' if color == 'white' else '♞'

    def get_valid_moves(self, board, start_row, start_col):
        moves = []
        # Возможные ходы коня (две клетки в одном направлении и одна в перпендикулярном)
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        for dr, dc in knight_moves:
            r = start_row + dr
            c = start_col + dc
            # Проверяем, что клетка (r, c) находится внутри доски
            if board.is_on_board(r, c):
                piece = board.get_piece(r, c)
                # Если клетка свободна или занята противником, ход допустим
                if not piece or piece.color != self.color:
                    moves.append((r, c))
        return moves

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♗' if color == 'white' else '♝'

    def get_valid_moves(self, board, start_row, start_col):
        moves = []
        # Слон движется по диагоналям: 4 диагональных направления
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for d_row, d_col in directions:
            moves.extend(board.get_line_moves(self, start_row, start_col, d_row, d_col))
        return moves

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♕' if color == 'white' else '♛'

    def get_valid_moves(self, board, start_row, start_col):
        moves = []
        # Ферзь может двигаться как ладья (вертикаль/горизонталь) и как слон (диагонали)
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1), # вертикальные и горизонтальные направления
            (1, 1), (1, -1), (-1, 1), (-1, -1) # диагональные направления
        ]
        for d_row, d_col in directions:
            moves.extend(board.get_line_moves(self, start_row, start_col, d_row, d_col))
        return moves

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♔' if color == 'white' else '♚'

    def get_valid_moves(self, board, start_row, start_col):
        moves = []
        # Король перемещается на одну клетку во всех 8 направлениях
        king_moves = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        for dr, dc in king_moves:
            r = start_row + dr
            c = start_col + dc
            if board.is_on_board(r, c):
                piece = board.get_piece(r, c)
                # Король может пойти, если клетка свободна или там фигура противника
                if not piece or piece.color != self.color:
                    moves.append((r, c))
        return moves

class Board:
    def __init__(self):
        # Словарь: ключ = (row, col), значение = объект Piece или None
        self.grid = {}
        self.setup_pieces()

    def setup_pieces(self):
        """
        Расставляем фигуры в стандартную начальную позицию.
        """
        # пешки
        for col in range(8):
            self.grid[(6, col)] = Pawn('white')
            self.grid[(1, col)] = Pawn('black')

        # ладьи
        self.grid[(7, 0)] = Rook('white')
        self.grid[(7, 7)] = Rook('white')
        self.grid[(0, 0)] = Rook('black')
        self.grid[(0, 7)] = Rook('black')

        # кони
        self.grid[(7, 1)] = Knight('white')
        self.grid[(7, 6)] = Knight('white')
        self.grid[(0, 1)] = Knight('black')
        self.grid[(0, 6)] = Knight('black')

        # слоны
        self.grid[(7, 2)] = Bishop('white')
        self.grid[(7, 5)] = Bishop('white')
        self.grid[(0, 2)] = Bishop('black')
        self.grid[(0, 5)] = Bishop('black')

        # ферзи
        self.grid[(7, 3)] = Queen('white')
        self.grid[(0, 3)] = Queen('black')

        # короли
        self.grid[(7, 4)] = King('white')
        self.grid[(0, 4)] = King('black')

    def is_on_board(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def get_piece(self, row, col):
        # Возвращаем фигуру, если есть, иначе None
        return self.grid.get((row, col))

    def move_piece(self, start, end):
        """
        Передвигает фигуру с клетки start в end.
        Предполагается, что ход уже проверен (is_valid_move).
        :param start:
        :param end:
        :return:
        """
        piece = self.grid.get(start)
        if piece:
            self.grid[end] = piece
            del self.grid[start]

    def print_board(self):
        """
        Печатает доску в консоль.
        Сверху - 8-я горизонталь (row=0), снизу - 1-я (row=7).
        Слева направо - столбцы a..h (col=0..7).
        :return:
        """
        print("   a  b c  d  e  f g  h")
        for row in range(8):
            print(8 - row, end="  ")
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece:
                    print(str(piece), end=" ")
                else:
                    print('▭', end=" ")  # Пустая клетка
            print(" ", 8 - row)
        print("   a  b c  d  e  f g  h")

    def get_line_moves(self, piece, start_row, start_col, d_row, d_col):
        """
        Вспомогательный метод для ладьи/слона/ферзя.
        Возвращает все допустимые клетки вдоль направления (d_row, d_col),
        пока не встретим край доски или фигуру.
        :param piece:
        :param start_row:
        :param start_col:
        :param d_row:
        :param d_col:
        :return:
        """
        moves = []
        r = start_row + d_row
        c = start_col + d_col
        while self.is_on_board(r, c):
            existing_piece = self.get_piece(r, c)
            if existing_piece:
                # Если это фигура соперника, её можно "взять" и остановиться
                if existing_piece.color != piece.color:
                    moves.append((r, c))
                # Если своя или чужая, дальше идти нельзя
                break
            else:
                # Пустая клетка — можем туда пойти
                moves.append((r, c))
            r += d_row
            c += d_col
        return moves

    def is_valid_move(self, start, end, current_color):
        """
        Проверяет, что на клетке start стоит фигура нужного цвета,
        и что ход в end входит в список допустимых ходов для этой фигуры.
        (Без учёта шаха/мата, рокировки и т.д.)
        :param start:
        :param end:
        :param current_color:
        :return:
        """
        piece = self.get_piece(start[0], start[1])
        if not piece:
            return False, "На выбранной клетке нет фигуры."
        if piece.color != current_color:
            return False, "Фигура не принадлежит текущему игроку."

        valid_positions = piece.get_valid_moves(self, start[0], start[1])
        if end not in valid_positions:
            return False, "Недопустимый ход для выбранной фигуры."

        return True, ""

    @staticmethod
    def algebraic_to_coords(pos_str):
        """
        Переводит 'a1' -> (7, 0), 'e2' -> (6, 4) и т.п.
        :param pos_str:
        :return:
        """
        if len(pos_str) != 2:
            return None
        col_letter = pos_str[0].lower() # 'a'..'h'
        row_digit = pos_str[1] # '1'..'8'

        if col_letter < 'a' or col_letter > 'h':
            return None
        if row_digit < '1' or row_digit > '8':
            return None

        col = ord(col_letter) - ord('a') # 'a'->0, 'b'->1
        row = 8 - int(row_digit) # '1'->7, '8'->0
        return (row, col)

class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = 'white'
        self.move_count = 0

    def switch_player(self):
        self.current_player = 'black' if self.current_player == 'white' else 'white'

    def run(self):
        while True:
            # 1. Печатаем доску
            self.board.print_board()
            print(f"Ход номер: {self.move_count}. Сейчас ходят {self.current_player}.")

            # 2. Считываем начальную позицию
            start_str = input(f"Введите позицию фигуры ({self.current_player}), например e2 (или 'exit'): ")
            if start_str.lower() == 'exit':
                print("Игра завершена.")
                break

            start = self.board.algebraic_to_coords(start_str)
            if not start:
                print("Неверный формат ввода (пример: e2). Попробуйте ещё раз.")
                continue

            # 3. Считываем конечную позицию
            end_str = input("Введите целевую позицию, например e4 (или 'exit'): ")
            if end_str.lower() == 'exit':
                print("Игра завершена.")

            end = self.board.algebraic_to_coords(end_str)
            if not end:
                print("Неверный формат ввода (пример: e4). Попробуйте ещё раз.")
                continue

            # 4. Проверяем ход
            valid, message = self.board.is_valid_move(start, end, self.current_player)
            if not valid:
                print(f"Ход некорректен: {message}")
                continue

            # 5. Если ход корректен, двигаем фигуру
            self.board.move_piece(start, end)

            # 6. Увеличиваем счётчик, переключаем игрока
            self.move_count += 1
            self.switch_player()

if __name__ == "__main__":
    game = Game()
    game.run()
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

class Kamikaze(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '⸱K⸱' if color == 'white' else '⸱k⸱'

    def get_valid_moves(self, board, start_row, start_col):
        moves = []
        # 1. Ход влево и вправо на одну клетку
        for dc in [-1, 1]:
            r, c = start_row, start_col + dc
            if board.is_on_board(r, c):
                piece = board.get_piece(r, c)
                if not piece or piece.color != self.color:  # Свободная клетка или чужая фигура
                    moves.append((r, c))

        # 2. Ход вперед до конца
        direction = -1 if self.color == 'white' else 1
        r, c = start_row + direction, start_col
        while board.is_on_board(r, c):
            piece = board.get_piece(r, c)
            if piece:  # Если встретилась фигура
                if piece.color != self.color:  # Взорвем фигуру противника
                    moves.append((r, c))
                break  # Взорвемся или остановимся
            moves.append((r, c))
            r += direction  # Идем дальше

        return moves

    def explode(self, board, start_row, start_col, end_row, end_col):
        """
        Метод для подрыва фигуры. Уничтожает себя и фигуру противника.
        """
        # Проверим, существует ли фигура на клетке, на которую мы ходим.
        if (end_row, end_col) in board.grid:
            target_piece = board.get_piece(end_row, end_col)
            if target_piece and target_piece.color != self.color:  # Если фигура противника
                del board.grid[(end_row, end_col)]  # Удаляем фигуру противника

        # Удаляем камикадзе с доски (он больше не будет на исходной клетке)
        if (start_row, start_col) in board.grid:
            del board.grid[(start_row, start_col)]  # Удаляем камикадзе с доски

        # Камикадзе исчезает с доски
        return

class Commander(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '⬭' if color == 'white' else '⬬'

    def get_valid_moves(self, board, start_row, start_col):
        moves = []
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2),  # Ход как ферзь на 2 клетки
                      (2, 2), (2, -2), (-2, 2), (-2, -2)]
        for dr, dc in directions:
            r, c = start_row + dr, start_col + dc
            if board.is_on_board(r, c):
                piece = board.get_piece(r, c)
                if not piece or piece.color != self.color:
                    moves.append((r, c))

        # Взятие на проходе (отслеживание хода противника нужно реализовать отдельно)
        return moves

class Champion(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '⛉' if color == 'white' else '⛊'

    def get_valid_moves(self, board, start_row, start_col):
        moves = []
        knight_moves = [  # Прыжки через одну клетку
            (2, 2), (2, -2), (-2, 2), (-2, -2)
        ]
        for dr, dc in knight_moves:
            r, c = start_row + dr, start_col + dc
            if board.is_on_board(r, c):
                piece = board.get_piece(r, c)
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

        # Добавление новых фигур
        self.grid[(5, 0)] = Kamikaze('white')
        self.grid[(2, 7)] = Kamikaze('black')

        self.grid[(5, 3)] = Commander('white')
        self.grid[(2, 3)] = Commander('black')

        self.grid[(5, 4)] = Champion('white')
        self.grid[(2, 4)] = Champion('black')

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
            target = self.grid.get(end)
            # Если ходит Камикадзе и там есть враг — он взрывается
            if isinstance(piece, Kamikaze) and target:
                piece.explode(self, start[0], start[1], end[0], end[1])
            else:
                # Обычный ход
                self.grid[end] = piece
                del self.grid[start]

    def print_board(self, highlight_moves=None):
        """
        Печатает доску в консоль.
        Сверху - 8-я горизонталь (row=0), снизу - 1-я (row=7).
        Слева направо - столбцы a..h (col=0..7).
        :return:
        """
        highlight_moves = highlight_moves or []  # Если передали None, заменяем на пустой список

        print("   a  b c  d  e  f g  h")
        for row in range(8):
            print(8 - row, end="  ")
            for col in range(8):
                if (row, col) in highlight_moves:
                    print('▬', end=" ")  # Показываем возможный ход
                else:
                    piece = self.get_piece(row, col)
                    print(str(piece) if piece else '▭', end=" ")
            print("", 8 - row)
        print("   a  b c  d  e  f g  h")

    def show_valid_moves(self, piece, row, col):
        """
        Отображает возможные ходы фигуры на доске.
        """
        valid_moves = piece.get_valid_moves(self, row, col)
        self.print_board(highlight_moves=valid_moves)  # Отображаем доску с подсвеченными ходами

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
                # Если это фигура соперника, её можно "съесть" и остановиться
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

        # Показываем возможные ходы
        print(f"Возможные ходы для {piece}:")
        self.show_valid_moves(piece, start[0], start[1])

        valid_positions = piece.get_valid_moves(self, start[0], start[1])
        if end not in valid_positions:
            return False, "Недопустимый ход для выбранной фигуры."

        return True, ""

    def copy(self):
        new_board = Board()
        new_board.grid = self.grid.copy()  # Копируем текущие фигуры
        return new_board

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

class MoveHistory:
    def __init__(self):
        self.history = []

    def add_move(self, board_state):
        self.history.append(board_state)

    def undo_move(self):
        if self.history:
            return self.history.pop()
        return None

class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = 'white'
        self.move_count = 0
        self.history = MoveHistory()

    def switch_player(self):
        self.current_player = 'black' if self.current_player == 'white' else 'white'

    def run(self):
        while True:
            # 1. Печатаем доску
            self.board.print_board()
            print(f"Ход номер: {self.move_count}. Сейчас ходят {self.current_player}.")

            # 2. Считываем начальную позицию
            start_str = input(f"Введите позицию фигуры ({self.current_player}), например e2 (или 'exit' - для выхода из игры,\n'undo N' - для отмены N последних ходов): ")
            if start_str.lower() == 'exit':
                print("Игра завершена.")
                break
            elif start_str.lower().startswith('undo'):
                # Разбираем команду для отката нескольких ходов
                parts = start_str.split()
                if len(parts) == 2 and parts[1].isdigit():
                    undo_moves = int(parts[1])
                    success = False  # Флаг, который проверяет, был ли откат хотя бы одного хода
                    for _ in range(undo_moves):
                        last_state = self.history.undo_move()
                        if last_state:
                            self.board = last_state
                            self.move_count -= 1
                            self.switch_player()
                            success = True
                        else:
                            print("Нет хода для отката.")

                    if success:
                        print(f"Откат на {undo_moves} ход(ов).")
                    continue

            start = self.board.algebraic_to_coords(start_str)
            if not start:
                print("Неверный формат ввода (пример: e2). Попробуйте ещё раз.")
                continue

            # Подсветка возможных ходов для выбранной фигуры
            piece = self.board.get_piece(start[0], start[1])
            if piece and piece.color == self.current_player:
                self.board.show_valid_moves(piece, start[0], start[1])

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

            # Сохраняем текущее состояние доски в историю перед выполнением хода
            self.history.add_move(self.board.copy())  # предполагаем, что нужно реализовать метод copy()

            # 5. Если ход корректен, двигаем фигуру
            self.board.move_piece(start, end)

            # 6. Увеличиваем счётчик, переключаем игрока
            self.move_count += 1
            self.switch_player()

if __name__ == "__main__":
    game = Game()
    game.run()
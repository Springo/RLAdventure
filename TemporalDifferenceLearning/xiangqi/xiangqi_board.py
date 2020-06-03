import copy

class XiangqiBoard:
    """
    0: empty
    1: pawn
    2: general
    3: advisor
    4: elephant
    5: horse
    6: cannon
    7: chariot
    """
    def __init__(self, grid=None):
        if grid is None:
            self.grid = [
                [-7, -5, -4, -3, -2, -3, -4, -5, -7],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, -6, 0, 0, 0, 0, 0, -6, 0],
                [-1, 0, -1, 0, -1, 0, -1, 0, -1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 1, 0, 1, 0, 1],
                [0, 6, 0, 0, 0, 0, 0, 6, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [7, 5, 4, 3, 2, 3, 4, 5, 7]
            ]
        else:
            self.grid = grid

    def _get_pawn_moves(self, row, col):
        moves = []
        if row > 0:
            if self.grid[row - 1][col] <= 0:
                moves.append((row - 1, col))
        if row <= 4:
            if col > 0 and self.grid[row][col - 1] <= 0:
                moves.append((row, col - 1))
            if col < 8 and self.grid[row][col + 1] <= 0:
                moves.append((row, col - 1))
        return moves

    def _get_general_moves(self, row, col):
        moves = []
        if col > 3 and self.grid[row][col - 1] <= 0:
            moves.append((row, col - 1))
        if col < 5 and self.grid[row][col + 1] <= 0:
            moves.append((row, col + 1))
        if row > 7 and self.grid[row - 1][col] <= 0:
            moves.append((row - 1, col))
        if row < 9 and self.grid[row + 1][col] <= 0:
            moves.append((row + 1, col))
        return moves

    def _get_advisor_moves(self, row, col):
        moves = []
        if col > 3 and row > 7 and self.grid[row - 1][col - 1] <= 0:
            moves.append((row - 1, col - 1))
        if col > 3 and row < 9 and self.grid[row + 1][col - 1] <= 0:
            moves.append((row + 1, col - 1))
        if col < 5 and row > 7 and self.grid[row - 1][col + 1] <= 0:
            moves.append((row - 1, col + 1))
        if col < 5 and row < 9 and self.grid[row + 1][col + 1] <= 0:
            moves.append((row + 1, col + 1))
        return moves

    def _get_elephant_moves(self, row, col):
        moves = []
        if col > 1 and row > 6 and self.grid[row - 2][col - 2] <= 0:
            moves.append((row - 2, col - 2))
        if col > 1 and row < 8 and self.grid[row + 2][col - 2] <= 0:
            moves.append((row + 2, col - 2))
        if col < 7 and row > 6 and self.grid[row - 2][col + 2] <= 0:
            moves.append((row - 2, col + 2))
        if col < 7 and row < 8 and self.grid[row + 2][col + 2] <= 0:
            moves.append((row + 2, col + 2))
        return moves

    def _get_horse_moves(self, row, col):
        moves = []
        if row > 1 and self.grid[row - 1][col] == 0:
            if col > 0 and self.grid[row - 2][col - 1] <= 0:
                moves.append((row - 2, col - 1))
            if col < 8 and self.grid[row - 2][col + 1] <= 0:
                moves.append((row - 2, col + 1))
        if row < 8 and self.grid[row + 1][col] == 0:
            if col > 0 and self.grid[row + 2][col - 1] <= 0:
                moves.append((row + 2, col - 1))
            if col < 8 and self.grid[row + 2][col + 1] <= 0:
                moves.append((row + 2, col + 1))
        if col > 1 and self.grid[row][col - 1] == 0:
            if row > 0 and self.grid[row - 1][col - 2] <= 0:
                moves.append((row - 1, col - 2))
            if row < 9 and self.grid[row + 1][col - 2] <= 0:
                moves.append((row + 1, col - 2))
        if col < 7 and self.grid[row][col + 1] == 0:
            if row > 0 and self.grid[row - 1][col + 2] <= 0:
                moves.append((row - 1, col - 2))
            if row < 9 and self.grid[row + 1][col + 2] <= 0:
                moves.append((row + 1, col - 2))
        return moves

    def _get_chariot_moves(self, row, col):
        moves = []
        for step in range(1, row + 1):
            if self.grid[row - step][col] <= 0:
                moves.append((row - step, col))
                if self.grid[row - step][col] < 0:
                    break
            else:
                break
        for step in range(1, 10 - row):
            if self.grid[row + step][col] <= 0:
                moves.append((row + step, col))
                if self.grid[row + step][col] < 0:
                    break
            else:
                break
        for step in range(1, col + 1):
            if self.grid[row][col - step] <= 0:
                moves.append((row, col - step))
                if self.grid[row][col - step] < 0:
                    break
            else:
                break
        for step in range(1, 9 - col):
            if self.grid[row][col + step] <= 0:
                moves.append((row, col + step))
                if self.grid[row][col + step] < 0:
                    break
            else:
                break
        return moves

    def _get_cannon_moves(self, row, col):
        moves = []
        hop = False
        for step in range(1, row + 1):
            if not hop:
                if self.grid[row - step][col] == 0:
                    moves.append((row - step, col))
                else:
                    hop = True
            else:
                if self.grid[row - step][col] < 0:
                    moves.append((row - step, col))
                    break
        hop = False
        for step in range(1, 10 - row):
            if not hop:
                if self.grid[row + step][col] <= 0:
                    moves.append((row + step, col))
                else:
                    hop = True
            else:
                if self.grid[row + step][col] < 0:
                    moves.append((row + step, col))
                    break
        hop = False
        for step in range(1, col + 1):
            if not hop:
                if self.grid[row][col - step] <= 0:
                    moves.append((row, col - step))
                else:
                    hop = True
            else:
                if self.grid[row][col - step] < 0:
                    moves.append((row, col - step))
                    break
        hop = False
        for step in range(1, 9 - col):
            if not hop:
                if self.grid[row][col + step] <= 0:
                    moves.append((row, col + step))
                else:
                    hop = True
            else:
                if self.grid[row][col + step] < 0:
                    moves.append((row, col + step))
                    break
        return moves

    def _check_facing_generals(self):
        for row in range(2):
            for col in range(3, 5):
                if self.grid[row][col] == -2:
                    for step in range(9 - row):
                        if self.grid[row + step][col] == 2:
                            return True
                        elif self.grid[row + step][col] != 0:
                            return False
        return False

    def get_possible_moves(self, check_checks=True, include_boards=False):
        moves = []
        for row in range(10):
            for col in range(9):
                new_moves = []
                if self.grid[row][col] == 1:
                    new_moves = self._get_pawn_moves(row, col)
                if self.grid[row][col] == 2:
                    new_moves = self._get_general_moves(row, col)
                if self.grid[row][col] == 3:
                    new_moves = self._get_advisor_moves(row, col)
                if self.grid[row][col] == 4:
                    new_moves = self._get_elephant_moves(row, col)
                if self.grid[row][col] == 5:
                    new_moves = self._get_horse_moves(row, col)
                if self.grid[row][col] == 6:
                    new_moves = self._get_cannon_moves(row, col)
                if self.grid[row][col] == 7:
                    new_moves = self._get_chariot_moves(row, col)
                for move in new_moves:
                    moves.append(((row, col), move))

        if check_checks:
            valid_moves = []
            boards = []
            for move in moves:
                valid = True
                new_board, _ = self.make_move(move)
                next_moves = new_board.get_possible_moves(check_checks=False)
                for next_move in next_moves:
                    end_row, end_col = next_move[1]
                    if new_board.grid[end_row][end_col] == -2:
                        valid = False
                    if new_board._check_facing_generals():
                        valid = False
                if valid:
                    valid_moves.append(move)
                    if include_boards:
                        boards.append(new_board)

            if include_boards:
                return valid_moves, boards
            return valid_moves

        return moves

    def _get_point_value(self, piece):
        if piece == 0:
            return 0
        elif piece == -1:
            return 1
        elif piece == -2:
            return 100000
        elif piece == -3:
            return 2
        elif piece == -4:
            return 2
        elif piece == -5:
            return 4
        elif piece == -6:
            return 4.5
        elif piece == -7:
            return 9
        else:
            print("Error: Took own piece.")
            return None

    def flip_board(self):
        new_grid = [[0] * 9 for _ in range(10)]
        for row in range(10):
            for col in range(9):
                new_grid[row][col] = -self.grid[9 - row][8 - col]
        return XiangqiBoard(grid=new_grid)

    def make_move(self, move):
        start_row, start_col = move[0]
        end_row, end_col = move[1]
        new_grid = copy.deepcopy(self.grid)
        points = self._get_point_value(new_grid[end_row][end_col])
        new_grid[end_row][end_col] = new_grid[start_row][start_col]
        new_grid[start_row][start_col] = 0
        return XiangqiBoard(grid=new_grid).flip_board(), points

    def print_board(self):
        for row in range(10):
            for col in range(9):
                if self.grid[row][col] == 0:
                    print(" _ ", end="")
                if self.grid[row][col] == 1:
                    print(" P ", end="")
                if self.grid[row][col] == 2:
                    print(" G ", end="")
                if self.grid[row][col] == 3:
                    print(" A ", end="")
                if self.grid[row][col] == 4:
                    print(" E ", end="")
                if self.grid[row][col] == 5:
                    print(" H ", end="")
                if self.grid[row][col] == 6:
                    print(" C ", end="")
                if self.grid[row][col] == 7:
                    print(" R ", end="")
                if self.grid[row][col] == -1:
                    print(" * ", end="")
                if self.grid[row][col] == -2:
                    print(" # ", end="")
                if self.grid[row][col] == -3:
                    print(" % ", end="")
                if self.grid[row][col] == -4:
                    print(" & ", end="")
                if self.grid[row][col] == -5:
                    print(" $ ", end="")
                if self.grid[row][col] == -6:
                    print(" @ ", end="")
                if self.grid[row][col] == -7:
                    print(" ! ", end="")
            print()


if __name__ == "__main__":
    board = XiangqiBoard()
    print(board.get_possible_moves(check_checks=True))
    board.print_board()
    new_board, points = board.make_move(((7, 1), (7, 4)))
    new_board, points = new_board.make_move(((9, 5), (8, 4)))
    new_board, points = new_board.make_move(((7, 4), (3, 4)))
    new_board.print_board()
    print(points)
    print(new_board.get_possible_moves(check_checks=True))

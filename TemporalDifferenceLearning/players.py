import random
import math
import copy


def check_win(player, grid, move):
    if (player != 1 and player != 2) or (move < 0 or move > 6) or grid[0][move] != 0:
        return False, True

    y = -1
    for i in range(len(grid)):
        if grid[len(grid) - i - 1][move] == 0:
            y = len(grid) - i - 1
            break

    # check horizontal
    counter = 1
    for i in range(3):
        if move + i + 1 > 6:
            break
        if grid[y][move + i + 1] == player:
            counter += 1
        else:
            break
    for i in range(3):
        if move - i - 1 < 0:
            break
        if grid[y][move - i - 1] == player:
            counter += 1
        else:
            break
    if counter >= 4:
        return True, False

    # check vertical
    counter = 1
    if y <= 2:
        for j in range(3):
            if grid[y + j + 1][move] == player:
                counter += 1
    if counter >= 4:
        return True, False

    # check diagonals:
    counter = 1
    for i in range(3):
        if move + i + 1 > 6 or y + i + 1 > 5:
            break
        if grid[y + i + 1][move + i + 1] == player:
            counter += 1
        else:
            break
    for i in range(3):
        if move - i - 1 < 0 or y - i - 1 < 0:
            break
        if grid[y - i - 1][move - i - 1] == player:
            counter += 1
        else:
            break
    if counter >= 4:
        return True, False

    counter = 1
    for i in range(3):
        if move + i + 1 > 6 or y - i - 1 < 0:
            break
        if grid[y - i - 1][move + i + 1] == player:
            counter += 1
        else:
            break
    for i in range(3):
        if move - i - 1 < 0 or y + i + 1 > 5:
            break
        if grid[y + i + 1][move - i - 1] == player:
            counter += 1
        else:
            break
    if counter >= 4:
        return True, False

    return False, False


class Player:
    def __init__(self, name):
        self.name = name
        self.move = -1

    def get_move(self):
        return -1

    def send_move(self, move):
        pass

    def send_state(self, player, board):
        pass


class HumanPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)

    def get_move(self):
        move = self.move
        self.move = -1
        return move

    def send_move(self, move):
        self.move = move


class RandomPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)

    def get_move(self):
        self.move = random.randint(0, 6)
        return self.move


class MinimaxPlayer(Player):
    def __init__(self, name, depth=2):
        Player.__init__(self, name)
        self.depth = depth
        self.player = None
        self.board = None

    def send_state(self, player, board):
        self.player = player
        self.board = board

    def get_move(self):
        best_move_score, move_scores = self.minimax(self.player, self.board, self.depth, True, -1000, 1000, force_all=True)
        print(self.player)
        print(move_scores)

        available_moves = []
        for move in range(7):
            if move_scores[move] == best_move_score:
                available_moves.append(move)

        choice = random.randint(0, len(available_moves) - 1)
        return available_moves[choice]

    def minimax(self, player, board, depth, maximize, alpha, beta, force_all=False):
        if maximize:
            move_scores = [-1000] * 7
        else:
            move_scores = [1000] * 7
        for move in range(7):
            win, invalid = check_win(player, board, move)
            if invalid:
                if maximize:
                    move_scores[move] = -1000
                else:
                    move_scores[move] = 1000
            else:
                if win:
                    if maximize:
                        move_scores[move] = 1
                        if not force_all:
                            alpha = max(alpha, 1)
                            if alpha >= beta:
                                return 1, move_scores
                    else:
                        move_scores[move] = -1
                        if not force_all:
                            beta = min(beta, -1)
                            if alpha >= beta:
                                return -1, move_scores
                else:
                    if depth == 0:
                        move_scores[move] = 0
                        if not force_all:
                            if maximize:
                                alpha = max(alpha, 0)
                                if alpha >= beta:
                                    return 0, move_scores
                            else:
                                beta = min(beta, 0)
                                if alpha >= beta:
                                    return 0, move_scores
                    else:
                        new_board = copy.deepcopy(board)
                        for i in range(len(new_board)):
                            if new_board[len(new_board) - i - 1][move] == 0:
                                new_board[len(new_board) - i - 1][move] = player
                                break
                        result, _ = self.minimax(3 - player, new_board, depth - 1, not maximize, alpha, beta)
                        result = result * 0.9
                        move_scores[move] = result

                        if not force_all:
                            if maximize:
                                alpha = max(alpha, result)
                                if alpha >= beta:
                                    return result, move_scores
                            else:
                                beta = min(beta, result)
                                if alpha >= beta:
                                    return result, move_scores

        if maximize:
            return max(move_scores), move_scores
        else:
            return min(move_scores), move_scores


if __name__ == "__main__":
    grid = [[0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 2, 2, 0, 0, 0]
            ]
    player = MinimaxPlayer("Bob", 4)
    player.send_state(1, grid)
    print(player.get_move())

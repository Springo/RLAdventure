import random
import math
import copy


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
        self.invalid = dict()
        self.invalid[-1] = True
        for i in range(7):
            self.invalid[i] = False

    def get_move(self):
        self.move = -1
        while self.invalid[self.move]:
            self.move = random.randint(0, 6)
        return self.move

    def send_state(self, player, board):
        for move in range(7):
            if board.heights[move] < 0:
                self.invalid[move] = True
            else:
                self.invalid[move] = False


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
            win, invalid = board.check_win(player, move)
            if invalid:
                if maximize:
                    move_scores[move] = -1.01
                else:
                    move_scores[move] = 1.01
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
                        new_board.input_move(player, move)
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

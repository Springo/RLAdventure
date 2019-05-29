import random
import math

class Player:
    def __init__(self, name):
        self.name = name
        self.move = 0

    def get_move(self):
        return 0

    def send_move(self, move):
        pass

    def send_feedback(self, result):
        pass


class HumanPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)

    def get_move(self):
        move = self.move
        self.move = 0
        return move

    def send_move(self, move):
        self.move = move


class RandomPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)

    def get_move(self):
        self.move = random.randint(1, 6)
        return self.move


class GreedyPlayer(Player):
    def __init__(self, name, epsilon=0):
        Player.__init__(self, name)
        self.epsilon = epsilon
        self.estimates = [0] * 6
        self.counts = [0] * 6

    def get_move(self):
        roll = random.random()
        if roll < self.epsilon:
            self.move = random.randint(1, 6)
        else:
            best_move = 0
            for i in range(len(self.estimates)):
                if self.counts[i] == 0:
                    self.move = i + 1
                    return self.move

                if self.estimates[i] > self.estimates[best_move]:
                    best_move = i
            self.move = best_move + 1
        return self.move

    def send_feedback(self, result):
        move_ind = self.move - 1
        total_damage = self.estimates[move_ind] * self.counts[move_ind]
        self.counts[move_ind] += 1
        self.estimates[move_ind] = (total_damage + result) / self.counts[move_ind]


class AnnealingGreedyPlayer(Player):
    def __init__(self, name, decrease_rate=1):
        Player.__init__(self, name)
        self.epsilon = 1.0
        self.estimates = [0] * 6
        self.counts = [0] * 6
        self.total = 0
        self.decrease_rate = decrease_rate

    def get_move(self):
        roll = random.random()
        if roll < self.epsilon:
            self.move = random.randint(1, 6)
        else:
            best_move = 0
            for i in range(len(self.estimates)):
                if self.counts[i] == 0:
                    self.move = i + 1
                    return self.move

                if self.estimates[i] > self.estimates[best_move]:
                    best_move = i
            self.move = best_move + 1
        return self.move

    def send_feedback(self, result):
        move_ind = self.move - 1
        total_damage = self.estimates[move_ind] * self.counts[move_ind]
        self.counts[move_ind] += 1
        self.estimates[move_ind] = (total_damage + result) / self.counts[move_ind]
        self.total += 1
        self.epsilon = 1.0 / (math.log2(self.total + 1) ** self.decrease_rate)


class UCBPlayer(Player):
    def __init__(self, name, conf=1):
        Player.__init__(self, name)
        self.estimates = [0] * 6
        self.counts = [0] * 6
        self.total = 0
        self.conf = conf

    def get_move(self):
        best_move = 0
        best_est = 0
        for i in range(len(self.estimates)):
            if self.counts[i] == 0:
                self.move = i + 1
                return self.move

            cur_est = self.estimates[i] + self.conf * (math.log(self.total + 1) / self.counts[i])
            if cur_est > best_est:
                best_move = i
                best_est = cur_est
        self.move = best_move + 1
        return self.move

    def send_feedback(self, result):
        move_ind = self.move - 1
        total_damage = self.estimates[move_ind] * self.counts[move_ind]
        self.counts[move_ind] += 1
        self.estimates[move_ind] = (total_damage + result) / self.counts[move_ind]
        self.total += 1

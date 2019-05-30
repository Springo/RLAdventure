import random
import math


class Player:
    def __init__(self, name):
        self.name = name
        self.move = -1

    def get_move(self):
        return -1

    def send_move(self, move):
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

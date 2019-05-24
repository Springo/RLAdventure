import random

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

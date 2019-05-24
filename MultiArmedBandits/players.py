import random

class Player:
    def __init__(self):
        pass

    def get_move(self):
        return 0

    def send_move(self, move):
        pass


class HumanPlayer(Player):
    def __init__(self):
        Player.__init__(self)
        self.move = 0

    def get_move(self):
        return self.move

    def send_move(self, move):
        self.move = move


class RandomPlayer(Player):
    def __init__(self):
        Player.__init__(self)

    def get_move(self):
        return random.randint(1, 6)

import numpy as np
import torch
import players
import connect_four_util as util
import connect_four_nets as nets


class ConnectFourSimulator:
    def __init__(self, player_1, player_2):
        self.p1 = player_1
        self.p2 = player_2

    def run(self, iters=1, verbose=False, data_out=None):
        p1_wins = 0
        p2_wins = 0
        ties = 0
        for i in range(iters):
            if verbose:
                print("=== Iteration {} ===".format(i + 1))

            # Set up board
            board = util.ConnectFourBoard()
            game_over = False
            win_message = ""
            turn = 1
            move = -1
            state_stack = []

            while not game_over:
                state_stack.append(board.package_state())

                if turn == 1:
                    self.p1.send_state(1, board)
                    move = self.p1.get_move()
                    if verbose:
                        print("\n{} played move {}.".format(self.p1.name, move))
                elif turn == 2:
                    self.p2.send_state(2, board)
                    move = self.p2.get_move()
                    if verbose:
                        print("\n{} played move {}.".format(self.p2.name, move))

                if move != -1:
                    win, _ = board.check_win(turn, move)
                    check = board.input_move(turn, move)
                    if check == 0:
                        if verbose:
                            board.print_board()
                        tie = board.check_tie()
                        if win:
                            game_over = True
                            if turn == 1:
                                win_message = "Player 1 ({}) wins.".format(self.p1.name)
                                p1_wins += 1
                            elif turn == 2:
                                win_message = "Player 2 ({}) wins.".format(self.p2.name)
                                p2_wins += 1
                        elif tie:
                            game_over = True
                            win_message = "Draw."
                            ties += 1
                        else:
                            turn = 3 - turn
                    else:
                        print("Error: Received invalid move.")
                        exit()
                    move = -1
                else:
                    print("Error: Received invalid move.")
                    exit()

            if verbose:
                print()
                print(win_message)
            else:
                print("[{}/{}] {}".format(i + 1, iters, win_message))

            if data_out is not None:
                data = []
                win_value = 1
                while len(state_stack) > 0:
                    state = state_stack.pop()
                    state.append(win_value)
                    data.append(state)
                    win_value *= -0.9
                util.save_to_file(data_out, data)


        print("=== Statistics ===")
        print("{} ({}%) wins by Player 1 ({})".format(p1_wins, 100.0 * p1_wins / iters, self.p1.name))
        print("{} ({}%) wins by Player 2 ({})".format(p2_wins, 100.0 * p2_wins / iters, self.p2.name))
        print("{} ({}%) ties".format(ties, 100.0 * ties / iters))


if __name__ == "__main__":
    net = nets.Connect4Network()
    data = util.read_from_file("test.csv")
    X, y = util.split_features_labels(data)
    X, y = util.shuffle_data(X, y)
    X = np.expand_dims(X, axis=1)
    X = torch.from_numpy(X).float()
    y = torch.from_numpy(y).float()
    net.fit(X, y)

    player_1 = players.DeepMinimaxPlayer("Deep", net, 4)
    #player_1 = players.RandomPlayer("Bimbo")
    player_2 = players.MinimaxPlayer("Max", 4)

    gs = ConnectFourSimulator(player_1, player_2)
    gs.run(10, verbose=False, data_out="test.csv")

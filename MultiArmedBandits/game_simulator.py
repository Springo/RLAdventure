import random
import players


class GameSimulator:
    def __init__(self, player_1, player_2, health_1=1000, health_2=1000):
        self.p1 = player_1
        self.p2 = player_2
        self.max_hp_1 = health_1
        self.max_hp_2 = health_2

    def reset_players(self):
        self.p1.reset_memory()
        self.p2.reset_memory()

    def run(self, iters=1, retain_memory=False, verbose=False):
        p1_wins = 0
        p2_wins = 0
        ties = 0
        for i in range(iters):
            if verbose:
                print("=== Iteration {} ===".format(i + 1))

            # Reset players
            if not retain_memory:
                self.reset_players()

            # Reset health
            hp_1 = self.max_hp_1
            hp_2 = self.max_hp_2

            # Reset weapons
            weapon_damages = [random.uniform(5, 15) for _ in range(6)]
            p1_weapons = weapon_damages[:]
            random.shuffle(p1_weapons)
            p2_weapons = weapon_damages[:]
            random.shuffle(p2_weapons)

            if verbose:
                print("Player 1 weapons: {}".format(p1_weapons))
                print("Player 2 weapons: {}".format(p2_weapons))

            game_over = False
            while not game_over:
                # Select move
                move_1 = self.p1.get_move()
                move_2 = self.p2.get_move()
                if move_1 <= 0 or move_1 > 6 or move_2 <= 0 or move_2 > 6:
                    print("Error: Received invalid move")
                    exit()

                if verbose:
                    print("Player 1 ({}/{}): {} | Player 2 ({}/{}): {}".format(hp_1, self.max_hp_1, move_1, hp_2,
                                                                               self.max_hp_2, move_2))

                # Apply damage
                damage_1 = round(max(0.0, p1_weapons[move_1 - 1] + random.gauss(0, 3)))
                damage_2 = round(max(0.0, p2_weapons[move_2 - 1] + random.gauss(0, 3)))
                hp_2 -= damage_1
                hp_1 -= damage_2

                # Send feedback
                self.p1.send_feedback(damage_1)
                self.p2.send_feedback(damage_2)

                if hp_1 <= 0 or hp_2 <= 0:
                    game_over = True
                    win_message = ""

                    if hp_1 <= 0 and hp_2 > 0:
                        win_message = "Player 2 ({}) wins.".format(self.p2.name)
                        p2_wins += 1
                    elif hp_2 <= 0 and hp_1 > 0:
                        win_message = "Player 1 ({}) wins.".format(self.p1.name)
                        p1_wins += 1
                    else:
                        win_message = "Tie."
                        ties += 1

                    if verbose:
                        print(win_message)
                    else:
                        print("[{}/{}] {}".format(i + 1, iters, win_message))

        print("=== Statistics ===")
        print("{} ({}%) wins by Player 1 ({})".format(p1_wins, 100.0 * p1_wins / iters, self.p1.name))
        print("{} ({}%) wins by Player 2 ({})".format(p2_wins, 100.0 * p2_wins / iters, self.p2.name))
        print("{} ({}%) ties".format(ties, 100.0 * ties / iters))


if __name__ == "__main__":
    # player_1 = players.RandomPlayer("Bimbo")
    player_1 = players.GreedyPlayer("Scrooge")
    # player_1 = players.GreedyPlayer("Donald", 0.01)
    # player_1 = players.GreedyPlayer("Hillary", 0.1)
    # player_1 = players.AnnealingGreedyPlayer("Theodore", 2)
    # player_1 = players.UCBPlayer("Ellen", 1)
    # player_2 = players.RandomPlayer("Bimbo")
    # player_2 = players.GreedyPlayer("Scrooge")
    # player_2 = players.GreedyPlayer("Donald", 0.01)
    # player_2 = players.GreedyPlayer("Hillary", 0.1)
    player_2 = players.AnnealingGreedyPlayer("Theodore", 2)
    # player_2 = players.UCBPlayer("Ellen", 1)

    gs = GameSimulator(player_1, player_2, health_1=10000, health_2=10000)
    gs.run(1000)

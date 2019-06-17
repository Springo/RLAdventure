import csv
import numpy as np


class ConnectFourBoard:
    def __init__(self):
        self.grid = [[0] * 7 for _ in range(6)]
        self.heights = [5] * 7

    def input_move(self, player, move):
        if (player != 1 and player != 2) or (move < 0 or move > 6) or (self.heights[move] < 0):
            return -1
        self.grid[self.heights[move]][move] = player
        self.heights[move] -= 1
        return 0

    def check_win(self, player, move):
        if (player != 1 and player != 2) or (move < 0 or move > 6) or (self.heights[move] < 0):
            return False, True

        y = self.heights[move]

        # check horizontal
        counter = 1
        for i in range(3):
            if move + i + 1 > 6:
                break
            if self.grid[y][move + i + 1] == player:
                counter += 1
            else:
                break
        for i in range(3):
            if move - i - 1 < 0:
                break
            if self.grid[y][move - i - 1] == player:
                counter += 1
            else:
                break
        if counter >= 4:
            return True, False

        # check vertical
        counter = 1
        if y <= 2:
            for j in range(3):
                if self.grid[y + j + 1][move] == player:
                    counter += 1
        if counter >= 4:
            return True, False

        # check diagonals:
        counter = 1
        for i in range(3):
            if move + i + 1 > 6 or y + i + 1 > 5:
                break
            if self.grid[y + i + 1][move + i + 1] == player:
                counter += 1
            else:
                break
        for i in range(3):
            if move - i - 1 < 0 or y - i - 1 < 0:
                break
            if self.grid[y - i - 1][move - i - 1] == player:
                counter += 1
            else:
                break
        if counter >= 4:
            return True, False

        counter = 1
        for i in range(3):
            if move + i + 1 > 6 or y - i - 1 < 0:
                break
            if self.grid[y - i - 1][move + i + 1] == player:
                counter += 1
            else:
                break
        for i in range(3):
            if move - i - 1 < 0 or y + i + 1 > 5:
                break
            if self.grid[y + i + 1][move - i - 1] == player:
                counter += 1
            else:
                break
        if counter >= 4:
            return True, False

        return False, False

    def check_tie(self):
        for i in range(len(self.heights)):
            if self.heights[i] >= 0:
                return False
        return True

    def print_board(self):
        for row in self.grid:
            for elem in row:
                if elem == 0:
                    print("| ", end="")
                elif elem == 1:
                    print("|#", end="")
                elif elem == 2:
                    print("|O", end="")
            print("|")

    def package_state(self):
        output = []
        for row in self.grid:
            for elem in row:
                output.append(elem)
        return output


def save_to_file(filename, data):
    with open(filename, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data)


def read_from_file(filename):
    data = []
    with open(filename, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            data.append(row)
    return np.matrix(data)


def split_features_labels(data):
    features = data[:, 0:-1].astype(int)
    labels = np.squeeze(np.array(data[:, -1].astype(float)))
    features = np.array(features).reshape((features.shape[0], 6, 7))
    return features, labels


def shuffle_data(X, y):
    idx = np.random.permutation(X.shape[0])
    return X[idx], y[idx]


if __name__ == "__main__":
    data = read_from_file("test.csv")
    X, y = split_features_labels(data)
    print(X.shape)
    print(y.shape)
    print(y)

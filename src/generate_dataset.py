#!/usr/bin/env python3
import os
import chess.pgn
import numpy as np
from state import State


class Dataset(object):
    def __init__(self, samples):
        self.num_samples = samples

    def generate_dataset(self):
        X, Y = [], []
        gn = 0
        values = {"1/2-1/2": 0, "0-1": -1, "1-0": 1}

        # pgn files in the data folder
        for fn in os.listdir("../data"):
            pgn = open(os.path.join("../data", fn))
            while 1:
                game = chess.pgn.read_game(pgn)
                if game is None:
                    break
                res = game.headers["Result"]
                if res not in values:
                    continue

                value = values[res]
                board = game.board()

                for i, move in enumerate(game.mainline_moves()):
                    board.push(move)
                    ser = State(board).serialize()

                    X.append(ser)
                    Y.append(value)

                print("parsing game %d, got %d examples" % (gn, len(X)))

                if self.num_samples is not None and len(X) > self.num_samples:
                    return X, Y
                gn += 1

        X = np.array(X)
        Y = np.array(Y)

        return X, Y


if __name__ == "__main__":
    dataset = Dataset(25000)
    X, Y = dataset.generate_dataset()
    np.savez("processed/dataset_elite.npz", X, Y)

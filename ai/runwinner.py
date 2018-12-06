# code reference: https://github.com/GianottiGustavo/neat-flappy/tree/master/FlapPyBio-master
import pickle
import sys

import neat

from ai.app import App


def run_winner(n=1):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config')

    # load Gnome
    genomes = pickle.load(open('winner.pkl', 'rb'))

    for i in range(0, n):
        # Play game and get results
        ai_Bio = App([genomes], config)
        ai_Bio.mainLoop()


def main():
    if len(sys.argv) > 1:
        run_winner(int(sys.argv[1]))
    else:
        run_winner()


if __name__ == "__main__":
    main()

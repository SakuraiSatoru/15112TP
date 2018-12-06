# code reference: https://github.com/GianottiGustavo/neat-flappy/tree/master/FlapPyBio-master
import pickle
import sys

import neat

import ai.app
import ai.sprites


# Driver for NEAT solution to FlapPyBird
def evolutionary_driver(n=50):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config')

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))

    # Run until we achive n.
    winner = p.run(eval_genomes, n=n)

    # dump
    pickle.dump(winner, open('winner.pkl', 'wb'))


def eval_genomes(genomes, config):
    # Play game and get results
    idx, genomes = zip(*genomes)
    player_Bio = ai.app.App(genomes, config)
    player_Bio.mainLoop()
    results = player_Bio.crashInfo
    print("crashinfo:", results)

    # Calculate fitness and top score
    top_score = 0
    for result, genomes in results:
        fitness = result
        genomes.fitness = -1 if fitness == 0 else fitness
        print("fitness:", genomes.fitness)
        if top_score < fitness:
            top_score = fitness

    # print score
    print('The top score was:', top_score)


def main():
    if len(sys.argv) > 1:
        evolutionary_driver(int(sys.argv[1]))
    else:
        evolutionary_driver()


if __name__ == "__main__":
    main()

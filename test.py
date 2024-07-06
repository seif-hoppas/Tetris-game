import GeneticAlgorithm as ga
import Ai_Tetris as ai



def test(Best_weights, ITERATIONS = 600 ):
    chromosome = ga.TetrisIndividual(Best_weights)
    score = ai.run_game(chromosome, 99999999, 60000000000000000, True)
    print("Test Final score: ", score)

if __name__ == "__main__":
    test()
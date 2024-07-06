import numpy as np
import GeneticAlgorithm as ga
import Ai_Tetris as ai
import test as ts
import matplotlib.pyplot as plt
import copy




def train(show_game):
    # Configuration
    generation_num = 10
    pop_num = 12
    Iterations = 10
    child_num = round(pop_num * 0.5)

    # Initialize the initial population
    initial_population = ga.GeneticAlgorithm(pop_num)
    print(initial_population)
    best_chromosomes = []
    best_scores = []

    for it in range(Iterations):
        # Make a copy from initial population so that we can run all experiments with the same initial population
        population = copy.deepcopy(initial_population)
        generations = []

        # Run the generations
        for i in range(generation_num):
            print('===================================')
            print('\n', f'==>Iteration: {it} Number of Generation: {i} ', '\n')
            print('=====================================')

            # Store the current population
            generations.append(copy.deepcopy(population))

            # Selection, crossover, and mutation
            selected_individuals = population.selection(population.chromosomes, child_num)
            new_population = population.crossover(selected_individuals, 0.75)
            new_population = population.mutation(new_population, 0.2)

            # Evaluate the fitness of the new population
            for i in range(child_num):
                chromosome_score = ai.run_game(population.chromosomes[i], 1000, 50000000, show_game)
                new_population[i].calculate_fitness(chromosome_score)

            # Replace the old population with the new one
            population.replace(new_population)

            # Print the fitness scores and the population
            fitness = [individual.fitness for individual in population.chromosomes]
            print(fitness)
            print(population)

            # Find the best two chromosomes and their scores
            sorted_indices = np.argsort(fitness)[::-1]  # Sort in descending order
            best_chromosome_1 = population.chromosomes[sorted_indices[0]]
            best_chromosome_2 = population.chromosomes[sorted_indices[1]]
            best_score_1 = fitness[sorted_indices[0]]
            best_score_2 = fitness[sorted_indices[1]]

            # Store the best chromosomes and scores
            best_chromosomes.append((best_chromosome_1, best_chromosome_2))
            best_scores.append((best_score_1, best_score_2))


    # Print the best chromosomes and scores
    for k in range(len(best_chromosomes)):
        print(f"Generation {k + 1}:\n")
        print(f"Best Chromosome 1: {best_chromosomes[k][0].weights}, Score: {best_scores[k][0]}\n")
        print(f"Best Chromosome 2: {best_chromosomes[k][1].weights}, Score: {best_scores[k][1]}\n")
        print("\n")

    # Plot scores of the best two chromosomes
    plt.figure()
    plt.plot(best_scores, label="Best Chromosomes Scores")
    plt.xlabel("Generation")
    plt.ylabel("Score")
    plt.title("Scores of the Best Chromosomes")
    plt.legend()
    plt.show()

    # Return the best chromosome from all generation and experiments
    return best_chromosomes, best_scores



if __name__ == "__main__":

    best_chromosomes, best_scores = train(True)
    max_weights = []
    max_score = 0

    with open('C:/Users/pc/PycharmProjects/Tetris/INFO.txt', 'a') as fd:
        fd.write("Best Chromosomes and Scores:\n")
        for i, (chromosome_pair, score_pair) in enumerate(zip(best_chromosomes, best_scores)):
            fd.write(f"Generation {i + 1}:\n")
            fd.write(f"Best Chromosome 1: {chromosome_pair[0].weights}, Score: {score_pair[0]}\n")
            print((f"Best Chromosome 1: {chromosome_pair[0].weights}, Score: {score_pair[0]}\n"))
            if max_score < score_pair[0]:
                max_score = score_pair[0]
                max_weights = chromosome_pair[0].weights

            fd.write(f"Best Chromosome 2: {chromosome_pair[1].weights}, Score: {score_pair[1]}\n")
        fd.write("\n")
    print("Max Weights of all time: ",max_weights)


    print("========> Test <========")

    Optimal_weights = max_weights
    ts.test(Optimal_weights,600)









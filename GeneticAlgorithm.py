import random
import numpy as np
import tetris_base as base
import Ai_Tetris as ai
random.seed(42)


class TetrisIndividual():
    def __init__(self, weights):
        # Initialize Tetris individual with weights and fitness score
        self.weights = weights
        self.fitness = 0

    def calculate_fitness(self, score):
        # Calculate fitness score based on game score
        self.fitness = score

    def calculate_best_move(self, board, piece,show_game = False):
        # Calculate the best move for the Tetris piece based on the current board state
        best_x = 0
        best_Y     = 0
        best_rotation = 0
        best_score = 1000000000000

        # Calculate the total number of holes and blocks above holes before making a move
        num_holes_before, num_blocking_blocks_before = base.calc_initial_move_info(board)
        for rotation in range(len(base.PIECES[piece['shape']])):
            # Iterate through each possible rotation
            for x in range(-2, base.BOARDWIDTH - 2):
                # Iterate through each possible position
                move_info = base.calc_move_info(board, piece, x, rotation, num_holes_before, num_blocking_blocks_before)
                # Check if the movement is valid
                if (move_info[0]):
                    # Calculate the score for the movement
                    move_score = 0
                    for i in range(1, len(move_info)):
                        move_score += self.weights[i - 1] * move_info[i]

                    # Update the best movement if the score is higher
                    if (move_score > best_score):
                        best_score = move_score
                        best_x = x
                        best_rotation = rotation


        # Update the piece's position and rotation for the best move
        piece['y'] = -2
        piece['x'] = best_x
        piece['rotation'] = best_rotation

class GeneticAlgorithm:
    def __init__ (self, population_size, num_parameters=9):
        # Initialize the genetic algorithm with a population of Tetris individuals
        self.chromosomes = []

        for i in range(population_size):
            # Create Tetris individuals with random weights
            parameters = np.random.uniform(-10, 10, size=(num_parameters))
            individual = TetrisIndividual(parameters)
            self.chromosomes.append(individual)

            # Evaluate the fitness of each individual
            score = ai.run_game(self.chromosomes[i], 1000, 50000000000, False)
            self.chromosomes[i].calculate_fitness(score)

    def __str__(self):
        # Print the weights and fitness scores of each chromosome in the population
        for i, individual in enumerate(self.chromosomes):
            print(f"Chromosome: {i + 1}")
            print(f"Weights: {individual.weights}")
            print(f"Score: {individual.fitness}")

        return ''

    def selection(self, chromosomes, num_selection):
        # Sort chromosomes based on fitness in descending order
        sorted_chromosomes = sorted(chromosomes, key=lambda x: x.fitness, reverse=False)

        # Select the top 50% of chromosomes
        selected_chromosomes = sorted_chromosomes[:num_selection]

        return selected_chromosomes


    def crossover(self, selected_population, crossover_rate):
        # Perform crossover to create offspring from selected individuals
        offspring = []

        for i in range(0, len(selected_population), 2):
            parent1 = selected_population[i]
            parent2 = selected_population[i + 1]

            r = np.random.random()

            if r > crossover_rate:
                m = np.random.randint(1, len(parent1.weights) - 1)
                child1 = TetrisIndividual(np.concatenate((parent1.weights[:m], parent2.weights[:m])))
                child2 = TetrisIndividual(np.concatenate((parent2.weights[:m], parent1.weights[m:])))
                offspring.extend([child1, child2])
            else:
                offspring.extend([parent1, parent2])


    def mutation(self, population, mutation_rate):
        # Perform mutation on the population
        for individual in population:
            for i in range(len(individual.weights)):
                if random.random() < mutation_rate:
                    individual.weights[i] += random.uniform(-1, 1)

        return population

    def replace(self, new_population):
        # Replace the current population with the new population
        new_pop = sorted(self.chromosomes, key=lambda x: x.fitness, reverse=False)
        new_pop[:(len(new_population))] = new_population
        random.shuffle(new_pop)
        self.chromosomes = new_pop

import random

class Chromosome:

    def __init__(self, gc, fitness):
        self.genetic_code = gc
        self.fitness = fitness

    def __str__(self):
        return f'code: {self.genetic_code} = {self.fitness}'


class GeneticAlgorithm:

    def __init__(self, num_of_files, poss_val):
        self.gene_length = num_of_files
        self.possible_values = poss_val

        self.generation_size = 10
        self.reproduction_size = 4
        self.max_iterations = 100
        self.mutation_rate = 0.1
        self.tournament_size = 3

    def calculate_fitness(self, genetic_code):
        fitness_val = 0

        for i in range(self.gene_length):
            fitness_val += (genetic_code[i]['neighbor_ports']/(genetic_code[i]['time_to_send'] * 1.0)) \
                           * (self.gene_length - i)

        return fitness_val

    def init_population(self):
        init_population = []

        for i in range(self.generation_size):
            genetic_code = []
            random_index = random.randrange(self.gene_length)
            genetic_code = self.possible_values[random_index:] + self.possible_values[:random_index]

            fitness = self.calculate_fitness(genetic_code)
            new_chromosome = Chromosome(genetic_code, fitness)
            init_population.append(new_chromosome)

        return init_population

    def selection(self, chromosomes):
        selected = []

        for i in range(self.reproduction_size):
            selected.append(self.tournament_selection(chromosomes))

        return selected

    def tournament_selection(self, chromosomes):
        selected = random.sample(chromosomes, self.tournament_size)

        winner = max(selected, key = lambda x: x.fitness)

        return winner

    def mutate(self, genetic_code):
        random_val = random.random

        if random_val < self.mutation_rate:
            random_i = random.randrange(self.gene_length)
            random_j = random.randrange(self.gene_length)
            while True:
                if random_i != random_j:
                    break
                random_j = random.randrange(self.gene_length)

            tmp = genetic_code[random_i]
            genetic_code[random_i] = genetic_code[random_j]
            genetic_code[random_j] = tmp

        return genetic_code





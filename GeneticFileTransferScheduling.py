import random

class Chromosome:

    def __init__(self, gc, fitness):
        self.genetic_code = gc
        self.fitness = fitness

    def __str__(self):
        return f'code: {self.genetic_code} = {self.fitness}'


class GeneticAlgorithm:

    def __init__(self, num_of_files, poss_val, server_id):
        self.gene_length = num_of_files
        self.possible_values = poss_val
        self.server_id = server_id

        self.generation_size = 10
        self.reproduction_size = 4
        self.max_iterations = 20
        self.mutation_rate = 0.1
        self.tournament_size = 3

    def calculate_fitness(self, genetic_code):
        fitness_val = 0

        for i in range(len(genetic_code)):
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
        # print(f'Server id: {self.server_id}, finished selection\n')
        return selected

    def tournament_selection(self, chromosomes):
        selected = random.sample(chromosomes, self.tournament_size)

        winner = max(selected, key=lambda x: x.fitness)

        return winner

    def mutate(self, genetic_code):
        random_val = random.random()

        if random_val < self.mutation_rate:
            random_i = random.randrange(len(genetic_code))
            random_j = random.randrange(len(genetic_code))
            while True:
                if random_i != random_j:
                    break
                random_j = random.randrange(len(genetic_code))

            tmp = genetic_code[random_i]
            genetic_code[random_i] = genetic_code[random_j]
            genetic_code[random_j] = tmp

        return genetic_code

    def crossover(self, parent1, parent2):
        child = []
        child_p1 = []
        child_p2 = []

        gene_a = int(random.random() * len(parent1))
        gene_b = int(random.random() * len(parent1))

        start_gene = min(gene_a, gene_b)
        end_gene = max(gene_a, gene_b)

        for i in range(start_gene, end_gene):
            child_p1.append(parent1[i])

        child_p2 = [item for item in parent2 if item not in child_p1]

        child = child_p1 + child_p2
        return child

    def create_generation(self, chromosomes):
        generation = []
        generation_size = 0

        while generation_size < self.generation_size:
            [parent1, parent2] = random.sample(chromosomes, 2)
            child1_code = self.crossover(parent1.genetic_code, parent2.genetic_code)

            child1_code = self.mutate(child1_code)

            child1 = Chromosome(child1_code, self.calculate_fitness(child1_code))

            generation.append(child1)

            generation_size += 1

        return generation

    def optimaze(self):
        population = self.init_population()

        for i in range(0, self.max_iterations):
            # print(f'Server id: {self.server_id}, iteratior : {i}')
            selected = self.selection(population)

            population = self.create_generation(selected)

            global_best_chromosome = max(population, key=lambda x: x.fitness)

        return global_best_chromosome.genetic_code
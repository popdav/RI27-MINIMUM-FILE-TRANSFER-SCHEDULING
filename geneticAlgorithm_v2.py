import random

class Chromosome:

    def __init__(self, gc, fitness):
        self.genetic_code = gc
        self.fitness = fitness

    def __str__(self):
        return f'code: {self.genetic_code} = {self.fitness}'


class GeneticAlgorithm:

    def __init__(self, num_of_servers, first_val):
        self.gene_length = num_of_servers
        self.first_val = first_val

        self.generation_size = 100
        self.reproduction_size = 50
        self.max_iterations = 15
        self.mutation_rate = 0.1
        self.tournament_size = 20

    def calculate_fitness(self, genetic_code):
        for i in range(self.gene_length):
            genetic_code[i].my_time = 0

        arr_of_time = []
        for i in range(self.gene_length):
            arr_of_time.append(genetic_code[i].cacl_my_time())

        return max(arr_of_time)

    def init_population(self):
        init_population = []

        for i in range(self.generation_size):
            genetic_code = []

            genetic_code = self.first_val
            random.shuffle(genetic_code)
            for i in range(len(genetic_code)):
                genetic_code[i].index = i

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

        winner = min(selected, key=lambda x: x.fitness)

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
            for i in range(len(genetic_code)):
                genetic_code[i].index = i

        return genetic_code

    def crossover(self, parent1, parent2):
        child = [-1] * len(parent1)

        gene_a = int(random.random() * len(parent1))
        gene_b = int(random.random() * len(parent1))

        start_gene = min(gene_a, gene_b)
        end_gene = max(gene_a, gene_b)

        for i in range(start_gene, end_gene):
            child[i] = parent1[i]

        for i in range(len(child)):
            for j in range(len(parent2)):
                if child[i] == -1 and parent2[j] not in child:
                    child[i] = parent2[j]

        for i in range(len(child)):
            child[i].index = i
        return child

    def create_generation(self, chromosomes):
        generation = []
        generation_size = 0

        # print(f'Server id: {self.server_id}, creating generation')
        while generation_size < self.generation_size:
            [parent1, parent2] = random.sample(chromosomes, 2)
            child1_code = self.crossover(parent1.genetic_code, parent2.genetic_code)

            child1_code = self.mutate(child1_code)

            child1 = Chromosome(child1_code, self.calculate_fitness(child1_code))
            generation.append(child1)

            generation_size += 1
            # print(f'Server id: {self.server_id}, gen size : {generation_size}')
        # print(f'Server id: {self.server_id}, finished creating generation')
        return generation

    def optimaze(self):
        population = self.init_population()

        global_best_chromosome = population[0]
        for i in range(0, self.max_iterations):
            # print(f'Server id: {self.server_id}, iteration : {i}')
            selected = self.selection(population)

            population = self.create_generation(selected)
            global_best_chromosome = min(population, key=lambda x: x.fitness)
            print(global_best_chromosome.fitness)
            # print(f'Server id: {self.server_id}, global best ch: : {global_best_chromosome}')

        return global_best_chromosome.genetic_code
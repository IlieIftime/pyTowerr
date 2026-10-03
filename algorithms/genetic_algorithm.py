import settings
import random # Necessário para gerar valores aleatórios


class GeneticAlgorithm:
    def __init__(self, tower_type):
        self.num_generations = 50
        self.num_genes = 4  # accuracy, cooldown, range, firepower
    # Tamanho da população inicial # 1000 indivíduos (se for possivel aumentar o tamanho da população não especifico no enunciado)
        self.population_size = 1000
        self.tower_type = tower_type
        self.population = self.initialize_population()
        self.current_generation = 0

    def initialize_population(self):
        """
        Initialize the population with random values
        :return: list of lists, each containing the genes for an individual
        """
        # Get ranges for this tower type from settings
        range_min, range_max = settings.TOWER_TYPES[self.tower_type]['range']
        cooldown_min, cooldown_max = settings.TOWER_TYPES[self.tower_type]['cooldown']
        damage_min, damage_max = settings.TOWER_TYPES[self.tower_type]['damage']
        
        # Definir valores minimos e maximos para a accuracy
        accuracy_min, accuracy_max = 0.01, 1.0
        first_population = []
        
        # Começar por gerar uma geração aleatória
        for i in range(self.population_size):
            individual = [random.uniform(accuracy_min, accuracy_max), # Valor aleatório para a accuracy da 1º geracão 
                         random.uniform(cooldown_min, cooldown_max), # Valor aleatório para o cooldown da 1º geracão
                         random.uniform(range_min, range_max), # Valor aleatório para o range da 1º geracão
                         random.uniform(damage_min, damage_max)] # Valor aleatório para o damage da 1º geracão
            first_population.append(individual) # Adicionar os cromossomas com genes aleatórios à população inicial
        
        return first_population # Retorna a população inicial
    
    def fitness_function(self, individual):
        """
        Calculate the fitness score for an individual
        :param individual: list of genes for an individual
        :return: float, the fitness score, between 0 and 1
        """
        
        accuracy, cooldown, range_, damage = individual # O individuo recebe os 4 genes
        accuracy_pontuation = (accuracy - 0.01) / (1.0 - 0.01) * 0.30 # Cálculo da pontuação para a accuracy x importância dada ao gene
        cooldown_pontuation = (2000 - cooldown) / (2000 - 200) * 0.30 # Cálculo da pontuação para o cooldown x importância dada ao gene
        range_pontuation = (range_ - 70) / (90 - 70) * 0.20 # Cálculo da pontuação para o range x importância dada ao gene
        damage_pontuation = (damage - 1) / (2 - 1) * 0.20 # Cálculo da pontuação para o dano x importância dada ao gene
        
        pontuacao_fitness = accuracy_pontuation + cooldown_pontuation + range_pontuation + damage_pontuation # Cálculo da pontuação total do fitness
        
        return pontuacao_fitness # Retorna a pontuação de fitness do individuo
    
    def run_generation(self):
        """
        Run a single generation of the genetic algorithm
        This is where the selection, crossover, and mutation steps are performed
        """
        selected = [] # Lista para guardar os individuos selecionados
        next_generation = [] # Lista para guardar a próxima geração
        tamanho_torneio = 3 # Seleção dos melhores individuos por torneio de tamanho 3 neste caso

        # Asegurar que o tamanho do torneio não é maior que o tamanho da população actual
        if tamanho_torneio > len(self.population):
            tamanho_torneio = len(self.population) #Caso contrário o tamanho do torneio é igual ao tamanho da população
        
        for _ in range(self.population_size):
            torneio = random.sample(self.population, tamanho_torneio) # Colecta aleatória de 3 individuos para o torneio
            melhor_individuo = max(torneio, key=self.fitness_function) # Seleção do melhor individuo do torneio
            selected.append(melhor_individuo) # Adicionar o melhor individuo à lista de selecionados

        for i in range(0, self.population_size, 2):
            parent1, parent2 = selected[i], selected[i + 1] # Seleção dos pais
            child1 = self.crossover(parent1, parent2) # Obtido do crossover dos pais por single-point
            child2 = self.crossover(parent2, parent1) # Obtido do crossover dos pais por single-point
            next_generation.append(self.mutate(child1)) # Adiciona o 1º filho à próxima geração depois de sofrer mutação uniforme
            next_generation.append(self.mutate(child2)) # Adiciona o 2º filho à próxima geração depois de sofrer mutação uniforme
        self.population = next_generation # Atualiza a população para a próxima geração
        
        return selected # Retorna a lista de cromossomas selecionados
    
    def crossover(self, parent1, parent2):
        """
        Perform crossover between two parents to produce a child
        :param parent1: Individual 1 to crossover
        :param parent2: Individual 2 to crossover
        :return: list, the genes of the child (individual)
        """
        ponto_corte = random.randint(1, self.num_genes - 1) # Ponto de corte aleatório num dos genes
        child = parent1[:ponto_corte] + parent2[ponto_corte:] # Criação do 1º filho o seguinte é com inversão desta lógica
        
        return child # Retorna o filho gerado
    
    def mutate(self, individual):
        """
        Perform mutation on an individual
        :param individual: list, the genes of the individual to mutate
        :return: list, the genes of the mutated individual
        """
        gene_mutado = random.randint(0, self.num_genes - 1) # Seleção aleatória de um gene para mutação
        
        if gene_mutado == 0:
            individual[gene_mutado] = random.uniform(0.01, 1.0) # Mutação do gene da accuracy
        elif gene_mutado == 1:
            individual[gene_mutado] = random.uniform(200, 2000) # Mutação do gene do cooldown
        elif gene_mutado == 2:
            individual[gene_mutado] = random.uniform(70, 90) # Mutação do gene do range
        else:
            individual[gene_mutado] = random.uniform(1, 2) # Mutação do gene do dano
        
        return individual # Retorna o individuo mutado    

    def get_best_solution(self, num_solutions=5):
        """
        Get the best solution(s) from the final generation
        :param num_solutions: int, the number of best solutions to return (default is 1). Use 5 for the final solution
        :return: list of lists, the best solution(s) from the final generation. It should return 5 solutions for the 5 towers
        """
        populacao_selecionada = sorted(self.population, key=self.fitness_function, reverse=True) # Ordenação da população pela pontuaçáo de fitness
        best_solutions = populacao_selecionada[:num_solutions] # Seleção dos melhores individuos da população
        best_fitness = [self.fitness_function(individual) for individual in best_solutions] # Cálculo do fitness dos melhores individuos
        
        return best_solutions, best_fitness # Retorna os melhores individuos e a sua pontuação fitness
    
    def get_current_generation(self):
        """
        Get the current generation number
        :return: int, the current generation number
        """
        return self.current_generation # Retorna o número da geração actual

    def run(self):
        """
        Run the genetic algorithm for the specified number of generations.
        It uses the run_generation method to perform the steps for each generation
        """
        for i in range(self.num_generations):
            self.current_generation = i + 1
            self.run_generation()

            best_solutions, best_fitness = self.get_best_solution(1) # Obtenção da melhor solução da população e da sua pontuação de fitness
            fitness_actual = best_fitness[0] # Obtenção da pontuação de fitness da melhor solução obtida
            
            if fitness_actual >= 0.93:
                break # Se a pontuação de fitness for maior ou igual a 0.93 termina o algoritmo 
        
        return self.get_best_solution(5) # Retorna as 5 melhores soluções obtidas disclaimer são 6 torres 1 dos valores vai ser igual a uma das pontuações de fitness obtidas



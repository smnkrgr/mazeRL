from maze import Maze
from tui import Tui
import csv
import random
import numpy as np
import time
import copy
import math


class GeneticAgent:

    def __init__(self, maze, actions, epsilon, population_size, steps, genes_path=None):

        self.maze = maze
        self.maze_dimensions = [len(self.maze.getMaze()), len(self.maze.getMaze()[0]), actions] 
        self.epsilon = epsilon
        self.goal_y, self.goal_x = self.maze.getGoalPosition()

        self.finishing_positions = self.initializeFinishingPositionsAndEndSteps(population_size)
        self.fitness = [0] * population_size
        self.steps = steps
        
        if genes_path is None: self.population = self.initializePopulation(population_size)
        else: self.population = self.readFromCSV(genes_path)

    def initializePopulation(self, size):

        pop = []

        for i in range(size):
            pop.append([random.randrange(100)] * self.steps)

        return pop

    def softmaxDistribution(self):

        distribution = []
        sum_exp_fitness = 0

        for value in self.fitness:
            sum_exp_fitness += math.exp(value)
            
        for genotype_fitness in self.fitness:
            distribution.append(math.exp(genotype_fitness)/sum_exp_fitness) 

        return distribution 

    def distributeGenotype(self, softmax):

        distribution = []
        equal_sized_piece = 1.0/len(self.population)
        i = 0
        
        for value in softmax:
            if value > equal_sized_piece:
                for i in range(int(value/equal_sized_piece)):
                    distribution.append(self.population[i])
            i += 1

        if len(self.population) >= len(distribution):
            for i in range(len(self.population) - len(distribution)):
                distribution.append(self.population[np.argmax(softmax)])
        else:
            print("Check distributeGenotype again you fucking idiot")
            exit()

        return distribution
        
    def crossGenotypes(self, genotype):

        new_population = []
        
        for i in range(len(self.population)):
            parent_a = genotype[i]
            parent_b = random.choice(genotype)
            offspring = []

            crossover_point = random.randint(0, len(parent_a))

            for i in range(len(parent_a)):
                if random.random() < self.epsilon: offspring.append(random.randrange(100))  
                elif i < crossover_point: offspring.append(parent_a[i])
                else: offspring.append(parent_b[i])

            new_population.append(offspring)

        return new_population
                
    def generateNewGeneration(self):

        softmax_fitness = self.softmaxDistribution()
        genotype_distribution = self.distributeGenotype(softmax_fitness)
        self.population = self.crossGenotypes(genotype_distribution)
        
    def simulate(self, games=1):

        average_fitness = []
        
        for game in range(games):

            print("Start Game: ", game)
            individual_number = 0
                                
            for genotype in self.population:
                self.runGameForIndividual(genotype, individual_number)
                individual_number += 1
                
            self.calcFitness()
            average_fitness.append(np.mean(self.fitness))
            print("Finished game with average population fitness: ", average_fitness[-1])

            print("Crossing population for new generation...")
            self.generateNewGeneration()
            
        return average_fitness
    
    def runGameForIndividual(self, genotype, genotype_number):

        status = "OK"
        steps = 0

        for gene in genotype:
            status = self.maze.handleMove((gene % self.maze_dimensions[2]) + 1)
            steps += 1
            if status is "GOAL": break

        if status is "GOAL":
            self.finishing_positions[genotype_number][0] = self.goal_y
            self.finishing_positions[genotype_number][1] = self.goal_x
            self.finishing_positions[genotype_number][2] = steps
        else:
            self.finishing_positions[genotype_number][0] = self.maze.getCurrentPosition()[0]
            self.finishing_positions[genotype_number][1] = self.maze.getCurrentPosition()[1]
            self.finishing_positions[genotype_number][2] = steps
            self.maze.resetMaze()

        return

    def calcFitness(self):

        for i in range(len(self.population)):
            
            # calculate euclidian distance between the finishing position and goal
            distance = math.sqrt((float(self.goal_y) - float(self.finishing_positions[i][0]))**2 +
                           (float(self.goal_x) - float(self.finishing_positions[i][1]))**2)      

            # bonus for reaching the goal to encourage shorter paths
            if distance == 0: 
                bonus = (self.steps - self.finishing_positions[i][2]) / self.steps * 100
                print("Goal reached")
            else: bonus = 0           

            self.fitness[i] = 1.0/(distance + 1) + bonus
            
        return

    def initializeFinishingPositionsAndEndSteps(self, size):

        positions = []

        for i in range(size):
            positions.append([0, 0, 0])

        return positions

    def savePopulationToCSV(self, path):

        with open(path, mode='w') as data_file:
            data_writer = csv.writer(data_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in range(len(self.population)):
                data_writer.writerow(self.population[i])

    def readPopulationFromCSV(self, path):

        population = []
        
        with open(path) as data_file:
            data_reader = csv.reader(data_file, delimiter=',')

            for row in data_reader:
                population.append(row)

        for genotype in population:
            genotype = int(genotype)
        
        return population


if __name__ == "__main__":

    maze = Maze("maze_levels/maze.txt")
    geneAgent = GeneticAgent(maze=maze, actions=4, epsilon=0.05, population_size=300, steps=1000)
    geneAgent.simulate(games=1000)


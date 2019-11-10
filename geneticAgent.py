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
            genotype = []
            for j in range(self.steps):
                genotype.append(random.randrange(100))
            pop.append(genotype)

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
            if value >= equal_sized_piece:
                for j in range(int(value/equal_sized_piece)):
                    distribution.append(self.population[i])
            i += 1

        if len(self.population) >= len(distribution):
            for i in range(len(self.population) - len(distribution)):
                distribution.append(self.population[np.argmax(softmax)])
        #else:
        #    print("Check distributeGenotype again you fucking idiot")
        #    exit()

        return distribution
        
    def crossGenotypes(self, genotype, avg_steps):

        new_population = []
        avg_corssover_point_list = []
        
        for i in range(len(self.population)):
            parent_a = genotype[i]
            parent_b = random.choice(genotype)
            offspring = []

            crossover_point = np.random.normal(loc=avg_steps/2, scale=avg_steps/6)
            #crossover_point = random.randint(0, len(parent_a))
            avg_corssover_point_list.append(crossover_point)
            
            for i in range(len(parent_a)):
                #if random.random() < self.epsilon: offspring.append(random.randrange(100))  
                if i < crossover_point: offspring.append(parent_a[i])
                else: offspring.append(parent_b[i])
            offspring[random.randrange(self.steps)] = random.randrange(100)
            new_population.append(offspring)

        avg_corssover_point = np.mean(avg_corssover_point_list)
        print("Average crossover_point: ", avg_corssover_point)
        return new_population
                
    def generateNewGeneration(self, avg_steps):

        softmax_fitness = self.softmaxDistribution()
        genotype_distribution = self.distributeGenotype(softmax_fitness)
        self.population = self.crossGenotypes(genotype_distribution, avg_steps)
        
    def simulate(self, games=1):

        average_fitness = []
        
        for game in range(games):

            print("Start Game: ", game)
            individual_number = 0
            avg_steps_list = []
                                
            for genotype in self.population:
                avg_steps_list.append(self.runGameForIndividual(genotype, individual_number))
                individual_number += 1
                
            avg_steps = np.mean(avg_steps_list)
            print("Average step size: ", avg_steps)
            self.calcFitness()
            average_fitness.append(np.mean(self.fitness))
            print("Finished game with average population fitness: ", average_fitness[-1])

            print("Crossing population for new generation...")
            self.generateNewGeneration(avg_steps)
            
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
        
        return steps
 
    def calcFitness(self):

        for i in range(len(self.population)):
            
            # calculate euclidian distance between the finishing position and goal
            distance = math.sqrt((float(self.goal_y) - float(self.finishing_positions[i][0]))**2 +
                           (float(self.goal_x) - float(self.finishing_positions[i][1]))**2)      

            # bonus for reaching the goal to encourage shorter paths
            if distance == 0: 
                bonus = (self.steps - self.finishing_positions[i][2]) / self.steps * 700
            else: bonus = -100           

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

    def demonstrate(self):

        status = "OK"
        tui = Tui()
        best_genotype = self.population[np.argmax(self.fitness)]
        counter = 0
        
        while status != "GOAL":
            y, x = self.maze.getCurrentPosition()
            tui.draw(self.maze.getMaze(), y, x)
            status = self.maze.handleMove((best_genotype[counter] % self.maze_dimensions[2]) + 1 )
            counter += 1
            if counter >= self.steps:
                break

if __name__ == "__main__":

    maze = Maze("maze_levels/maze.txt")
    geneAgent = GeneticAgent(maze=maze, actions=4, epsilon=0.05, population_size=1000, steps=1500)
    geneAgent.simulate(games=500)
    geneAgent.demonstrate()

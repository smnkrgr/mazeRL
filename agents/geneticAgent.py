from maze import Maze
from tui import Tui
import csv
import random
import numpy as np
import time


class GeneticAgent:

    def __init__(self, maze, actions, epsilon, population_size, steps, genes_path = None):

        self.maze = maze
        self.maze_dimensions = [len(self.maze.getMaze()), len(self.maze.getMaze()[0]), actions] 
        self.epsilon = epsilon
        self.goal_y, self.goal_x = self.maze.getGoalPosition()

        self.finishing_positions = self.initializeFinishingPositions(population_size)
        self.fitness = [0] * population_size
        self.steps = steps
        
        if genes_path == None: self.population = self.initializePopulation(population_size)
        else: self.population = self.readFromCSV(genes_path)

    def initializePopulation(self, size):

        pop = []

        for i in range(size):
            pop.append([random.randrange(100)] * self.steps)

        return pop

    def calcFitness(self):

        for i in range(len(self.population)):
            
            # calculate euclidian distance between the finishing position and goal
            distance = sqrt((self.goal_y - self.finishing_positions[i][0])^2 +
                           (self.goal_x - self.finishing_positions[i][1])^2)      

            # bonus for reaching the goal to encourage shorter paths
            if distance == 0: bonus = self.steps - self.finishing_positions[i][2]
            else: bonus = 0
            
            self.fitness[i] = 1.0/(distance + 1) + bonus
            
        return

    def initializeFinishingPositionsAndEndSteps(self, size):

        positions = []

        for i in range(size):
            positions.append([0,0,0])

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

    
                
         

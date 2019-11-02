from maze import Maze
from tui import Tui
import csv
import random
import numpy as np

class Agent:

    def __init__(self, maze, actions, epsilon, q_path = None, n_path = None):

        self.maze = maze
        self.Q_dimensions = [len(self.maze.getMaze()), len(self.maze.getMaze()[0]), actions] 
        self.epsilon = epsilon
        
        if q_path == None: self.Q = self.initializeFieldActionArray(0.0)
        else: self.Q = self.readFromCSV(q_path)
        
        if n_path == None: self.N = self.initializeFieldActionArray(0)
        else: self.N = self.readFromCSV(n_path)

    def simulate(self, games = 1):

        for i in range(games):
            status = "OK"
            executed_actions = []

            while status != "GOAL":
                pos_y, pos_x = self.maze.getCurrentPosition()
                action = self.chooseAction(pos_y, pos_x)
                
                status = self.maze.handleMove(action)
                executed_actions.append([pos_y, pos_x, action])

                self.N[pos_y][pos_x][action-1] += 1
                self.Q[pos_y][pos_x][action-1] += ((self.calcReward(status) - self.Q[pos_y][pos_x][action-1])
                                                   * (1.0 / self.N[pos_y][pos_x][action-1]))

            average_reward = 1.0 / len(executed_actions)
            for i in range(len(executed_actions)):
                y, x, action = executed_actions[i]
                self.Q[y][x][action-1] += average_reward

    def demonstrate(self):

        status = "OK"
        tui = Tui()

        while status != "GOAL":
            y, x = self.maze.getCurrentPosition()
            tui.draw(self.maze.getMaze(), y, x)
            status = self.maze.handleMove(self.chooseAction(y, x))

    def calcReward(self, status):

        if status == "OK": return 0
        elif status == "WALL": return -1
        elif status == "GOAL": return 1
        
    def chooseAction(self, y, x):

        if random.random() < self.epsilon:
            return random.randrange(4) + 1
        else:
            argmax = []
            argmax.append(np.argmax(self.Q[y][x]))
            for i in range(self.Q_dimensions[2]):
                if argmax[0] != i and self.Q[y][x][argmax[0]] == self.Q[y][x][i]:
                    argmax.append(i)
            return random.choice(argmax) + 1
            
    def initializeFieldActionArray(self, value):

        Q = []
        
        for i in range(self.Q_dimensions[0]):
            row = []
            for j in range(self.Q_dimensions[1]):
                row.append([value] * self.Q_dimensions[2])
            Q.append(row)

        return Q
        
    def saveQtoCSV(self, path):

        with open(path, mode='w') as data_file:
            data_writer = csv.writer(data_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in range(self.Q_dimensions[0]):
                for j in range(self.Q_dimensions[1]):
                    data_writer.writerow(self.Q[i][j])

    def readFromCSV(self, path):

        Q = []

        with open(path) as data_file:
            data_reader = csv.reader(data_file, delimiter=',')
            rows = []
            for row in data_reader:
                rows.append(row)
                
            for i in range(self.Q_dimensions[0]):
                row = []
                for j in range(self.Q_dimensions[1]):
                    row.append(rows[(i * self.Q_dimensions[0]) + j])
                Q.append(row)

        return Q


if __name__ == '__main__':

    maze = Maze("maze.txt")
    agent = Agent(maze, 4, 0.1)
    #agent.simulate(10)
    agent.demonstrate()
    

            

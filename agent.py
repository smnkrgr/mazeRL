from maze import Maze
from tui import Tui
import csv
import random
import numpy as np
import time

class Agent:

    def __init__(self, maze, actions, epsilon, alpha, discount, q_path = None, n_path = None):
        
        self.maze = maze
        self.Q_dimensions = [len(self.maze.getMaze()), len(self.maze.getMaze()[0]), actions] 
        self.epsilon = epsilon
        self.alpha = alpha
        self.discount = discount
        
        if q_path == None: self.Q = self.initializeFieldActionArray(1.0)
        else: self.Q = self.readFromCSV(q_path)
        
        if n_path == None: self.N = self.initializeFieldActionArray(0)
        else: self.N = self.readFromCSV(n_path)

    def simulate(self, games = 1):

        game_count = 1
        for i in range(games):
            status = "OK"
            #executed_actions = []
            count = 0
            print("Start Game: ", game_count)
            while status != "GOAL":
                pos_y, pos_x = self.maze.getCurrentPosition()
                action = self.chooseAction(pos_y, pos_x)
                
                status = self.maze.handleMove(action)
                #executed_actions.append([pos_y, pos_x, action])
                count += 1
                if (count%100000 == 0):
                    print("X: ", pos_x, "Y: " , pos_y,"Game No.: " , game_count , "Current step count: " , count)
                #self.N[pos_y][pos_x][action-1] += 1
                #self.Q[pos_y][pos_x][action-1] += ((self.calcReward(status) - self.Q[pos_y][pos_x][action-1])
                #                                   * (1.0 / self.N[pos_y][pos_x][action-1]))
                self.calcNewQ(status, action, pos_y, pos_x)
                
            print("Finished Game: ", game_count)
            game_count += 1
            #average_reward = 1.0 / len(executed_actions)
            #for i in range(len(executed_actions)):
            #    y, x, action = executed_actions[i]
            #    self.Q[y][x][action-1] += average_reward

    def demonstrate(self):

        status = "OK"
        tui = Tui()

        while status != "GOAL":
            y, x = self.maze.getCurrentPosition()
            tui.draw(self.maze.getMaze(), y, x)
            status = self.maze.handleMove(self.chooseAction(y, x, explore=False))
            
    def calcReward(self, status):

        if status == "OK": return 0
        elif status == "WALL": return -1
        elif status == "GOAL": return 100

    def calcNewQ(self, status, action, pos_y, pos_x):
    
        current_y,current_x = self.maze.getCurrentPosition()
        highestScoreNextStep = self.Q[current_y][current_x][self.chooseAction(current_y, current_x, explore=False) - 1]
        
        self.Q[pos_y][pos_x][action-1] = (1-self.alpha) * self.Q[pos_y][pos_x][action-1] + self.alpha  * ( self.calcReward(status) + self.discount * highestScoreNextStep)
        

    def chooseAction(self, y, x, explore = True):
        
        if explore and random.random() < self.epsilon:
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
                
            for row in rows:
                #TODO range() to #actions
                for i in range(4):
                    row[i] = float(row[i])
                
            for i in range(self.Q_dimensions[0]):
                row = []
                for j in range(self.Q_dimensions[1]):
                    row.append(rows[(i * self.Q_dimensions[1]) + j])
                Q.append(row)

        return Q


if __name__ == '__main__':

    games = 50
    epsilon = 0.1
    alpha = 0.5
    discount = 1
    maze = Maze("maze.txt")
    agent = Agent(maze, 4, epsilon, alpha, discount, "test")
    currentTime = time.time()
    #agent.simulate(games)
    print("Time to finish ", games, " games in min.: ", (time.time() - currentTime)/60 )
    agent.demonstrate()
    #agent.saveQtoCSV("test")

            

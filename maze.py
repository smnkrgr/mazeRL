
class Maze:

    starting_position_char = "Y"
    goal_position_char = "X"
    
    def __init__(self, path):

        self.maze = self.readMaze(path)
        self.start_y, self.start_x = self.setStartingPosition()
        self.current_position_y = self.start_y
        self.current_position_x = self.start_x
        self.goal_position = self.setGoalPosition()

    def handleMove(self, move):

        status = "OK"
        
        if move == 1: move = "LEFT"
        elif move == 2: move = "DOWN"
        elif move == 3: move = "UP"
        else: move = "RIGHT"
        
        if move == "UP" and self.checkLegalMove(self.current_position_y - 1, self.current_position_x):
            self.current_position_y = self.current_position_y - 1 
        elif move == "DOWN" and self.checkLegalMove(self.current_position_y + 1, self.current_position_x):
            self.current_position_y = self.current_position_y + 1
        elif move == "LEFT" and self.checkLegalMove(self.current_position_y, self.current_position_x - 1):  
            self.current_position_x = self.current_position_x - 1
        elif move == "RIGHT" and self.checkLegalMove(self.current_position_y, self.current_position_x + 1):  
            self.current_position_x = self.current_position_x + 1
        else:
            status = "WALL"
            
        if self.current_position_y == self.goal_position[0] and self.current_position_x == self.goal_position[1]:
            status = "GOAL"
            self.resetMaze()
            
        return status

    def checkLegalMove(self, pos_y, pos_x):

        
        if pos_y >= len(self.maze): return False
        if pos_x > len(self.maze[0]): return False

        if self.maze[pos_y][pos_x] == " ":
            return True
        elif self.maze[pos_y][pos_x] == self.starting_position_char:
            return True
        elif self.maze[pos_y][pos_x] == self.goal_position_char:
            return True
        else: return False

    def readMaze(self, path):

        maze = []
        mazeFile = open(path, "r")
        columns = mazeFile.readlines()

        for column in columns:
            column = column.strip()
            row = [i for i in column]
            maze.append(row)
        return maze

    def getPositionOf(self, char):

        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                if self.maze[i][j] == char:
                    return i, j

    def resetMaze(self):

        self.current_position_y = self.start_y
        self.current_position_x = self.start_x
        return

    def setStartingPosition(self):

        return self.getPositionOf(self.starting_position_char)

    def setGoalPosition(self):

        return self.getPositionOf(self.goal_position_char)

    def getMaze(self):

        return self.maze

    def getCurrentPosition(self):

        return self.current_position_y, self.current_position_x

    def getGoalPosition(self):

        return self.goal_position

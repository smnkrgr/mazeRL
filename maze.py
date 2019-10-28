

class Maze:

    starting_position_char = "Y"
    goal_position_char = "X"
    
    def __init__(self, path):

        self.maze = self.readMaze(path)
        self.current_position_y, self.current_position_x = self.setStartingPosition()
        self.goal_position = self.setGoalPosition()

    def handleMove(self, move):

        status = "OK"

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
        return status

    def checkLegalMove(self, pos_y, pos_x):

        if pos_y > len(self.maze[0]): return False
        if pos_x > len(self.maze): return False
        
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


if __name__ == "__main__":
    
    maze = Maze("maze.txt")

    mazerep = maze.getMaze()

    for i in mazerep:
        print("".join(i))

    print len(mazerep)
    print len(mazerep[0])
    print maze.getCurrentPosition()
    print maze.handleMove("UP")
    print maze.getCurrentPosition()
    print maze.handleMove("RIGHT")
    print maze.getCurrentPosition()
    print maze.handleMove("RIGHT")
    print maze.getCurrentPosition()
    print maze.getGoalPosition()

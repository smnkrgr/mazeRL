from maze import Maze
from tui import Tui

if __name__ == "__main__":

    maze = Maze("maze.txt")
    tui = Tui()
    status = "OK"

    while status != "GOAL":
        pos_y, pos_x = maze.getCurrentPosition()
        tui.draw(maze.getMaze(), pos_y, pos_x)
        status = maze.handleMove(tui.recieveInput())

    print("finished")
    

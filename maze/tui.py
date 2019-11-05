import os

class Tui:

    def __init__(self):

        return

    def draw(self, field, player_pos_y, player_pos_x):

        field[player_pos_y][player_pos_x] = "O"
        os.system("clear")

        for i in field:
            print("".join(i)) 

        field[player_pos_y][player_pos_x] = " "

        return

    def recieveInput(self):

        print("1 = left, 2 = down, 3 = up and 4 = right. Waiting for input:")
        try:
            player_input = input()
        except:
            player_input = 5
        
        if player_input == 1: return "LEFT"
        elif player_input == 2: return "DOWN"
        elif player_input == 3: return "UP"
        elif player_input == 4: return "RIGHT"
        else:
            print("Wrong Input; try again")
            return self.recieveInput()
        


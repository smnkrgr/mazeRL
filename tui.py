import os
import pygame as pg
import time

class Tui:

    def __init__(self):

        self.drawIntroScreen()
        self.slap = pg.mixer.Sound("sounds/slap4.wav")
        return

    def draw(self, field, player_pos_y, player_pos_x):

        time.sleep(0.02)
        pg.mixer.set_num_channels(50)
        field[player_pos_y][player_pos_x] = "O"
        os.system("clear")
#       self.slap.play()
        for i in field:
            print("".join(i)) 

        field[player_pos_y][player_pos_x] = " "

        return

    def drawIntroScreen(self):

        pg.mixer.init()
        pg.init()

        beatme = pg.mixer.Sound("sounds/beatme123.wav")
        fuckyou = pg.mixer.Sound("sounds/Fuck you.wav")

        pg.mixer.set_num_channels(20)
        
        os.system("clear")

        introscreen = """@@@#(/**,. ,******. .(###(/////(###(///(###(((#,.       
            @@@#/***,. .,,,,,,. /(###(/(%@@@@@@#///(((((/(#,.      
            @&%(/***,. ,******, .#&&&%(@@@@@@@@@@#((((((((#,.      
            &&%#**//*, ... ....  (###((@#%&@@&@@@(((((/(((#*.      
            &%%/*,***,         . (####(/.    .%@@///(((((#((/.     
            &%%(**,,*,       ....(###((    .. /(////((((##(##*,..  
            %%%(,,,,,*         ..(###((... . .///////(((#(((#,,,.  
            %%%(*,,,,*       ....(###(,#. .../((///(((((##((#*,,.  
            #%%#**,,,*       ....  .   **#/(%@#(/(((((((##((#*,,.  
            #&%#**,,,,              */  .,.((/*/(/(((((#(#((#*,,   
            (&%#*,,,,,            .   #/ ..,*((&@,/((#####(#(*,    
            #&%#**,,,*     .           ..#. .#(%((**((####(((*.    
           .(&&%**,,,*.     .   ,        ##.&&*.,/*,*(#####((**,   
           ./@&%**,,,,.  .     .,        ./, ...,/#//(#######/**,,.
           .,@&%**,,,,.  .     (**,,,. ..#,/...,/(%*/#######(/**,,,
           .,@&%**,,,,....     %/(#( ./(/ /&@%(#%@/*/####%###/**,,,
           .,@&%/*,,,,.       ,/.        ..*(###/,/#%##%###/****,  
           ..@&%/*,,,,..   ...,/.           *(#%#%/,,(%##%###/*****
          ...@&%/**,,,..    ..*/,.         ,*((%#%/,,/(##%%##/*****
          .,.@&%/*,,,*,.    .,*,,          ./#(%%%(*,.*##%%%#(*****
          ,,,@&%/*,,**,.   ..,*,#.         .(((&@%#,. .#%%%%#(/.,**
          ,,.&&%/*,,,,*%%//@.**/%%%%%(..& ,*(#@@@%#.  ,%%%%%%(/.,**
         .,,.#&%(*,,,,*%%(#&.*/(&###%%%(#%@@@@@%#...*%%%%%%#/..**  
         .,,.#@%(*,,,,*#%#%*.**(@%((%%%%%#%&@@@@@&&%,%@%%%%%%#(*.**"""

        beatme.play()

        print(introscreen)
        print("         B U D D Y I T H I N K Y O U G O T T H E W R O N G D O O R")

        time.sleep(3)

        fuckyou.play()
        os.system("clear")

        time.sleep(1)
        
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
        


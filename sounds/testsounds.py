import pygame as pg
import time

pg.mixer.init()
pg.init()

a1Note = pg.mixer.Sound("slap7.wav")
a2Note = pg.mixer.Sound("Take it boy.wav")

pg.mixer.set_num_channels(50)

for i in range(25):
    a1Note.play()
    time.sleep(0.03)
    a2Note.play()
    time.sleep(0.03)

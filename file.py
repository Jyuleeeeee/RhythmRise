import pygame, sys, math, time, os
from pygame.locals import *

pygame.init()

class Note:
    def __init__(self, x, y, size_x, size_y, speed):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.speed = speed

m1_h_notes = []
with open('music1_hard.txt', 'r') as inFile:
    text = inFile.readlines()
for i in range(0, len(text)):
    m1_h_notes.append(list(map(str, text[i].split())))

for i in range(0, len(m1_h_notes)):
    print(f"{m1_h_notes[i]}")

note_line = []
if len(m1_h_notes) > 0:
    line = m1_h_notes.pop(0)



print(line)
print(line[0][0])
print(f"{note_line}")
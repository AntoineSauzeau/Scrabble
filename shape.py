from enum import IntEnum
import pygame

class ShapeType:
    Rectangle = 0,
    Line = 1

''' Cette classe a vocation à rajouter des fonctions aux
    formes de base de pygame '''
class Shape:

    def __init__(self):
        pass;

    def new_rectangle(self, surface, color, rect, width=0):
        self.type = ShapeType.Rectangle;
        self.surface = surface;
        self.color = color;
        self.rect = rect;
        self.width = width;

    def new_line(self, surface, color, start_pos, end_pos, width=1):
        self.type = ShapeType.Line;
        self.surface = surface;
        self.start_pos = start_pos;
        self.end_pos = end_pos;
        self.width = width;

    def draw(self):

        if(self.type == ShapeType.Rectangle):
            pygame.draw.rect(self.surface, self.color, self.rect, self.width);

        elif(self.type == ShapeType.Line):
            pygame.draw.line(self.surface, self.start_pos, self.end_pos, self.width);

    def in_bounds(self, x, y):

        if(self.type == ShapeType.Rectangle):

            x_min = self.rect[0];
            y_min = self.rect[1];
            x_max = x_min + self.rect[2];
            y_max = y_min + self.rect[3];

            return (x_max >= x and x >= x_min and y_max >= y and y >= y_min);

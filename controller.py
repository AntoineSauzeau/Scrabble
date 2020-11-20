from interface import Interface
import pygame
from pygame.locals import *
import time


class Controller():

    def __init__(self):
        print("Constructor Controller");

    def start_loop(self):

        self.exit = False;

        while(not(self.exit)):

            for event in pygame.event.get():

                if(event.type == pygame.QUIT):
                    return;

                self.interface.event(event);


    def create_interface(self):
        self.interface = Interface(self);

    def quit(self):
        print("Fin du programme.")
        self.exit = True;

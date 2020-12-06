from interface import Interface
import pygame
from pygame.locals import *
import time
import threading


class Controller():

    FPS = 160

    def __init__(self):

        print("Constructor Controller");

        self.exit = False;


    def start_loop(self):

        clock = pygame.time.Clock();
        while(not(self.exit)):

            for event in pygame.event.get():

                if(event.type == pygame.QUIT):
                    return;

                self.interface.event(event);

            self.interface.draw();

            clock.tick(self.FPS);



    def create_interface(self):
        self.interface = Interface(self);

    def quit(self):
        print("Fin du programme.")
        self.exit = True;

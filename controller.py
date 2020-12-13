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

            try:
                for event in pygame.event.get():

                    self.interface.event(event);

                self.interface.draw();

            except:

                #En cas de crash du programme on sauvegarde la partie si une partie était en cours
                game_interface = self.interface.get_game_interface();
                if(game_interface != None):

                    game = game_interface.get_game_instance();
                    if(game != None):
                        game.create_save();

            clock.tick(self.FPS);



    def create_interface(self):
        self.interface = Interface(self);

    def quit(self):

        game_interface = self.interface.get_game_interface();
        if(game_interface != None):
            game_instance = game_interface.get_game_instance();
            game_instance.stop_timer();


        print("Fin du programme.")
        self.exit = True;

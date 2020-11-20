#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import time
from enum import IntEnum
import os
from button import Button
from game import Game
from player import Player

class Page(IntEnum):
    MainMenu = 0,
    TurnByTurnMenu = 1

class MenuInterface():

    #Fonctions init
    def __init__(self, interface):
        print('Constructor Menu');

        self.interface = interface;
        self.page = Page.MainMenu;

        self.l_button_by_page = [[]];

        self.load_images();

        self.init_main_menu();
        self.init_turn_by_turn_menu();



    def init_main_menu(self):

        interface_width = self.interface.MENU_WINDOW_WIDTH;
        interface_height = self.interface.MENU_WINDOW_HEIGHT;

        bttn_play_mode_turn = Button("Jouer chacun son tour");
        bttn_play_mode_turn.set_text_size(35);
        bttn_play_mode_turn.set_color((0, 0, 0));
        bttn_play_mode_turn.set_pos((interface_width/2, 275));
        bttn_play_mode_turn.set_padding(20);

        bttn_play_mode_bot = Button("Jouer contre un bot");
        bttn_play_mode_bot.set_text_size(35);
        bttn_play_mode_bot.set_color((0, 0, 0));
        bttn_play_mode_bot.set_pos((interface_width/2, 335));
        bttn_play_mode_bot.set_padding(20);

        bttn_stats = Button("Statistiques");
        bttn_stats.set_text_size(35);
        bttn_stats.set_color((0, 0, 0));
        bttn_stats.set_pos((interface_width/2, 395));
        bttn_stats.set_padding(20);

        bttn_settings = Button("Paramètres");
        bttn_settings.set_text_size(35);
        bttn_settings.set_color((0, 0, 0));
        bttn_settings.set_pos((interface_width/2, 455));
        bttn_settings.set_padding(20);

        bttn_quit = Button("Quitter");
        bttn_quit.set_text_size(35);
        bttn_quit.set_color((0, 0, 0));
        bttn_quit.set_pos((interface_width/2, 555));
        bttn_quit.set_padding(20);

        page=0    #Index de la page du menu principale
        self.l_button_by_page[page].append(bttn_play_mode_turn);
        self.l_button_by_page[page].append(bttn_play_mode_bot);
        self.l_button_by_page[page].append(bttn_stats);
        self.l_button_by_page[page].append(bttn_settings);
        self.l_button_by_page[page].append(bttn_quit);

    def init_turn_by_turn_menu(self):
        pass;




    #Fonctions draw
    def draw(self, window):
        print("Draw Menu");

        self.l_drawed_button = [];

        if(self.page == Page.MainMenu):
            self.draw_main_menu(window);
        elif(self.page == Page.TurnByTurnMenu):
            self.draw_turn_by_turn_menu(window);

        pygame.display.flip();

    def draw_main_menu(self, window):

        interface_width = self.interface.MENU_WINDOW_WIDTH;
        interface_height = self.interface.MENU_WINDOW_HEIGHT;

        background_rect = (0, 0, interface_width, interface_height);
        pygame.draw.rect(window, (255, 255, 255), background_rect);

        window.blit(self.img_scrabble_title, (0, 0));

        i_page=int(Page.MainMenu)
        for button in self.l_button_by_page[i_page]:
            button.draw(window);

    def draw_turn_by_turn_menu(self, window):
        pass;




    def load_images(self):

        #On charge les images une seule fois pour éviter de perdre du temps à chaque fois
        self.img_scrabble_title = pygame.image.load(os.path.join("Images", "Scrabble_title.png"));



    #Fonctions event
    def event(self, e):

        i_page = int(self.page);

        if(e.type == pygame.MOUSEMOTION):

            for button in self.l_button_by_page[i_page]:

                mouse_x = e.pos[0];
                mouse_y = e.pos[1];

                if(button.in_bounds(mouse_x, mouse_y)):
                    button.highlight(0, (23, 192, 187));
                else:
                    button.remove_highlighting();

            self.interface.draw();

        elif(e.type == pygame.MOUSEBUTTONUP):

            for button in self.l_button_by_page[i_page]:

                mouse_x = e.pos[0];
                mouse_y = e.pos[1];

                if(button.in_bounds(mouse_x, mouse_y)):
                    if(button.get_text() == "Quitter"):
                        controller = self.interface.get_controller();
                        controller.quit();
                    elif(button.get_text() == "Jouer chacun son tour"):

                        game = Game([Player("Antoine"), Player("Alexandre")]);
                        self.interface.create_game_interface(game);
                        self.interface.change_page(1);




    def change_page(page):

        self.page = page;
        self.draw();

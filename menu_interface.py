#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import time
from enum import IntEnum
import os
from button import Button
from game import Game
from player import Player
from text_edit_box import TextEditBox
from text_switch_widget import TextSwitchWidget

class Page(IntEnum):
    MainMenu = 0,
    GameMenu = 1,
    SaveMenu = 2

class MenuInterface():

    #Fonctions init
    def __init__(self, interface):
        print('Constructor Menu');

        self.interface = interface;
        self.page = Page.MainMenu;

        self.l_button_by_page = [[], []];
        self.l_tew_by_page = [[], []];       #TextEditBox
        self.l_tsw_by_page = [[], []];       #TextSwitchWidget

        self.load_images();

        self.init_main_menu();
        self.init_game_menu();



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

        page=0;    #Index de la page du menu principale
        self.l_button_by_page[page].append(bttn_play_mode_turn);
        self.l_button_by_page[page].append(bttn_play_mode_bot);
        self.l_button_by_page[page].append(bttn_stats);
        self.l_button_by_page[page].append(bttn_settings);
        self.l_button_by_page[page].append(bttn_quit);

    def init_game_menu(self):

        interface_width = self.interface.MENU_WINDOW_WIDTH;
        interface_height = self.interface.MENU_WINDOW_HEIGHT;

        page = 1;

        tew_name_player_1 = TextEditBox();
        tew_name_player_1.set_pos((15, 100));

        tew_name_player_2 = TextEditBox();
        tew_name_player_2.set_pos((15, 170));

        tew_name_player_3 = TextEditBox();
        tew_name_player_3.set_pos((15, 240));

        tew_name_player_4 = TextEditBox();
        tew_name_player_4.set_pos((15, 310));

        self.l_tew_by_page[page].append(tew_name_player_1);
        self.l_tew_by_page[page].append(tew_name_player_2);
        self.l_tew_by_page[page].append(tew_name_player_3);
        self.l_tew_by_page[page].append(tew_name_player_4);


        tsw_n_bot = TextSwitchWidget();
        tsw_n_bot.set_pos(interface_width/2, 447);
        tsw_n_bot.set_l_value(["0", "1", "2", "3"]);
        tsw_n_bot.set_text_size(16);

        self.l_tsw_by_page[page].append(tsw_n_bot);


        bttn_start_game = Button("Lancer la partie");
        bttn_start_game.set_text_size(27);
        bttn_start_game.set_pos((interface_width-105, interface_height-35));
        bttn_start_game.set_border(True);
        bttn_start_game.set_padding(8);
        bttn_start_game.set_border_thickness(3);

        self.l_button_by_page[page].append(bttn_start_game);


    #Fonctions draw
    def draw(self, window):

        self.l_drawed_button = [];

        if(self.page == Page.MainMenu):
            self.draw_main_menu(window);
        elif(self.page == Page.GameMenu):
            self.draw_game_menu(window);

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

    def draw_game_menu(self, window):

        interface_width = self.interface.MENU_WINDOW_WIDTH;
        interface_height = self.interface.MENU_WINDOW_HEIGHT;

        #PART BACKGROUND
        background_rect = (0, 0, interface_width, interface_height);
        pygame.draw.rect(window, (46, 40, 42), background_rect);


        #PART PLAYER NAME
        font = pygame.font.SysFont("", size=27);
        img_text_choose_player_name = font.render("Choisissez le nom des joueurs", True, (255, 255, 255));

        img_text_choose_player_name_size = img_text_choose_player_name.get_size();
        img_text_choose_player_name_x = int(interface_width/2-img_text_choose_player_name_size[0]/2);
        img_text_choose_player_name_y = 26;

        window.blit(img_text_choose_player_name, (img_text_choose_player_name_x, img_text_choose_player_name_y));

        line_1_start_pos = (img_text_choose_player_name_x, img_text_choose_player_name_y-10);
        line_1_end_pos = (img_text_choose_player_name_x+img_text_choose_player_name_size[0], img_text_choose_player_name_y-10);

        pygame.draw.line(window, (255, 255, 255), line_1_start_pos, line_1_end_pos);

        line_2_start_pos = (img_text_choose_player_name_x, img_text_choose_player_name_y+img_text_choose_player_name_size[1]+10);
        line_2_end_pos = (img_text_choose_player_name_x+img_text_choose_player_name_size[0], img_text_choose_player_name_y+img_text_choose_player_name_size[1]+10);

        pygame.draw.line(window, (255, 255, 255), line_2_start_pos, line_2_end_pos);

        font = pygame.font.SysFont("", size=22);

        img_label_joueur_1 = font.render("Nom du joueur 1", True, (255, 255, 255));
        window.blit(img_label_joueur_1, (15, 80));

        img_label_joueur_2 = font.render("Nom du joueur 2", True, (255, 255, 255));
        window.blit(img_label_joueur_2, (15, 150));

        img_label_joueur_3 = font.render("Nom du joueur 3", True, (255, 255, 255));
        window.blit(img_label_joueur_3, (15, 220));

        img_label_joueur_4 = font.render("Nom du joueur 4", True, (255, 255, 255));
        window.blit(img_label_joueur_4, (15, 290));


        #PART NUMBER BOT
        font = pygame.font.SysFont("", size=27);
        img_text_choose_n_bot = font.render("Choisissez le nombre de bot", True, (255, 255, 255));

        img_text_choose_n_bot_size = img_text_choose_n_bot.get_size();
        img_text_choose_n_bot_x = interface_width/2-img_text_choose_n_bot_size[0]/2;
        img_text_choose_n_bot_y = 390;

        window.blit(img_text_choose_n_bot, (img_text_choose_n_bot_x, img_text_choose_n_bot_y));

        line_1_start_pos = (img_text_choose_n_bot_x, img_text_choose_n_bot_y-10);
        line_1_end_pos = (img_text_choose_n_bot_x+img_text_choose_n_bot_size[0], img_text_choose_n_bot_y-10);

        pygame.draw.line(window, (255, 255, 255), line_1_start_pos, line_1_end_pos);

        line_2_start_pos = (img_text_choose_n_bot_x, img_text_choose_n_bot_y+img_text_choose_n_bot_size[1]+10);
        line_2_end_pos = (img_text_choose_n_bot_x+img_text_choose_n_bot_size[0], img_text_choose_n_bot_y+img_text_choose_n_bot_size[1]+10);

        pygame.draw.line(window, (255, 255, 255), line_2_start_pos, line_2_end_pos);



        i_page=int(Page.GameMenu)
        for button in self.l_button_by_page[i_page]:
            button.draw(window);

        for tew in self.l_tew_by_page[i_page]:
            tew.draw(window);

        for tsw in self.l_tsw_by_page[i_page]:
            tsw.draw(window);


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

                    elif(button.get_text() == "Jouer contre un bot"):
                        self.change_page(1);

            for tsw in self.l_tsw_by_page[i_page]:

                if(tsw.in_arrow_left_bounds(mouse_x, mouse_y)):
                    tsw.previous();
                elif(tsw.in_arrow_right_bounds(mouse_x, mouse_y)):
                    tsw.next();


    def change_page(self, page):

        self.page = page;

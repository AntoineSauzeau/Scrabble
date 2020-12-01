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
from save_manager import SaveManager

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

        self.save_manager = SaveManager();

        self.l_button_by_page = [[], [], []];
        self.l_tew_by_page = [[], [], []];       #TextEditBox
        self.l_tsw_by_page = [[], [], []];       #TextSwitchWidget

        self.key_pressed = None;

        self.load_images();

        self.init_main_menu();
        self.init_game_menu();
        self.init_save_menu();


    def init_main_menu(self):

        interface_width = self.interface.MENU_WINDOW_WIDTH;
        interface_height = self.interface.MENU_WINDOW_HEIGHT;

        bttn_play_mode_turn = Button("Nouvelle partie");
        bttn_play_mode_turn.set_text_size(35);
        bttn_play_mode_turn.set_color((0, 0, 0));
        bttn_play_mode_turn.set_pos((interface_width/2, 275));
        bttn_play_mode_turn.set_padding(20);

        bttn_play_mode_bot = Button("Reprendre une partie");
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

        self.tew_name_player_1 = TextEditBox();
        self.tew_name_player_1.set_pos((15, 100));

        self.tew_name_player_2 = TextEditBox();
        self.tew_name_player_2.set_pos((15, 170));

        self.tew_name_player_3 = TextEditBox();
        self.tew_name_player_3.set_pos((15, 240));

        self.tew_name_player_4 = TextEditBox();
        self.tew_name_player_4.set_pos((15, 310));

        self.l_tew_by_page[page].append(self.tew_name_player_1);
        self.l_tew_by_page[page].append(self.tew_name_player_2);
        self.l_tew_by_page[page].append(self.tew_name_player_3);
        self.l_tew_by_page[page].append(self.tew_name_player_4);


        self.tsw_n_bot = TextSwitchWidget();
        self.tsw_n_bot.set_pos(interface_width/2, 447);
        self.tsw_n_bot.set_l_value(["0", "1", "2", "3"]);
        self.tsw_n_bot.set_text_size(16);

        self.l_tsw_by_page[page].append(self.tsw_n_bot);


        bttn_start_game = Button("Lancer la partie");
        bttn_start_game.set_text_size(27);
        bttn_start_game.set_pos((interface_width-105, interface_height-35));
        bttn_start_game.set_border(True);
        bttn_start_game.set_padding(8);
        bttn_start_game.set_border_thickness(3);

        self.l_button_by_page[page].append(bttn_start_game);

    def init_save_menu(self):

        interface_width = self.interface.MENU_WINDOW_WIDTH;
        interface_height = self.interface.MENU_WINDOW_HEIGHT;

        bttn_load = Button("Charger");
        bttn_load.set_text_size(24);
        bttn_load.set_padding(10);
        bttn_load.set_pos((interface_width-55, interface_height-30));
        bttn_load.set_border(True);
        bttn_load.set_border_thickness(3);

        bttn_back = Button("Retour");
        bttn_back.set_text_size(24);
        bttn_back.set_padding(10);
        bttn_back.set_pos((50, interface_height-30));
        bttn_back.set_border(True);
        bttn_back.set_border_thickness(3);

        page = Page.SaveMenu;
        self.l_button_by_page[page].append(bttn_load);
        self.l_button_by_page[page].append(bttn_back);

        tsw_page = TextSwitchWidget();
        tsw_page.set_pos(interface_width/2, 485);
        tsw_page.set_l_value(["Page 1", "Page 2"]);
        tsw_page.set_text_size(16);

        self.l_tsw_by_page[page].append(tsw_page);


    #Fonctions draw
    def draw(self, window):

        self.l_drawed_button = [];

        if(self.page == Page.MainMenu):
            self.draw_main_menu(window);
        elif(self.page == Page.GameMenu):
            self.draw_game_menu(window);
        elif(self.page == Page.SaveMenu):
            self.draw_save_menu(window);

        self.draw_widgets(window);

        pygame.display.flip();

    def draw_main_menu(self, window):

        interface_width = self.interface.MENU_WINDOW_WIDTH;
        interface_height = self.interface.MENU_WINDOW_HEIGHT;

        background_rect = (0, 0, interface_width, interface_height);
        pygame.draw.rect(window, (255, 255, 255), background_rect);

        window.blit(self.img_scrabble_title, (0, 0));


    def draw_game_menu(self, window):

        interface_width = self.interface.MENU_WINDOW_WIDTH;
        interface_height = self.interface.MENU_WINDOW_HEIGHT;

        #PART BACKGROUND
        background_rect = (0, 0, interface_width, interface_height);
        pygame.draw.rect(window, (101, 13, 27), background_rect);


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


    def draw_save_menu(self, window):

        interface_width = self.interface.MENU_WINDOW_WIDTH;
        interface_height = self.interface.MENU_WINDOW_HEIGHT;

        #PART BACKGROUND
        background_rect = (0, 0, interface_width, interface_height);
        pygame.draw.rect(window, (101, 13, 27), background_rect);

        font = pygame.font.SysFont("", size=32);
        img_text_l_save = font.render("Liste des sauvegardes", True, (255, 255, 255));

        img_text_l_save_size = img_text_l_save.get_size();
        img_text_l_save_x = interface_width/2 - img_text_l_save_size[0]/2;

        window.blit(img_text_l_save, (img_text_l_save_x, 40));

        save_list_box_width = int(interface_width/1.5);
        save_list_box_x = interface_width/2 - (save_list_box_width)/2;

        save_list_box_rect = (save_list_box_x, 105, save_list_box_width, 350);

        pygame.draw.rect(window, (255, 255, 255), save_list_box_rect);
        pygame.draw.rect(window, (0, 0, 0), save_list_box_rect, 4);

        l_save_name = self.save_manager.get_l_save_name();
        n_save = len(l_save_name);

        font = pygame.font.SysFont("", size=23);

        text_n_save = "Vous avez " + str(n_save) + " sauvegarde(s)";
        img_text_n_save = font.render(text_n_save, True, (0, 0, 0));

        img_text_n_save_width = img_text_n_save.get_size()[0];
        img_text_n_save_x = interface_width/2-img_text_n_save_width/2;

        window.blit(img_text_n_save, (img_text_n_save_x, 125));

    def draw_widgets(self, window):

        for button in self.l_button_by_page[self.page]:
            button.draw(window);

        for tew in self.l_tew_by_page[self.page]:
            tew.draw(window);

        for tsw in self.l_tsw_by_page[self.page]:
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
                    elif(button.get_text() == "Nouvelle partie"):
                        self.change_page(Page.GameMenu);

                    elif(button.get_text() == "Reprendre une partie"):
                        self.change_page(Page.SaveMenu);

                    elif(button.get_text() == "Lancer la partie"):

                        l_player = [];

                        for tew in self.l_tew_by_page[Page.GameMenu]:

                            player_name = tew.get_text();
                            if(player_name != ""):
                                l_player.append(Player(player_name));


                        if(len(l_player) >= 2):
                            game = Game(l_player);
                            self.interface.create_game_interface(game);
                            self.interface.change_page(1);

                    elif(button.get_text() == "Retour"):
                        self.change_page(Page.MainMenu);


            for tsw in self.l_tsw_by_page[i_page]:

                if(tsw.in_arrow_left_bounds(mouse_x, mouse_y)):
                    tsw.previous();
                elif(tsw.in_arrow_right_bounds(mouse_x, mouse_y)):
                    tsw.next();

            for tew in self.l_tew_by_page[i_page]:

                if(tew.in_bounds(mouse_x, mouse_y)):
                    tew.set_focused(True);
                else:
                    tew.set_focused(False);

        elif(e.type == pygame.KEYDOWN):
            self.key_pressed = e.key;

        elif(e.type == pygame.KEYUP):

            for tew in self.l_tew_by_page[i_page]:

                if(tew.get_focused()):

                    tew.keyboard_event(self.key_pressed);
                    self.key_pressed = None;



    def change_page(self, page):

        self.page = page;

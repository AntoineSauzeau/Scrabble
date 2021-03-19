#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import time
from enum import IntEnum
import os
import math

from button import Button
from game import Game, get_played_time_formatted
from player import Player
from text_edit_widget import TextEditWidget
from text_switch_widget import TextSwitchWidget
from save_manager import SaveManager
from stats import Stats
from settings import Settings

class Page(IntEnum):
    MainMenu = 0,
    GameMenu = 1,
    SaveMenu = 2,
    StatsMenu = 3
    SettingsMenu = 4

class MenuInterface():
    """
        Manages the display and management of events in the menu window page
    """

    #Initialization functions
    def __init__(self, interface):
        print('Constructor Menu');

        self.interface = interface;
        self.page = Page.MainMenu;

        #Widget
        self.l_button_by_page = [[], [], [], [], []];
        self.l_tew_by_page = [[], [], [], [], []];       #TextEditWidget
        self.l_tsw_by_page = [[], [], [], [], []];       #TextSwitchWidget

        self.key_pressed = None;                    #Last key of the keyboard pressed, allows to know that it letter add to the tew that has the focus

        #Save
        self.save_manager = SaveManager();
        self.n_save_per_page = 10;
        self.save_page_index = 0;
        self.index_save_selected = None;
        self.l_img_delete_save_rect = [];
        self.l_img_text_save_rect = [];

        #Stats
        self.stats = Stats();

        self.stats = Stats();
        self.stats.load();

        #Settings
        self.settings_instance = None;


        #Initialisation of the graphic elements
        self.load_images();

        self.init_main_menu();
        self.init_game_menu();
        self.init_save_menu();
        self.init_stats_menu();
        self.init_settings_menu();


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

        self.tew_name_player_1 = TextEditWidget();
        self.tew_name_player_1.set_pos((15, 100));

        self.tew_name_player_2 = TextEditWidget();
        self.tew_name_player_2.set_pos((15, 170));

        self.tew_name_player_3 = TextEditWidget();
        self.tew_name_player_3.set_pos((15, 240));

        self.tew_name_player_4 = TextEditWidget();
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


        bttn_next = Button("Suivant");
        bttn_next.set_text_size(27);
        bttn_next.set_pos((interface_width-56, interface_height-30));
        bttn_next.set_border(True);
        bttn_next.set_padding(8);
        bttn_next.set_border_thickness(3);

        bttn_back = Button("Retour");
        bttn_back.set_text_size(27);
        bttn_back.set_pos((51, interface_height-30));
        bttn_back.set_border(True);
        bttn_back.set_padding(8);
        bttn_back.set_border_thickness(3);

        self.l_button_by_page[page].append(bttn_next);
        self.l_button_by_page[page].append(bttn_back);

    def init_save_menu(self):

        interface_width = self.interface.MENU_WINDOW_WIDTH;
        interface_height = self.interface.MENU_WINDOW_HEIGHT;

        bttn_load = Button("Tout supprimer");
        bttn_load.set_text_size(24);
        bttn_load.set_padding(10);
        bttn_load.set_pos((interface_width-84, interface_height-30));
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

        self.tsw_page = TextSwitchWidget();
        self.tsw_page.set_pos(interface_width/2, 485);
        self.tsw_page.set_l_value(["Page 1", "Page 2"]);
        self.tsw_page.set_text_size(16);

        self.l_tsw_by_page[page].append(self.tsw_page);

    def init_stats_menu(self):

        interface_width = self.interface.MENU_WINDOW_WIDTH;
        interface_height = self.interface.MENU_WINDOW_HEIGHT;

        self.tsw_player_stats = TextSwitchWidget();
        self.tsw_player_stats.set_pos(interface_width/2, 500);

        bttn_back = Button("Retour");
        bttn_back.set_text_size(24);
        bttn_back.set_padding(10);
        bttn_back.set_pos((50, interface_height-30));
        bttn_back.set_border(True);
        bttn_back.set_border_thickness(3);

        bttn_reset = Button("Réinitialiser");
        bttn_reset.set_text_size(24);
        bttn_reset.set_padding(10);
        bttn_reset.set_pos((interface_width-71, interface_height-30));
        bttn_reset.set_border(True);
        bttn_reset.set_border_thickness(3);

        page = Page.StatsMenu;
        self.l_button_by_page[page].append(bttn_back);
        self.l_button_by_page[page].append(bttn_reset);

        self.tsw_player_stats_page = TextSwitchWidget();
        self.tsw_player_stats_page.set_pos(interface_width/2, 502);
        self.tsw_player_stats_page.set_text_size(13);

        l_player_name = self.stats.get_l_player_name(); print(l_player_name);
        if(len(l_player_name) != 0):
            self.tsw_player_stats_page.set_l_value(l_player_name);
        else:
            self.tsw_player_stats_page.set_l_value(["Aucun joueur"]);

        self.l_tsw_by_page[page].append(self.tsw_player_stats_page);

    def init_settings_menu(self):

        interface_width = self.interface.MENU_WINDOW_WIDTH;
        interface_height = self.interface.MENU_WINDOW_HEIGHT;

        bttn_back = Button("Retour");
        bttn_back.set_text_size(24);
        bttn_back.set_padding(10);
        bttn_back.set_pos((50, interface_height-30));
        bttn_back.set_border(True);
        bttn_back.set_border_thickness(3);

        page = Page.SettingsMenu;
        self.l_button_by_page[page].append(bttn_back);

        self.settings_instance = Settings();
        settings = self.settings_instance.get_l_settings();

        self.tsw_dictionary = TextSwitchWidget();
        self.tsw_dictionary.set_pos(interface_width/2, 200);
        self.tsw_dictionary.set_text_size(23);

        l_tsw_value = ["Officiel du scrabble", "Dictionnaire plus complet"];
        self.tsw_dictionary.set_l_value(l_tsw_value);
        self.tsw_dictionary.set_index(settings["dict_index"]);

        self.l_tsw_by_page[page].append(self.tsw_dictionary);






    #Draw functions
    def draw(self, window):

        self.l_drawed_button = [];

        if(self.page == Page.MainMenu):
            self.draw_main_menu(window);
        elif(self.page == Page.GameMenu):
            self.draw_game_menu(window);
        elif(self.page == Page.SaveMenu):
            self.draw_save_menu(window);
        elif(self.page == Page.StatsMenu):
            self.draw_stats_menu(window);
        elif(self.page == Page.SettingsMenu):
            self.draw_settings_menu(window);

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

        save_list_box_rect = (save_list_box_x, 95, save_list_box_width, 350);

        pygame.draw.rect(window, (255, 255, 255), save_list_box_rect);
        pygame.draw.rect(window, (0, 0, 0), save_list_box_rect, 4);

        l_save_name = self.save_manager.get_l_save_name();
        n_save = len(l_save_name);

        font = pygame.font.SysFont("", size=23);

        text_n_save = "Vous avez " + str(n_save) + " sauvegarde(s)";
        img_text_n_save = font.render(text_n_save, True, (0, 0, 0));

        img_text_n_save_width = img_text_n_save.get_size()[0];
        img_text_n_save_x = interface_width/2-img_text_n_save_width/2;

        window.blit(img_text_n_save, (img_text_n_save_x, 115));

        font = pygame.font.SysFont("", size=24);

        self.l_img_delete_save_rect.clear();
        self.l_img_text_save_rect.clear();

        save_min_index = self.save_page_index*self.n_save_per_page;
        save_max_index = save_min_index + self.n_save_per_page;
        for save_index in range(save_min_index, save_max_index):

            if(save_index == len(l_save_name)):
                break;

            save_name = l_save_name[save_index];
            text_save = str(save_index+1) + ") " + save_name;

            img_text_save = font.render(text_save, True, (0, 0, 0));

            img_text_save_size = img_text_save.get_size();
            img_text_save_y = (save_index-save_min_index)*28+156-img_text_save_size[1]/2;

            window.blit(img_text_save, (85, img_text_save_y));

            img_text_save_rect = (85, img_text_save_y, img_text_save_size[0], img_text_save_size[1]);

            self.l_img_text_save_rect.append(img_text_save_rect);


            img_delete_save_size = self.img_red_cross.get_size();
            img_delete_save_x = save_list_box_x+save_list_box_width-27-img_delete_save_size[0]/2;
            img_delete_save_y = img_text_save_y-img_delete_save_size[1]/2+img_text_save_size[1]/2;

            window.blit(self.img_red_cross, (img_delete_save_x, img_delete_save_y));

            img_delete_save_rect = (img_delete_save_x, img_delete_save_y, img_delete_save_size[0], img_delete_save_size[1]);

            self.l_img_delete_save_rect.append(img_delete_save_rect);


        n_save_page = math.ceil(len(l_save_name)/self.n_save_per_page);
        l_page_name = [];
        for i in range(n_save_page):
            page_name = "Page " + str(i+1);
            l_page_name.append(page_name);

        self.tsw_page.set_l_value(l_page_name);


    def draw_stats_menu(self, window):

        interface_width = self.interface.MENU_WINDOW_WIDTH;
        interface_height = self.interface.MENU_WINDOW_HEIGHT;

        background_rect = (0, 0, interface_width, interface_height);
        pygame.draw.rect(window, (105, 56, 92), background_rect);

        font = pygame.font.SysFont("", size=32);
        img_text_global_stats = font.render("Statistiques globales", True, (255, 255, 255));

        img_text_global_stats_size = img_text_global_stats.get_size();
        img_text_global_stats_x = interface_width/2-img_text_global_stats_size[0]/2;

        window.blit(img_text_global_stats, (img_text_global_stats_x, 20));

        l_global_stats = self.stats.get_l_global_stats();

        font = pygame.font.SysFont("", size=26);

        text_n_game = "Nombre de partie : " + str(l_global_stats["n_game"]);
        text_n_scrabble = "Nombre de scrabble : " + str(l_global_stats["n_scrabble"]);
        text_n_placed_letter = "Nombre de lettres placées : " + str(l_global_stats["n_placed_letter"]);
        text_n_placed_word = "Nombre de mots placés : " + str(l_global_stats["n_placed_word"]);

        time_played = l_global_stats["time_played"];
        time_played_formatted = get_played_time_formatted(time_played);
        text_played_time = "Temps joué : " + time_played_formatted;

        img_text_n_game = font.render(text_n_game, True, (255, 255, 255));
        img_text_n_scrabble = font.render(text_n_scrabble, True, (255, 255, 255));
        img_text_n_placed_letter = font.render(text_n_placed_letter, True, (255, 255, 255));
        img_text_n_placed_word = font.render(text_n_placed_word, True, (255, 255, 255));
        img_text_played_time = font.render(text_played_time, True, (255, 255, 255));

        window.blit(img_text_n_game, (32, 70));
        window.blit(img_text_n_scrabble, (32, 100));
        window.blit(img_text_n_placed_letter, (32, 130));
        window.blit(img_text_n_placed_word, (32, 160));
        window.blit(img_text_played_time, (32, 190));

        img_text_played_time_size = img_text_played_time.get_size();
        line_start_pos = (20, 70);
        line_end_pos = (20, 190 + img_text_played_time_size[1]);

        pygame.draw.line(window, (255, 255, 255), line_start_pos, line_end_pos, 6);

        font = pygame.font.SysFont("", size=32);
        img_text_player_stats = font.render("Statistiques par joueur", True, (255, 255, 255));

        img_text_player_stats_size = img_text_player_stats.get_size();
        img_text_player_stats_x = interface_width/2-img_text_player_stats_size[0]/2;

        window.blit(img_text_player_stats, (img_text_player_stats_x, 240));

        l_player_stats = self.stats.get_l_player_stats();
        if(len(l_player_stats) == 0):

            n_win = 0;
            n_lose = 0;
            n_scrabble = 0;
            n_placed_letter = 0;
            n_placed_word = 0;
            time_played = 0;

        else:

            player_name = self.tsw_player_stats_page.get_displayed_value();
            player_stats = l_player_stats[player_name];

            n_win = player_stats["n_win"];
            n_lose = player_stats["n_lose"];
            n_scrabble = player_stats["n_scrabble"];
            n_placed_letter = player_stats["n_placed_letter"];
            n_placed_word = player_stats["n_placed_word"];
            time_played = player_stats["time_played"];

        text_n_win = "Nombre de partie gagnée : " + str(n_win);
        text_n_lose = "Nombre de partie perdu : " + str(n_lose);
        text_n_scrabble = "Nombre de scrabble : " + str(n_scrabble);
        text_n_placed_letter = "Nombre de lettre posée : " + str(n_placed_letter);
        text_n_placed_word = "Nombre de mot posé : " + str(n_placed_word);

        time_played_formatted = get_played_time_formatted(time_played);
        text_time_played = "Temps joué : " + time_played_formatted;

        font = pygame.font.SysFont("", size=26);

        img_text_n_win = font.render(text_n_win, True, (255, 255, 255));
        img_text_n_lose = font.render(text_n_lose, True, (255, 255, 255));
        img_text_n_scrabble = font.render(text_n_scrabble, True, (255, 255, 255));
        img_text_n_placed_letter = font.render(text_n_placed_letter, True, (255, 255, 255));
        img_text_n_placed_word = font.render(text_n_placed_word, True, (255, 255, 255));
        img_text_time_played = font.render(text_time_played, True, (255, 255, 255));

        window.blit(img_text_n_win, (32, 290));
        window.blit(img_text_n_lose, (32, 320));
        window.blit(img_text_n_scrabble, (32, 350));
        window.blit(img_text_n_placed_letter, (32, 380));
        window.blit(img_text_n_placed_word, (32, 410));
        window.blit(img_text_time_played, (32, 440));

        img_text_time_played_size = img_text_time_played.get_size();
        line_start_pos = (20, 290);
        line_end_pos = (20, 440 + img_text_time_played_size[1]);

        pygame.draw.line(window, (255, 255, 255), line_start_pos, line_end_pos, 6);



    def draw_settings_menu(self, window):

        interface_width = self.interface.MENU_WINDOW_WIDTH;
        interface_height = self.interface.MENU_WINDOW_HEIGHT;

        background_rect = (0, 0, interface_width, interface_height);
        pygame.draw.rect(window, (49, 87, 44), background_rect);

        font = pygame.font.SysFont("", size=33);

        img_text_choose_dict = font.render("-- Choix du dictionnaire --", True, (255, 255, 255));

        img_text_choose_dict_size = img_text_choose_dict.get_size();
        img_text_choose_dict_x = interface_width/2 - img_text_choose_dict_size[0]/2;

        window.blit(img_text_choose_dict, (img_text_choose_dict_x, 150));





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

        self.img_red_cross = pygame.image.load(os.path.join("Images", "red_cross.png"))
        self.img_red_cross = pygame.transform.scale(self.img_red_cross, (15, 15));

    def replay_game(self, l_player):

        game = Game(l_player);
        self.interface.create_game_interface(game);

        game_interface = self.interface.get_game_interface();
        game.set_game_interface_instance(game_interface);


    #Fonctions event
    def event(self, e):

        i_page = int(self.page);

        if(e.type == pygame.QUIT):
            controller = self.interface.get_controller();
            controller.quit();

        elif(e.type == pygame.MOUSEMOTION):

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

                    elif(button.get_text() == "Statistiques"):
                        self.change_page(Page.StatsMenu);

                    elif(button.get_text() == "Paramètres"):
                        self.change_page(Page.SettingsMenu);

                    elif(button.get_text() == "Suivant"):

                        l_player = [];

                        for tew in self.l_tew_by_page[Page.GameMenu]:

                            player_name = tew.get_text();
                            if(player_name != ""):
                                l_player.append(Player(player_name));


                        if(len(l_player) >= 2):
                            game = Game(l_player);
                            self.interface.create_game_interface(game);

                            game_interface = self.interface.get_game_interface();
                            game.set_game_interface_instance(game_interface);

                            self.interface.change_page(1);

                    elif(button.get_text() == "Retour"):
                        self.change_page(Page.MainMenu);
                        self.l_img_text_save_rect.clear();

                    elif(button.get_text() == "Réinitialiser"):
                        self.stats.reset();
                        self.stats.load();

                    elif(button.get_text() == "Tout supprimer"):
                        self.save_manager.reset();


            for tsw in self.l_tsw_by_page[i_page]:

                if(tsw.in_arrow_left_bounds(mouse_x, mouse_y)):
                    tsw.previous();
                elif(tsw.in_arrow_right_bounds(mouse_x, mouse_y)):
                    tsw.next();

                if(tsw == self.tsw_dictionary):
                    settings = self.settings_instance.get_l_settings();
                    settings["dict_index"] = tsw.get_index();

                    self.settings_instance.save();

            self.save_page_index = self.tsw_page.get_index();

            for tew in self.l_tew_by_page[i_page]:

                if(tew.in_bounds(mouse_x, mouse_y)):
                    tew.set_focused(True);
                else:
                    tew.set_focused(False);

            for i in range(len(self.l_img_delete_save_rect)):

                img_delete_save_rect = self.l_img_delete_save_rect[i];

                if(self.in_rect_bounds(img_delete_save_rect, mouse_x, mouse_y)):

                    save_min_index = self.save_page_index*self.n_save_per_page;

                    l_save_name = self.save_manager.get_l_save_name();
                    save_name = l_save_name[save_min_index+i];

                    self.save_manager.remove_save(save_name);

            for i in range(len(self.l_img_text_save_rect)):

                img_text_save_rect = self.l_img_text_save_rect[i];

                if(self.in_rect_bounds(img_text_save_rect, mouse_x, mouse_y)):

                    save_min_index = self.save_page_index*self.n_save_per_page;

                    l_save_name = self.save_manager.get_l_save_name();
                    if(i == len(l_save_name)):
                        break;

                    save_name = l_save_name[save_min_index+i];

                    self.game = Game();
                    self.save_manager.set_game_instance(self.game);
                    self.save_manager.load_save(save_name);

                    self.interface.create_game_interface(self.game);
                    self.interface.change_page(1);

                    game_interface = self.interface.get_game_interface();
                    self.game.set_game_interface_instance(game_interface);
                    game_interface.show_message_save_loaded();

                    self.l_img_text_save_rect.clear()
                    break;



        elif(e.type == pygame.KEYDOWN):
            self.key_pressed = e.key;

        elif(e.type == pygame.KEYUP):

            for tew in self.l_tew_by_page[i_page]:

                if(tew.get_focused()):

                    tew.keyboard_event(self.key_pressed);
                    self.key_pressed = None;


    def in_rect_bounds(self, rect, x, y):

        x_min = rect[0];
        y_min = rect[1];
        x_max = x_min + rect[2];
        y_max = y_min + rect[3];

        return (x >= x_min and x <= x_max and y >= y_min and y <= y_max);



    #GETTERS/SETTERS
    def change_page(self, page):

        self.page = page;

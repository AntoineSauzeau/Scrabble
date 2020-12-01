import pygame
from menu_interface import MenuInterface
from game_interface import GameInterface
from enum import IntEnum

class Page(IntEnum):
    Menu = 0,
    Game = 1


class Interface:

    # CONSTANTES
    MENU_WINDOW_WIDTH = 379;
    MENU_WINDOW_HEIGHT = 600;

    GAME_WINDOW_WIDTH = 1100;
    GAME_WINDOW_HEIGHT = 700;

    def __init__(self, controller):

        pygame.init();

        self.window = pygame.display.set_mode((self.MENU_WINDOW_WIDTH, self.MENU_WINDOW_HEIGHT));
        pygame.display.set_caption("Scrabble");

        self.page = Page.Menu;

        self.controller = controller;

        self.menu = MenuInterface(self);
        self.game = None;

        self.draw();


    def event(self, e):

        if(self.page == Page.Menu):
            self.menu.event(e);
        elif(self.page == Page.Game):
            self.game.event(e);

    def draw(self):
        if(self.page == Page.Menu):
            self.menu.draw(self.window);
        elif(self.page == Page.Game):
            self.game.draw(self.window);




    def change_page(self, page):

        if(page == Page.Menu):

            self.page = page
            self.window = pygame.display.set_mode((self.MENU_WINDOW_WIDTH, self.MENU_WINDOW_HEIGHT));

        elif(page == Page.Game):

            self.page = page
            self.window = pygame.display.set_mode((self.GAME_WINDOW_WIDTH, self.GAME_WINDOW_HEIGHT));


    #GETTERS/SETTERS
    def get_page():
        return self.page;

    def get_controller(self):
        return self.controller;

    def get_menu_interface(self):
        return self.menu;

    def get_game_interface(self):
        return self.game;

    def create_game_interface(self, game):
        self.game = GameInterface(self, game);

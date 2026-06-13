
"""
Moduł game_app.py
Definiuje główną klasę zarządzającą całym środowiskiem uruchomieniowym gry (GameApp).
"""

import pygame
import sys
from settings import *
from entities import Player
import logic
import rendering

class GameApp:
    """
    Centralna klasa aplikacji, która przechowuje cały dynamiczny stan gry,
    zasoby (czcionki, okno) oraz spina logikę z renderowaniem klatek.
    """
    def __init__(self):
        """
        Konstruktor inicjalizujący silnik Pygame, okno wyświetlania oraz stan początkowy gry.
        """
        pygame.init()
        pygame.font.init()

        self.width = WIDTH
        self.height = HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        # Inicjalizacja czcionek
        self.font_ui = pygame.font.SysFont(None, 28)
        self.font_stage = pygame.font.SysFont(None, 36)
        self.font_small = pygame.font.SysFont(None, 20) 
        self.font_large = pygame.font.SysFont(None, 48) 
        self.font_gameover = pygame.font.SysFont(None, 100)

        # Inicjalizacja obiektów i kolekcji gry
        self.player = Player(WORLD_WIDTH / 2, WORLD_HEIGHT / 2)
        self.enemies = []
        self.items = []
        self.current_targets = []

        # Kontrolery stanów gry
        self.state = "MAIN_MENU" 
        self.stage = 1
        self.stage_timer = 0.0  
        self.stage_kills = 0

        self.enemy_speed_bonus = 0.0 
        self.save_message_timer = 0.0  

        self.wave1_spawned = False
        self.wave2_spawned = False
        self.running = True

        # Deklaracje obiektów interfejsu (Recty)
        self.btn_menu_rect = None
        self.btn_load_rect = None
        self.btn_go_restart_rect = None
        self.btn_go_load_rect = None
        self.shop_rects = []
        self.btn_stage_clear = None
        self.btn_save_game = None
        self.btn_shop_menu = None
        self.btn_return_menu_rect = None

    def update_rects(self):
        """
        Aktualizuje wymiary i pozycje przycisków interfejsu w zależności 
        od aktualnych wymiarów okna (obsługa resizable).
        """
        self.btn_menu_rect = pygame.Rect(self.width / 2 - 150, int(self.height / 2) - 60, 300, 50)
        self.btn_load_rect = pygame.Rect(self.width / 2 - 150, int(self.height / 2) + 10, 300, 50)
        
        self.btn_go_restart_rect = pygame.Rect(self.width / 2 - 150, int(self.height / 2) + 10, 300, 50)
        self.btn_go_load_rect = pygame.Rect(self.width / 2 - 150, int(self.height / 2) + 75, 300, 50)
        
        self.shop_rects = [pygame.Rect(self.width / 2 - 50, int(self.height / 2) - 120 + i * 32, 280, 28) for i in range(6)]
        self.btn_stage_clear = pygame.Rect(self.width / 2 - 150, int(self.height / 2) + 90, 300, 34)
        self.btn_save_game = pygame.Rect(self.width / 2 - 150, int(self.height / 2) + 140, 300, 34)
        self.btn_shop_menu = pygame.Rect(self.width / 2 - 150, int(self.height / 2) + 190, 300, 34)
        
        self.btn_return_menu_rect = pygame.Rect(self.width / 2 - 150, self.height / 2 + 80, 300, 50)

    def run(self):
        """
        Uruchamia główną nieskończoną pętlę gry (Game Loop).
        Kontroluje czas delta (dt) i synchronizuje moduły logic.py oraz rendering.py.
        """
        while self.running:
            dt = self.clock.tick(120) / 1000.0
            
            self.update_rects()
            logic.handle_events(self)
            logic.update_logic(self, dt)
            rendering.draw_screen(self)
            
            pygame.display.flip()

        pygame.quit()
        sys.exit()
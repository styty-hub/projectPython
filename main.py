"""
Moduł main.py
Główny punkt wejściowy do gry. Odpowiada za uruchomienie instancji klasy GameApp.
"""

from game import GameApp

if __name__ == "__main__":
    game = GameApp()
    game.run()
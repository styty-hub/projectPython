"""
Moduł entities.py
Zawiera definicje klas reprezentujących obiekty w grze: Player, Enemy oraz Item.
"""

class Player:
    """
    Klasa reprezentująca postać gracza.
    Przechowuje informacje o pozycji, statystykach, zdrowiu i zasobach.
    """
    def __init__(self, x, y):
        """
        Inicjalizuje obiekt gracza na podanych współrzędnych ze statystykami bazowymi.

        :param x: Początkowa współrzędna X (float lub int).
        :param y: Początkowa współrzędna Y (float lub int).
        """
        self.x = x
        self.y = y
        self.radius = 20
        self.max_hp = 5.0 
        self.hp = 5.0
        self.speed = 270 
        self.range = 150
        self.damage = 1.0
        self.attack_speed = 1.0
        self.weapons = 1
        self.attack_cooldown = 0.0
        self.hurt_timer = 0.0
        self.shoot_timer = 0.0 
        self.money = 0


class Enemy:
    """
    Klasa reprezentująca przeciwnika w grze.
    """
    def __init__(self, x, y, hp=2.0, speed=200, damage=0.5, attack_speed=0.75, radius=15):
        """
        Inicjalizuje obiekt przeciwnika.

        :param x: Początkowa współrzędna X (float lub int).
        :param y: Początkowa współrzędna Y (float lub int).
        :param hp: Maksymalne i początkowe zdrowie przeciwnika (float).
        :param speed: Prędkość poruszania się przeciwnika (float lub int).
        :param damage: Obrażenia zadawane przez przeciwnika (float).
        :param attack_speed: Szybkość ataku przeciwnika (float).
        :param radius: Promień (wielkość) przeciwnika (int).
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.max_hp = hp
        self.hp = hp
        self.speed = speed
        self.damage = damage
        self.attack_speed = attack_speed
        self.attack_cd = 0.0
        self.dist = 0.0 


class Item:
    """
    Klasa reprezentująca przedmiot leżący na mapie (np. leczenie, pieniądze).
    """
    def __init__(self, x, y, item_type, color, from_enemy=False):
        """
        Inicjalizuje obiekt przedmiotu.

        :param x: Współrzędna X przedmiotu na mapie (float lub int).
        :param y: Współrzędna Y przedmiotu na mapie (float lub int).
        :param item_type: Typ przedmiotu, np. "HEAL_DROP", "MONEY_DROP" (str).
        :param color: Kolor przedmiotu do renderowania (tuple RGB).
        :param from_enemy: Flaga oznaczająca, czy przedmiot wypadł z pokonanego wroga (bool).
        """
        self.x = x
        self.y = y
        self.radius = 10
        self.type = item_type
        self.color = color
        self.from_enemy = from_enemy
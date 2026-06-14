
"""
entities.py
Moduł zawierajacy klasy gracza, przeciwnika i przedmiotu
"""

class Player:
    """
    Reprezentacja Gracza
    """
    def __init__(self, x, y):
        """
        Konstruktor z domyślnym ustawianiem pozycji gracza

        :param x: koord X
        :param y: koord Y
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
    Reprezentacja Przeciwnika
    """
    def __init__(self, x, y, hp=2.0, speed=200, damage=0.5, attack_speed=0.75, radius=15):
        """
        Konstruktor z domyślnym ustawianiem pozycji, hp, obrazen, szybkosci, szybkosci ataku i wielkosci przeciwnika

        :param x: koord X
        :param y: koord Y
        :param hp: maks i poczatkowe zdrowie
        :param speed: szybkosc poruszania
        :param damage: obrazenia
        :param attack_speed: szybkosc ataku
        :param radius: promien koła przeciwnika
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
    Reprezentacja Przedmiotu
    """
    def __init__(self, x, y, item_type, color, from_enemy=False):
        """
        Konstruktor klasy przedmiotu ze stalą jego wielkoscią

        :param x: koord X
        :param y: koord Y
        :param item_type: typ przedmiotu 
        :param color: kolor
        :param from_enemy: flaga czy przedmiot jest od wroga
        """
        self.x = x
        self.y = y
        self.radius = 10
        self.type = item_type
        self.color = color
        self.from_enemy = from_enemy
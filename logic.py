
"""
logic.py
Moduł zawierajacy mechanike gry, ruch, spawn przeciwników i wykrywanie kolizjii
"""

import pygame
import random
import math
import os
from settings import *
from entities import Player, Enemy, Item

def handle_events(game):
    """
    Przetwarzanie danych z glownej klasy gry.

    :param game: obiekt gry
    """
    # petla eventow
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
            
        if event.type == pygame.VIDEORESIZE:
            game.width, game.height = event.w, event.h
            game.screen = pygame.display.set_mode((game.width, game.height), pygame.RESIZABLE)
            
        # myszka
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.state   == "MAIN_MENU":
                if game.btn_menu_rect.collidepoint(event.pos):
                    game.player = Player(WORLD_WIDTH / 2, WORLD_HEIGHT / 2) 
                    game.stage = 1
                    game.stage_timer = 0.0  
                    game.stage_kills = 0
                    game.enemy_speed_bonus = 0.0
                    game.enemies.clear() 
                    game.items.clear()   
                    game.wave1_spawned = False
                    game.wave2_spawned = False
                    game.state = "PLAYING"
                
                # ladowanie z pliku
                elif game.btn_load_rect.collidepoint(event.pos):
                    if os.path.exists("save.txt") and os.path.getsize("save.txt") > 0:
                        try:
                            save_dict = {}
                            with open("save.txt", "r") as f:
                                for line in f:
                                    if ":" in line:
                                        key, val = line.split(":", 1)
                                        save_dict[key.strip()] = val.strip()

                            if "Stage" in save_dict:
                                game.stage = int(save_dict.get("Stage", 1))
                                game.player.money = int(save_dict.get("Money", 0))
                                game.player.max_hp = float(save_dict.get("Max_HP", 5.0))
                                game.player.hp = float(save_dict.get("HP", 5.0))
                                game.player.speed = float(save_dict.get("Speed", 270.0))
                                game.player.damage = float(save_dict.get("Damage", 1.0))
                                game.player.attack_speed = float(save_dict.get("Attack_Speed", 1.0))
                                game.player.range = float(save_dict.get("Range", 150.0))
                                game.player.weapons = int(save_dict.get("Weapons", 1))
                                game.enemy_speed_bonus = float(save_dict.get("Enemy_Speed_Bonus", 0.0))
                                
                                game.state = "SHOP"
                                game.enemies.clear()
                                game.items.clear()
                                game.stage_timer = 0.0
                                game.stage_kills = 0
                                game.wave1_spawned = False
                                game.wave2_spawned = False
                        except Exception as e:
                            print("blad podczas ladowania:", e)

            elif game.state == "SHOP":
                if game.btn_stage_clear.collidepoint(event.pos):
                    hp_bonus = 1.0 + (game.stage - 1) * 0.5
                    game.player.max_hp += hp_bonus
                    game.player.hp = game.player.max_hp
                    
                    game.stage += 1
                    game.stage_timer = 0.0  
                    game.stage_kills = 0
                    game.enemies.clear() 
                    game.items.clear()   
                    game.wave1_spawned = False
                    game.wave2_spawned = False
                    game.state = "PLAYING" 
                
                elif game.btn_save_game.collidepoint(event.pos):
                    try:
                        with open("save.txt", "w") as f:
                            save_data = (
                                f"Stage: {game.stage}\n"
                                f"Money: {game.player.money}\n"
                                f"Max_HP: {game.player.max_hp}\n"
                                f"HP: {game.player.hp}\n"
                                f"Speed: {game.player.speed}\n"
                                f"Damage: {game.player.damage}\n"
                                f"Attack_Speed: {game.player.attack_speed}\n"
                                f"Range: {game.player.range}\n"
                                f"Weapons: {game.player.weapons}\n"
                                f"Enemy_Speed_Bonus: {game.enemy_speed_bonus}\n"
                            )
                            f.write(save_data)
                        game.save_message_timer = 2.0 
                    except Exception as e:
                        print("blad przy zapisie:", e)
                        
                elif game.btn_shop_menu.collidepoint(event.pos):
                    game.state = "MAIN_MENU"
                
                else:
                    base_prices = [35, 45, 65, 65, 85, 135]
                    prices = [base_price + (game.stage - 1) * 10 for base_price in base_prices]
                    
                    for i, rect in enumerate(game.shop_rects):
                        if rect.collidepoint(event.pos):
                            price = prices[i]
                            if game.player.money >= price:
                                if i == 0:                            # hp
                                    game.player.max_hp += 1
                                    game.player.hp += 1
                                    game.player.money -= price
                                elif i == 1 and game.player.speed < 400:   # speed
                                    game.player.speed += 10
                                    game.player.money -= price
                                    game.enemy_speed_bonus += 6.0
                                elif i == 2:                          # damage
                                    game.player.damage += 0.5
                                    game.player.money -= price
                                elif i == 3:                          # atk
                                    game.player.attack_speed += 0.2
                                    game.player.money -= price
                                elif i == 4:                          # range
                                    game.player.range += 15
                                    game.player.money -= price
                                elif i == 5 and game.player.weapons < 3:   # weapon
                                    game.player.weapons += 1
                                    game.player.money -= price
            
            elif game.state == "GAME_OVER":
                if game.btn_go_restart_rect.collidepoint(event.pos):
                    game.player = Player(WORLD_WIDTH / 2, WORLD_HEIGHT / 2) 
                    game.stage = 1
                    game.stage_timer = 0.0  
                    game.stage_kills = 0
                    game.enemy_speed_bonus = 0.0
                    game.enemies.clear() 
                    game.items.clear()   
                    game.wave1_spawned = False
                    game.wave2_spawned = False
                    game.state = "PLAYING" 
                
                elif game.btn_go_load_rect.collidepoint(event.pos):
                    if os.path.exists("save.txt") and os.path.getsize("save.txt") > 0:
                        try:
                            save_dict = {}
                            with open("save.txt", "r") as f:
                                for line in f:
                                    if ":" in line:
                                        key, val = line.split(":", 1)
                                        save_dict[key.strip()] = val.strip()

                                if "Stage" in save_dict:
                                    game.stage = int(save_dict.get("Stage", 1))
                                    game.player.money = int(save_dict.get("Money", 0))
                                    game.player.max_hp = float(save_dict.get("Max_HP", 5.0))
                                    game.player.hp = float(save_dict.get("HP", 5.0))
                                    game.player.speed = float(save_dict.get("Speed", 270.0))
                                    game.player.damage = float(save_dict.get("Damage", 1.0))
                                    game.player.attack_speed = float(save_dict.get("Attack_Speed", 1.0))
                                    game.player.range = float(save_dict.get("Range", 150.0))
                                    game.player.weapons = int(save_dict.get("Weapons", 1))
                                    game.enemy_speed_bonus = float(save_dict.get("Enemy_Speed_Bonus", 0.0))
                                    
                                    game.state = "SHOP"
                                    game.enemies.clear()
                                    game.items.clear()
                                    game.stage_timer = 0.0
                                    game.stage_kills = 0
                                    game.wave1_spawned = False
                                    game.wave2_spawned = False
                        except Exception as e:
                            print("blad przy ladowaniu:", e)

            elif game.state == "PAUSED":
                if game.btn_return_menu_rect.collidepoint(event.pos):
                    game.state = "MAIN_MENU"
                
        # klawiatura
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game.state == "PLAYING":
                    game.state = "PAUSED"
                elif game.state == "PAUSED":
                    game.state = "PLAYING"

def update_logic(game, dt):
    """
    Aktualizacja pozycji, walki i przeciwnikow
    
    :param game: obiekt gry
    :param dt: delta time
    """
    if game.save_message_timer > 0:
        game.save_message_timer -= dt

    if game.state == "PLAYING":
        # stage timer
        game.stage_timer += dt  
        if game.stage_timer >= 60.0:  
            game.stage_timer = 60.0
            game.state = "SHOP" 

        if game.player.hp <= 0:
            game.state = "GAME_OVER"
            
        if game.player.hurt_timer > 0:
            game.player.hurt_timer -= dt
            
        if game.player.shoot_timer > 0:
            game.player.shoot_timer -= dt

        # ruch gracza
        keys = pygame.key.get_pressed()
        dir_x, dir_y = 0, 0

        if keys[pygame.K_w]: dir_y -= 1
        if keys[pygame.K_s]: dir_y += 1
        if keys[pygame.K_a]: dir_x -= 1
        if keys[pygame.K_d]: dir_x += 1

        if dir_x != 0 and dir_y != 0:
            dir_x *= 0.707
            dir_y *= 0.707

        game.player.x += dir_x * game.player.speed * dt
        game.player.y += dir_y * game.player.speed * dt

        if game.player.x < game.player.radius: game.player.x = game.player.radius
        if game.player.x > WORLD_WIDTH - game.player.radius: game.player.x = WORLD_WIDTH - game.player.radius
        if game.player.y < game.player.radius: game.player.y = game.player.radius
        if game.player.y > WORLD_HEIGHT - game.player.radius: game.player.y = WORLD_HEIGHT - game.player.radius

        # spawn wrogow
        current_max_enemies = 10 + (game.stage - 1) * 5
        enemies_to_spawn = 0
        
        if not game.wave1_spawned:
            enemies_to_spawn = current_max_enemies // 2
            game.wave1_spawned = True
        elif game.stage_timer >= 15.0 and not game.wave2_spawned:
            enemies_to_spawn = current_max_enemies - len(game.enemies)
            game.wave2_spawned = True
        elif game.wave2_spawned and len(game.enemies) < current_max_enemies:
            enemies_to_spawn = 1

        for _ in range(enemies_to_spawn):
            mid_x = WORLD_WIDTH / 2
            mid_y = WORLD_HEIGHT / 2
            
            if game.player.x < mid_x:
                min_x = 30
                max_x = int(mid_x)
            else:
                min_x = int(mid_x)
                max_x = WORLD_WIDTH - 30
                
            if game.player.y < mid_y:
                min_y = 30
                max_y = int(mid_y)
            else:
                min_y = int(mid_y)
                max_y = WORLD_HEIGHT - 30
            
            spawn_x = random.randint(min_x, max_x)
            spawn_y = random.randint(min_y, max_y)
            
            attempts = 0
            while math.hypot(game.player.x - spawn_x, game.player.y - spawn_y) < 400 and attempts < 50:
                spawn_x = random.randint(min_x, max_x)
                spawn_y = random.randint(min_y, max_y)
                attempts += 1
            
            normal_hp = 2.0 + (game.stage - 1) * 0.5
            normal_speed = 220 + ((game.stage - 1) * 3) + game.enemy_speed_bonus
            normal_damage = 0.5 + (game.stage - 1) * 0.5
            
            is_big_enemy = game.stage >= 3 and random.random() < 0.20
            
            if is_big_enemy:
                enemy_hp = normal_hp * 2.0 
                enemy_radius = 30
                enemy_speed = normal_speed * 0.75
                enemy_damage = normal_damage * 2.0
            else:
                enemy_hp = normal_hp
                enemy_radius = 15
                enemy_speed = normal_speed
                enemy_damage = normal_damage
            
            game.enemies.append(Enemy(spawn_x, spawn_y, hp=enemy_hp, speed=enemy_speed, damage=enemy_damage, radius=enemy_radius))

        for enemy in game.enemies:
            enemy.dist = math.hypot(game.player.x - enemy.x, game.player.y - enemy.y)

        # atak
        game.player.attack_cooldown -= dt

        enemies_in_range = [e for e in game.enemies if e.dist <= game.player.range]
        enemies_in_range.sort(key=lambda e: e.dist)
        game.current_targets = enemies_in_range[:game.player.weapons]

        if game.player.attack_cooldown <= 0:
            if game.current_targets:
                for target in game.current_targets:
                    target.hp -= game.player.damage
                game.player.attack_cooldown = 1.0 / game.player.attack_speed
                game.player.shoot_timer = 0.1 

        # ruch wrogow
        alive_enemies = []
        for enemy in game.enemies:
            if enemy.hp <= 0:
                game.stage_kills += 1 
                
                if enemy.radius == 30:
                    game.player.money += (game.stage + 5)
                else:
                    game.player.money += game.stage  
                    
                if random.random() < 0.05:
                    game.items.append(Item(enemy.x, enemy.y, "HEAL_DROP", COLOR_HEAL, from_enemy=True))
                continue
            
            enemy.attack_cd -= dt
            dx = game.player.x - enemy.x
            dy = game.player.y - enemy.y
            
            if enemy.dist > 0:
                enemy.x += (dx / enemy.dist) * enemy.speed * dt
                enemy.y += (dy / enemy.dist) * enemy.speed * dt
                
            dist_to_player = math.hypot(game.player.x - enemy.x, game.player.y - enemy.y)
            
            if dist_to_player < game.player.radius + enemy.radius:
                if enemy.attack_cd <= 0:
                    game.player.hp -= enemy.damage
                    game.player.hurt_timer = 0.15 
                    enemy.attack_cd = 1.0 / enemy.attack_speed
                    if game.player.hp <= 0:
                        game.state = "GAME_OVER"
            
            alive_enemies.append(enemy)

        game.enemies = alive_enemies

        # kolizje wrogow
        for i in range(len(game.enemies)):
            for j in range(i + 1, len(game.enemies)):
                e1 = game.enemies[i]
                e2 = game.enemies[j]
                dx = e1.x - e2.x
                dy = e1.y - e2.y
                dist = math.hypot(dx, dy)
                min_dist = e1.radius + e2.radius
                if dist < min_dist and dist > 0:
                    overlap = min_dist - dist
                    nx = dx / dist
                    ny = dy / dist
                    e1.x += nx * (overlap / 2)
                    e1.y += ny * (overlap / 2)
                    e2.x -= nx * (overlap / 2)
                    e2.y -= ny * (overlap / 2)

        # spawn itemow
        map_money = [i for i in game.items if i.type == "MONEY_DROP"]
        map_gold = [i for i in game.items if i.type == "GOLDEN_ORB"]
        map_heals = [i for i in game.items if i.type == "HEAL_DROP" and not i.from_enemy]
        
        if len(map_money) < 3 and random.random() < 0.005:
            game.items.append(Item(
                random.randint(10, WORLD_WIDTH - 10),
                random.randint(10, WORLD_HEIGHT - 10),
                "MONEY_DROP",
                GREEN,
                from_enemy=False 
            ))
            
        if len(map_gold) < 1 and random.random() < 0.0005:
            game.items.append(Item(
                random.randint(10, WORLD_WIDTH - 10),
                random.randint(10, WORLD_HEIGHT - 10),
                "GOLDEN_ORB",
                COLOR_GOLD,
                from_enemy=False 
            ))
            
        if len(map_heals) < 1 and random.random() < 0.001:
            game.items.append(Item(
                random.randint(10, WORLD_WIDTH - 10),
                random.randint(10, WORLD_HEIGHT - 10),
                "HEAL_DROP",
                COLOR_HEAL,
                from_enemy=False 
            ))

        uncollected_items = []
        for item in game.items:
            dist_to_item = math.hypot(game.player.x - item.x, game.player.y - item.y)
            if dist_to_item < game.player.radius + item.radius:
                if item.type == "HEAL_DROP":
                    game.player.hp += 1.0 
                    if game.player.hp > game.player.max_hp:
                        game.player.hp = game.player.max_hp
                elif item.type == "MONEY_DROP":
                    game.player.money += 5
                elif item.type == "GOLDEN_ORB": 
                    game.player.money += 10
            else:
                uncollected_items.append(item)
        game.items = uncollected_items
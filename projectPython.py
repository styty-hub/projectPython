import pygame
import sys
import random
import math

# 1. INICJALIZACJA
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Survival RPG: Max HP tylko dla gracza")

BLACK = (0, 0, 0)
DARK_GRAY = (40, 40, 40)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

COLOR_SPEED = (0, 100, 255)      
COLOR_RANGE = (255, 255, 0)      
COLOR_ATK_SPD = (255, 165, 0)    
COLOR_DMG = (128, 0, 128)        
COLOR_HP = (0, 255, 100)         
COLOR_WEAPON = (0, 255, 255)     
COLOR_HEAL = (0, 255, 0)         

WORLD_WIDTH = 2000
WORLD_HEIGHT = 1500

font_ui = pygame.font.SysFont(None, 28)
font_small = pygame.font.SysFont(None, 20) 
font_gameover = pygame.font.SysFont(None, 100)

# --- 2. KLASY ---

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.max_hp = 5.0 
        self.hp = 5.0
        self.speed = 300
        self.range = 150
        self.damage = 1.0
        self.attack_speed = 1.0
        self.weapons = 1
        self.attack_cooldown = 0.0

class Enemy:
    def __init__(self, x, y, hp=2.0, speed=200, damage=0.5, attack_speed=0.75):
        self.x = x
        self.y = y
        self.radius = 15
        self.max_hp = hp
        self.hp = hp
        self.speed = speed
        self.damage = damage
        self.attack_speed = attack_speed
        self.attack_cd = 0.0
        self.dist = 0.0 

class Item:
    def __init__(self, x, y, item_type, color, from_enemy=False):
        self.x = x
        self.y = y
        self.radius = 10
        self.type = item_type
        self.color = color
        self.from_enemy = from_enemy

# --- 3. PRZYGOTOWANIE GRY ---

clock = pygame.time.Clock()
player = Player(WORLD_WIDTH / 2, WORLD_HEIGHT / 2)

enemies = []
MAX_ENEMIES = 10 
items = []

state = "PLAYING" 
stage = 1
stage_timer = 0.0  
stage_kills = 0

running = True

# --- 4. GŁÓWNA PĘTLA GRY ---
while running:
    
    dt = clock.tick(120) / 1000.0

    btn_rect = pygame.Rect(WIDTH / 2 - 150, HEIGHT / 2 + 50, 300, 60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == "STAGE_CLEAR" and btn_rect.collidepoint(event.pos):
                stage += 1
                stage_timer = 0.0  
                stage_kills = 0
                enemies.clear() 
                items.clear()   
                state = "PLAYING" 
            
            elif state == "GAME_OVER" and btn_rect.collidepoint(event.pos):
                player = Player(WORLD_WIDTH / 2, WORLD_HEIGHT / 2) 
                stage = 1
                stage_timer = 0.0  
                stage_kills = 0
                enemies.clear() 
                items.clear()   
                state = "PLAYING" 

    if state == "PLAYING":
        
        # 1. Obsługa Timera
        stage_timer += dt  
        if stage_timer >= 60.0:  
            stage_timer = 60.0
            state = "STAGE_CLEAR" 

        if player.hp <= 0:
            state = "GAME_OVER"
            
        # 2. Ruch Gracza
        keys = pygame.key.get_pressed()
        dir_x, dir_y = 0, 0

        if keys[pygame.K_w]: dir_y -= 1
        if keys[pygame.K_s]: dir_y += 1
        if keys[pygame.K_a]: dir_x -= 1
        if keys[pygame.K_d]: dir_x += 1

        if dir_x != 0 and dir_y != 0:
            dir_x *= 0.707
            dir_y *= 0.707

        player.x += dir_x * player.speed * dt
        player.y += dir_y * player.speed * dt

        if player.x < player.radius: player.x = player.radius
        if player.x > WORLD_WIDTH - player.radius: player.x = WORLD_WIDTH - player.radius
        if player.y < player.radius: player.y = player.radius
        if player.y > WORLD_HEIGHT - player.radius: player.y = WORLD_HEIGHT - player.radius

        # 3. Spawnowanie Wrogów
        if len(enemies) < MAX_ENEMIES:
            spawn_x = random.randint(15, WORLD_WIDTH - 15)
            spawn_y = random.randint(15, WORLD_HEIGHT - 15)
            while math.hypot(player.x - spawn_x, player.y - spawn_y) < 400:
                spawn_x = random.randint(15, WORLD_WIDTH - 15)
                spawn_y = random.randint(15, WORLD_HEIGHT - 15)
            
            enemy_hp = 2.0 + (stage - 1) * 0.5
            enemies.append(Enemy(spawn_x, spawn_y, hp=enemy_hp))

        for enemy in enemies:
            enemy.dist = math.hypot(player.x - enemy.x, player.y - enemy.y)

        # 4. Atak Gracza
        player.attack_cooldown -= dt

        if player.attack_cooldown <= 0:
            enemies_in_range = [e for e in enemies if e.dist <= player.range]
            enemies_in_range.sort(key=lambda e: e.dist)
            targets = enemies_in_range[:player.weapons]
            
            if targets:
                for target in targets:
                    target.hp -= player.damage
                player.attack_cooldown = 1.0 / player.attack_speed

        # 5. Ruch Wrogów i Kolizje 
        alive_enemies = []
        for enemy in enemies:
            if enemy.hp <= 0:
                stage_kills += 1 
                if random.random() < 0.20:
                    items.append(Item(enemy.x, enemy.y, "HEAL_DROP", COLOR_HEAL, from_enemy=True))
                continue
            
            enemy.attack_cd -= dt
            dx = player.x - enemy.x
            dy = player.y - enemy.y
            
            if enemy.dist > 0:
                enemy.x += (dx / enemy.dist) * enemy.speed * dt
                enemy.y += (dy / enemy.dist) * enemy.speed * dt
                
            dist_to_player = math.hypot(player.x - enemy.x, player.y - enemy.y)
            if dist_to_player < player.radius + enemy.radius:
                if enemy.attack_cd <= 0:
                    player.hp -= enemy.damage
                    enemy.attack_cd = 1.0 / enemy.attack_speed
                    if player.hp <= 0:
                        state = "GAME_OVER"
            
            alive_enemies.append(enemy)

        enemies = alive_enemies

        # 6. Odpychanie się Wrogów
        for i in range(len(enemies)):
            for j in range(i + 1, len(enemies)):
                e1 = enemies[i]
                e2 = enemies[j]
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

        # 7. Mechanika Przedmiotów 
        map_items = [i for i in items if not i.from_enemy]
        
        if len(map_items) < 3 and random.random() < 0.01:
            available_types = []
            available_weights = []

            if player.speed < 500:
                available_types.append({"type": "SPEED", "color": COLOR_SPEED})
                available_weights.append(16) 
                
            available_types.append({"type": "RANGE", "color": COLOR_RANGE})
            available_weights.append(16) 
            available_types.append({"type": "ATK_SPEED", "color": COLOR_ATK_SPD})
            available_weights.append(16) 
            available_types.append({"type": "DAMAGE", "color": COLOR_DMG})
            available_weights.append(15) 
            
            available_types.append({"type": "HP_BOOST", "color": COLOR_HP})
            available_weights.append(15) 
            available_types.append({"type": "HEAL_DROP", "color": COLOR_HEAL})
            available_weights.append(20) 
            
            if player.weapons < 3:
                available_types.append({"type": "WEAPON", "color": COLOR_WEAPON})
                available_weights.append(2)  

            if available_types:
                chosen_item = random.choices(available_types, weights=available_weights, k=1)[0]
                items.append(Item(
                    random.randint(10, WORLD_WIDTH - 10),
                    random.randint(10, WORLD_HEIGHT - 10),
                    chosen_item["type"],
                    chosen_item["color"],
                    from_enemy=False 
                ))

        uncollected_items = []
        for item in items:
            dist_to_item = math.hypot(player.x - item.x, player.y - item.y)
            if dist_to_item < player.radius + item.radius:
                if item.type == "SPEED": 
                    if player.speed < 500:
                        player.speed += 25
                        if player.speed > 500: player.speed = 500
                elif item.type == "RANGE": 
                    player.range += 20
                elif item.type == "ATK_SPEED": 
                    player.attack_speed += 0.2
                elif item.type == "DAMAGE": 
                    player.damage += 0.5
                elif item.type == "HP_BOOST": 
                    player.max_hp += 1.0
                    player.hp += 1.0
                elif item.type == "HEAL_DROP":
                    player.hp += 0.5
                    if player.hp > player.max_hp:
                        player.hp = player.max_hp
                elif item.type == "WEAPON":
                    if player.weapons < 3: player.weapons += 1
            else:
                uncollected_items.append(item)
        items = uncollected_items

    # --- KAMERA ---
    camera_x = player.x - (WIDTH / 2)
    camera_y = player.y - (HEIGHT / 2)

    camera_max_x = max(0, WORLD_WIDTH - WIDTH)
    camera_max_y = max(0, WORLD_HEIGHT - HEIGHT)
    
    if camera_x < 0: camera_x = 0
    if camera_x > camera_max_x: camera_x = camera_max_x
    if camera_y < 0: camera_y = 0
    if camera_y > camera_max_y: camera_y = camera_max_y

    # --- RYSOWANIE GRAFIKI ---
    screen.fill(BLACK)

    for x in range(0, WORLD_WIDTH + 1, 100):
        pygame.draw.line(screen, DARK_GRAY, (x - camera_x, 0 - camera_y), (x - camera_x, WORLD_HEIGHT - camera_y))
    for y in range(0, WORLD_HEIGHT + 1, 100):
        pygame.draw.line(screen, DARK_GRAY, (0 - camera_x, y - camera_y), (WORLD_WIDTH - camera_x, y - camera_y))

    pygame.draw.rect(screen, GREEN, (0 - camera_x, 0 - camera_y, WORLD_WIDTH, WORLD_HEIGHT), 5)

    for item in items:
        draw_item_x = int(item.x - camera_x)
        draw_item_y = int(item.y - camera_y)
        
        if item.type == "HEAL_DROP":
            pygame.draw.rect(screen, item.color, (draw_item_x - 3, draw_item_y - 10, 6, 20))
            pygame.draw.rect(screen, item.color, (draw_item_x - 10, draw_item_y - 3, 20, 6))
        else:
            pygame.draw.circle(screen, item.color, (draw_item_x, draw_item_y), item.radius)

    for enemy in enemies:
        draw_x = int(enemy.x - camera_x)
        draw_y = int(enemy.y - camera_y)
        pygame.draw.circle(screen, RED, (draw_x, draw_y), enemy.radius)
        
        hp_ratio = max(0, enemy.hp / enemy.max_hp) 
        pygame.draw.rect(screen, RED, (draw_x - 15, draw_y - 25, 30, 5))
        pygame.draw.rect(screen, GREEN, (draw_x - 15, draw_y - 25, 30 * hp_ratio, 5))

        # ZMIANA: Przeciwnicy znowu pokazują tylko aktualne HP
        enemy_hp_text = font_small.render(f"{enemy.hp:.1f}", True, WHITE)
        screen.blit(enemy_hp_text, enemy_hp_text.get_rect(center=(draw_x, draw_y - 35)))

    if state != "GAME_OVER":
        draw_player_x = int(player.x - camera_x)
        draw_player_y = int(player.y - camera_y)
        
        range_surface = pygame.Surface((player.range * 2, player.range * 2), pygame.SRCALPHA)
        pygame.draw.circle(range_surface, (255, 255, 255, 10), (player.range, player.range), player.range)
        screen.blit(range_surface, (draw_player_x - player.range, draw_player_y - player.range))
        
        pygame.draw.circle(screen, WHITE, (draw_player_x, draw_player_y), player.radius)

    # --- INTERFEJS UŻYTKOWNIKA ---
    bar_x, bar_y, bar_width, bar_height = 20, 20, 200, 16
    player_hp_ratio = max(0, player.hp / player.max_hp)
    pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (bar_x, bar_y, bar_width * player_hp_ratio, bar_height))

    # Gracz ma podwójny, kolorowy tekst HP
    text_start_x = bar_x + bar_width + 10
    current_hp_surface = font_ui.render(f"{player.hp:.1f}", True, COLOR_HP)
    screen.blit(current_hp_surface, (text_start_x, bar_y - 2))
    
    max_hp_surface = font_ui.render(f" / {player.max_hp:.1f}", True, WHITE)
    screen.blit(max_hp_surface, (text_start_x + current_hp_surface.get_width(), bar_y - 2))

    ui_elements = [
        {"text": f"Speed: {int(player.speed)}", "color": COLOR_SPEED},
        {"text": f"Damage: {player.damage:.1f}", "color": COLOR_DMG},
        {"text": f"Atk Speed: {player.attack_speed:.1f}/s", "color": COLOR_ATK_SPD},
        {"text": f"Range: {int(player.range)}", "color": COLOR_RANGE},
        {"text": f"Weapons: {player.weapons}/3", "color": COLOR_WEAPON if player.weapons < 3 else RED}
    ]
    for i, element in enumerate(ui_elements):
        text_surface = font_ui.render(element["text"], True, element["color"])
        screen.blit(text_surface, (20, 60 + (i * 30))) 

    seconds = int(stage_timer)
    ms = int((stage_timer % 1) * 100)
    timer_str = f"{seconds:02d}:{ms:02d}"
    timer_text = font_ui.render(timer_str, True, WHITE)
    screen.blit(timer_text, (WIDTH - timer_text.get_width() - 20, 20))

    # --- NAKŁADKI STANÓW ---
    if state == "STAGE_CLEAR":
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        clear_text = font_gameover.render(f"ETAP {stage} UKOŃCZONY!", True, GREEN)
        screen.blit(clear_text, clear_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 100)))

        kills_text = font_ui.render(f"Zabici przeciwnicy: {stage_kills}", True, WHITE)
        screen.blit(kills_text, kills_text.get_rect(center=(WIDTH / 2, HEIGHT / 2)))

        pygame.draw.rect(screen, GREEN, btn_rect)
        pygame.draw.rect(screen, WHITE, btn_rect, 3) 
        btn_text = font_ui.render("NASTĘPNY ETAP", True, BLACK)
        screen.blit(btn_text, btn_text.get_rect(center=btn_rect.center))

    elif state == "GAME_OVER":
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 
        screen.blit(overlay, (0, 0))
        
        game_over_text = font_gameover.render("GAME OVER", True, RED)
        screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50)))
        
        pygame.draw.rect(screen, RED, btn_rect)
        pygame.draw.rect(screen, WHITE, btn_rect, 3) 
        btn_text = font_ui.render("ZACZNIJ PONOWNIE", True, WHITE)
        screen.blit(btn_text, btn_text.get_rect(center=btn_rect.center))

    pygame.display.flip()

pygame.quit()
sys.exit()
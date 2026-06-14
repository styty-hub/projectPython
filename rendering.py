
"""
rendering.py
Moduł zawierajacy funkcję odpowiadającą za renderowanie świata gry co każdą klatke
"""

import math
import pygame
import os
from settings import *

def draw_screen(game):
    """
    Czyści ekran i renderuje grafike dopasowaną do bieżącego stanu gry

    :param game: obiekt gry
    """
    game.screen.fill(BLACK)

    if game.state == "MAIN_MENU":
        pygame.draw.rect(game.screen, GREEN, game.btn_menu_rect)
        pygame.draw.rect(game.screen, WHITE, game.btn_menu_rect, 3) 
        btn_text = game.font_ui.render("START", True, BLACK)
        game.screen.blit(btn_text, btn_text.get_rect(center=game.btn_menu_rect.center))
        
        can_load = os.path.exists("save.txt") and os.path.getsize("save.txt") > 0
        load_color = GREEN if can_load else DARK_GRAY
        load_text_color = BLACK
        
        pygame.draw.rect(game.screen, load_color, game.btn_load_rect)
        if can_load:
            pygame.draw.rect(game.screen, WHITE, game.btn_load_rect, 3)
        else:
            pygame.draw.rect(game.screen, DARK_GRAY, game.btn_load_rect, 3) 
            
        load_text_surf = game.font_ui.render("LOAD GAME", True, BLACK)
        game.screen.blit(load_text_surf, load_text_surf.get_rect(center=game.btn_load_rect.center))
        
    else:
        camera_x = int(game.player.x - (game.width / 2))
        camera_y = int(game.player.y - (game.height / 2))

        if WORLD_WIDTH < game.width:
            camera_x = int((WORLD_WIDTH - game.width) / 2)
        else:
            camera_max_x = int(WORLD_WIDTH - game.width)
            if camera_x < 0: camera_x = 0
            if camera_x > camera_max_x: camera_x = camera_max_x
            
        if WORLD_HEIGHT < game.height:
            camera_y = int((WORLD_HEIGHT - game.height) / 2)
        else:
            camera_max_y = int(WORLD_HEIGHT - game.height)
            if camera_y < 0: camera_y = 0
            if camera_y > camera_max_y: camera_y = camera_max_y

        # siatka w tle
        for x in range(0, WORLD_WIDTH + 1, 100):
            pygame.draw.line(game.screen, DARK_GRAY, (x - camera_x, 0 - camera_y), (x - camera_x, WORLD_HEIGHT - camera_y))
        for y in range(0, WORLD_HEIGHT + 1, 100):
            pygame.draw.line(game.screen, DARK_GRAY, (0 - camera_x, y - camera_y), (WORLD_WIDTH - camera_x, y - camera_y))

        pygame.draw.rect(game.screen, DARK_GRAY, (0 - camera_x, 0 - camera_y, WORLD_WIDTH, WORLD_HEIGHT), 5)

        # render itemow
        for item in game.items:
            draw_item_x = int(item.x - camera_x)
            draw_item_y = int(item.y - camera_y)
            
            if item.type == "HEAL_DROP":
                pygame.draw.rect(game.screen, item.color, (draw_item_x - 3, draw_item_y - 10, 6, 20))
                pygame.draw.rect(game.screen, item.color, (draw_item_x - 10, draw_item_y - 3, 20, 6))
            elif item.type == "GOLDEN_ORB": 
                pygame.draw.circle(game.screen, item.color, (draw_item_x, draw_item_y), item.radius + 3)
            else:
                pygame.draw.circle(game.screen, item.color, (draw_item_x, draw_item_y), item.radius)

        # render linii ataku
        if game.state == "PLAYING" and game.current_targets:
            draw_player_x = int(game.player.x - camera_x)
            draw_player_y = int(game.player.y - camera_y)
            
            if game.player.shoot_timer > 0:
                line_color = (255, 161, 84) 
                line_width = 5 
            else:
                line_color = (128, 128, 128) 
                line_width = 2
                
            for target in game.current_targets:
                draw_target_x = int(target.x - camera_x)
                draw_target_y = int(target.y - camera_y)
                pygame.draw.line(game.screen, line_color, (draw_player_x, draw_player_y), (draw_target_x, draw_target_y), line_width)

        # render wrogow i hp
        for enemy in game.enemies:
            draw_x = int(enemy.x - camera_x)
            draw_y = int(enemy.y - camera_y)
            
            if game.state == "PLAYING" and enemy in game.current_targets:
                enemy_color = (255, 90, 90) 
            else:
                enemy_color = RED
                
            pygame.draw.circle(game.screen, enemy_color, (draw_x, draw_y), enemy.radius)
            
            hp_ratio = max(0, enemy.hp / enemy.max_hp) 
            bar_w = enemy.radius * 2
            pygame.draw.rect(game.screen, RED, (draw_x - enemy.radius, draw_y - enemy.radius - 10, bar_w, 5))
            pygame.draw.rect(game.screen, GREEN, (draw_x - enemy.radius, draw_y - enemy.radius - 10, bar_w * hp_ratio, 5))

            enemy_hp_text = game.font_small.render(f"{enemy.hp:.1f}", True, WHITE)
            game.screen.blit(enemy_hp_text, enemy_hp_text.get_rect(center=(draw_x, draw_y - enemy.radius - 20)))

        # render playera
        if game.state != "GAME_OVER":
            draw_player_x = int(game.player.x - camera_x)
            draw_player_y = int(game.player.y - camera_y)
            
            range_surface = pygame.Surface((game.player.range * 2, game.player.range * 2), pygame.SRCALPHA)
            pygame.draw.circle(range_surface, (255, 255, 255, 10), (game.player.range, game.player.range), game.player.range)
            game.screen.blit(range_surface, (draw_player_x - game.player.range, draw_player_y - game.player.range))
            
            current_player_color = COLOR_HURT if game.player.hurt_timer > 0 else WHITE
            pygame.draw.circle(game.screen, current_player_color, (draw_player_x, draw_player_y), game.player.radius)

        # render hudu
        bar_x, bar_y, bar_width, bar_height = 20, 20, 200, 16
        player_hp_ratio = max(0, game.player.hp / game.player.max_hp)
        pygame.draw.rect(game.screen, RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(game.screen, GREEN, (bar_x, bar_y, bar_width * player_hp_ratio, bar_height))

        text_start_x = bar_x + bar_width + 10
        
        current_hp_color = GREEN if game.player.hp >= game.player.max_hp else RED
        current_hp_surface = game.font_ui.render(f"{game.player.hp:.1f}", True, current_hp_color)
        game.screen.blit(current_hp_surface, (text_start_x, bar_y - 2))
        
        max_hp_surface = game.font_ui.render(f" / {game.player.max_hp:.1f}", True, GREEN)
        game.screen.blit(max_hp_surface, (text_start_x + current_hp_surface.get_width(), bar_y - 2))

        ui_elements = [
            {"text": f"Speed: {int(game.player.speed)}", "color": COLOR_SPEED},
            {"text": f"Damage: {game.player.damage:.1f}", "color": COLOR_DMG},
            {"text": f"Atk Speed: {game.player.attack_speed:.1f}/s", "color": COLOR_ATK_SPD},
            {"text": f"Range: {int(game.player.range)}", "color": COLOR_RANGE},
            {"text": f"Weapons: {game.player.weapons}/3", "color": COLOR_WEAPON} 
        ]
        for i, element in enumerate(ui_elements):
            text_surface = game.font_ui.render(element["text"], True, element["color"])
            game.screen.blit(text_surface, (20, 60 + (i * 30))) 

        stage_text = game.font_stage.render(f"STAGE {game.stage}", True, RED)
        game.screen.blit(stage_text, (game.width - stage_text.get_width() - 20, 20))

        seconds = int(game.stage_timer)
        ms = int((game.stage_timer % 1) * 100)
        timer_str = f"{seconds:02d}:{ms:02d}"
        timer_text = game.font_large.render(timer_str, True, WHITE)
        game.screen.blit(timer_text, (game.width - timer_text.get_width() - 20, 60))

        money_text = game.font_large.render(f"{game.player.money} $", True, GREEN)
        game.screen.blit(money_text, (game.width - money_text.get_width() - 20, 110))

        # w zaleznosci od stanu gry render odpowiednich elementow gui
        if game.state == "PLAYING" and 10.0 <= game.stage_timer < 15.0 and not game.wave2_spawned:
            countdown_seconds = math.ceil(15.0 - game.stage_timer)
            wave_text_str = f"NEXT WAVE IN {countdown_seconds} s"
            wave_text_surf = game.font_large.render(wave_text_str, True, WHITE)
            game.screen.blit(wave_text_surf, wave_text_surf.get_rect(midtop=(game.width / 2, 20)))

        if game.state == "SHOP":
            overlay = pygame.Surface((game.width, game.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 240)) 
            game.screen.blit(overlay, (0, 0))

            clear_text = game.font_gameover.render(f"STAGE {game.stage} COMPLETE", True, GREEN)
            game.screen.blit(clear_text, clear_text.get_rect(center=(game.width / 2, int(game.height / 2) - 250)))

            kills_text = game.font_ui.render(f"Enemies slain: {game.stage_kills}", True, WHITE)
            game.screen.blit(kills_text, kills_text.get_rect(center=(game.width / 2, int(game.height / 2) - 210)))

            shop_money_color = RED if game.player.money <= 0 else GREEN
            money_shop_text = game.font_large.render(f"{game.player.money} $", True, shop_money_color)
            game.screen.blit(money_shop_text, money_shop_text.get_rect(center=(game.width / 2, int(game.height / 2) - 170)))

            base_prices = [35, 45, 65, 65, 85, 135] # hp speed damage atk range weapon
            prices = [base_price + (game.stage - 1) * 10 for base_price in base_prices]
            
            shop_labels = [
                ("Max HP +1", f"{prices[0]}$", COLOR_HP, True),
                ("Speed +10", f"{prices[1]}$", COLOR_SPEED, game.player.speed < 400),
                ("Damage +0.5", f"{prices[2]}$", COLOR_DMG, True),
                ("Atk Speed +0.2", f"{prices[3]}$", COLOR_ATK_SPD, True),
                ("Range +15", f"{prices[4]}$", COLOR_RANGE, True),
                ("Weapon +1", f"{prices[5]}$", COLOR_WEAPON, game.player.weapons < 3)
            ]

            for i, rect in enumerate(game.shop_rects):
                label, price_str, base_color, can_buy = shop_labels[i]
                can_afford = game.player.money >= prices[i]

                if not can_buy:
                    bg_color = BLACK
                    border_color = DARK_GRAY
                    text_color = DARK_GRAY
                    price_color = DARK_GRAY
                elif not can_afford:
                    bg_color = BLACK
                    border_color = RED
                    text_color = RED
                    price_color = RED
                else:
                    bg_color = DARK_GRAY
                    border_color = base_color
                    text_color = WHITE
                    price_color = GREEN
                
                pygame.draw.rect(game.screen, bg_color, rect)
                pygame.draw.rect(game.screen, border_color, rect, 2)
                
                text_surf = game.font_ui.render(label, True, text_color)
                game.screen.blit(text_surf, text_surf.get_rect(midleft=(rect.left + 15, rect.centery)))
                    
                price_surf = game.font_ui.render(price_str, True, price_color)
                game.screen.blit(price_surf, price_surf.get_rect(midright=(rect.right - 15, rect.centery)))

            shop_ui_elements = [
                {"text": f"Max HP: {game.player.max_hp:.1f}", "color": COLOR_HP},
                {"text": f"Speed: {int(game.player.speed)}", "color": COLOR_SPEED},
                {"text": f"Damage: {game.player.damage:.1f}", "color": COLOR_DMG},
                {"text": f"Atk Speed: {game.player.attack_speed:.1f}/s", "color": COLOR_ATK_SPD},
                {"text": f"Range: {int(game.player.range)}", "color": COLOR_RANGE},
                {"text": f"Weapons: {game.player.weapons}/3", "color": COLOR_WEAPON} 
            ]
            
            stats_start_x = int(game.width / 2) - 300
            stats_header = game.font_ui.render("CURRENT STATS:", True, WHITE)
            game.screen.blit(stats_header, stats_header.get_rect(midleft=(stats_start_x, int(game.height / 2) - 130)))

            for i, element in enumerate(shop_ui_elements):
                text_surface = game.font_ui.render(element["text"], True, element["color"])
                game.screen.blit(text_surface, text_surface.get_rect(midleft=(stats_start_x, int(game.height / 2) - 100 + i * 32))) 

            pygame.draw.rect(game.screen, GREEN, game.btn_stage_clear)
            pygame.draw.rect(game.screen, WHITE, game.btn_stage_clear, 3) 
            btn_text = game.font_ui.render("NEXT STAGE", True, BLACK)
            game.screen.blit(btn_text, btn_text.get_rect(center=game.btn_stage_clear.center))

            pygame.draw.rect(game.screen, COLOR_SAVE_BTN, game.btn_save_game)
            pygame.draw.rect(game.screen, WHITE, game.btn_save_game, 3) 
            save_btn_text = game.font_ui.render("SAVE GAME", True, WHITE)
            game.screen.blit(save_btn_text, save_btn_text.get_rect(center=game.btn_save_game.center))
            
            pygame.draw.rect(game.screen, RED, game.btn_shop_menu)
            pygame.draw.rect(game.screen, WHITE, game.btn_shop_menu, 3)
            menu_btn_text = game.font_ui.render("MAIN MENU", True, WHITE)
            game.screen.blit(menu_btn_text, menu_btn_text.get_rect(center=game.btn_shop_menu.center))

            if game.save_message_timer > 0:
                saved_text = game.font_ui.render("GAME SAVED", True, COLOR_SAVE_BTN)
                game.screen.blit(saved_text, saved_text.get_rect(center=(game.width / 2, game.btn_shop_menu.bottom + 40)))

        elif game.state == "GAME_OVER":
            overlay = pygame.Surface((game.width, game.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)) 
            game.screen.blit(overlay, (0, 0))
            
            game_over_text = game.font_gameover.render("GAME OVER", True, RED)
            game.screen.blit(game_over_text, game_over_text.get_rect(center=(game.width / 2, game.height / 2 - 50)))
            
            pygame.draw.rect(game.screen, RED, game.btn_go_restart_rect)
            pygame.draw.rect(game.screen, WHITE, game.btn_go_restart_rect, 3) 
            btn_text = game.font_ui.render("START AGAIN", True, WHITE)
            game.screen.blit(btn_text, btn_text.get_rect(center=game.btn_go_restart_rect.center))
            
            can_load = os.path.exists("save.txt") and os.path.getsize("save.txt") > 0
            load_color = GREEN if can_load else DARK_GRAY
            
            pygame.draw.rect(game.screen, load_color, game.btn_go_load_rect)
            if can_load:
                pygame.draw.rect(game.screen, WHITE, game.btn_go_load_rect, 3)
            else:
                pygame.draw.rect(game.screen, DARK_GRAY, game.btn_go_load_rect, 3) 
                
            load_text_surf = game.font_ui.render("LOAD GAME", True, BLACK)
            game.screen.blit(load_text_surf, load_text_surf.get_rect(center=game.btn_go_load_rect.center))
            
        elif game.state == "PAUSED":
            overlay = pygame.Surface((game.width, game.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)) 
            game.screen.blit(overlay, (0, 0))
            
            pause_text = game.font_gameover.render("PAUSED", True, WHITE)
            game.screen.blit(pause_text, pause_text.get_rect(center=(game.width / 2, game.height / 2 - 50)))
            
            info_text = game.font_ui.render("ESC to continue", True, WHITE)
            game.screen.blit(info_text, info_text.get_rect(center=(game.width / 2, game.height / 2 + 10)))
            
            pygame.draw.rect(game.screen, RED, game.btn_return_menu_rect)
            pygame.draw.rect(game.screen, WHITE, game.btn_return_menu_rect, 3) 
            btn_text = game.font_ui.render("MAIN MENU", True, WHITE)
            game.screen.blit(btn_text, btn_text.get_rect(center=game.btn_return_menu_rect.center))
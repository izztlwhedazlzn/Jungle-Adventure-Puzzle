import pygame
import sys

# CONFIGURATIONS & INITIALIZATION
pygame.init()
pygame.font.init()

pygame.mixer.init()

# Background Music
pygame.mixer.music.load("assets/sounds/background.mp3")
pygame.mixer.music.set_volume(3)
pygame.mixer.music.play(-1)

click_sound = pygame.mixer.Sound("assets/sounds/select click.wav")
boat_sound = pygame.mixer.Sound("assets/sounds/boat splash.wav")
win_sound = pygame.mixer.Sound("assets/sounds/win.wav")
lose_sound = pygame.mixer.Sound("assets/sounds/gameover.wav")
enter_sound = pygame.mixer.Sound("assets/sounds/enter.wav")

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("River Crossing: Jungle Adventure")
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
BLUE = (65, 105, 225)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
RED = (220, 20, 60)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)

# Fonts
FONT_TITLE = pygame.font.SysFont("Verdana", 32, bold=True)
FONT_SUB = pygame.font.SysFont("Verdana", 22, bold=True)
FONT_BODY = pygame.font.SysFont("Verdana", 18)


#TRANSLATION DICTIONARY 
TEXTS = {
    "EN": {
        "title": "River Crossing: Jungle Adventure",
        "start": "1. Press ENTER to Start Game",
        "instr_btn": "2. Press I for Instructions",
        "lang_btn": "3. Press L to Change Language (Current: EN)",
        "exit_btn": "4. Press ESC to Exit",
        "instructions": "INSTRUCTIONS / RULES",
        "rule1": "- Boat capacity: Max 2 entities. Must be rowed by Explorer or Monkey.",
        "rule2": "- Tiger + Monkey alone = Tiger eats Monkey (LOSE).",
        "rule3": "- Monkey + Banana alone = Monkey eats Banana (LOSE).",
        "rule4": "- Move all entities safely across the river.",
        "back_menu": "Press BACKSPACE to return to Menu",
        "controls": "[1-5]: Load/Unload Entity | [SPACE]: Move Boat | [P]: Pause | [R]: Restart",
        "win": "CONGRATULATIONS!",
        "win_sub": "YOU WIN LEVEL ",
        "next_lvl": "Press ENTER for Next Level",
        "game_over": "GAME OVER!",
        "paused": "GAME PAUSED",
        "paused_sub": "Press P to Resume.",
        "score": "Score: ",
        "time": "Time Left: ",
        "level": "Level: "
    },
    "MS": {
        "title": "Kembara Menyeberang Sungai: Rimba",
        "start": "1. Tekan ENTER untuk Mula",
        "instr_btn": "2. Tekan I untuk Arahan",
        "lang_btn": "3. Tekan L to Tukar Bahasa (Semasa: MS)",
        "exit_btn": "4. Tekan ESC untuk Keluar",
        "instructions": "ARAHAN / PERATURAN",
        "rule1": "- Kapasiti Rakit: Maks 2 entiti. Mesti dikayuh oleh Explorer atau Monyet.",
        "rule2": "- Harimau + Monyet kendiri = Harimau makan Monyet (KALAH).",
        "rule3": "- Monyet + Pisang kendiri = Monyet makan Pisang (KALAH).",
        "rule4": "- Bawa semua entiti menyeberangi sungai dengan selamat.",
        "back_menu": "Tekan BACKSPACE untuk kembali ke Menu",
        "controls": "[1-5]: Naik/Turun Entiti | [SPACE]: Gerak Rakit | [P]: Jeda | [R]: Mula Semula",
        "win": "TAHNIAH!",
        "win_sub": "ANDA MENANG TAHAP ",
        "next_lvl": "Tekan ENTER untuk Tahap Seterusnya",
        "game_over": "PERMAINAN TAMAT!",
        "paused": "PERMAINAN DIJEDA",
        "paused_sub": "Tekan P untuk Sambung.",
        "score": "Skor: ",
        "time": "Masa: ",
        "level": "Tahap: "
    }
}

# CLASSES 

class Entity:
    def __init__(self, id_num, name, color, image_path=None):
        self.id = id_num
        self.name = name
        self.color = color
        self.side = "LEFT"
        self.width = 70
        self.height = 70
        self.x = 0
        self.y = 0
        
        self.image = None
        if image_path:
            try:
                loaded_img = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(loaded_img, (self.width, self.height))
            except Exception as e:
                print(f"Gagal muat imej {name} di {image_path}: {e}")

    def draw(self, surface, x, y):
        self.x = x
        self.y = y
        
        if self.image:
            surface.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), border_radius=10)
            pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height), 2, border_radius=10)
            txt = FONT_BODY.render(self.name[:3].upper(), True, BLACK if self.color != BLACK else WHITE)
            surface.blit(txt, (self.x + 15, self.y + 22))

class Boat:
    def __init__(self, image_path=None):
        self.side = "LEFT"
        self.passengers = []
        
        self.width = 250 
        self.height =  140
        self.x = 240
        self.y = 410       
        self.target_x = 240
        self.speed = 10
        
        self.image = None
        if image_path:
            try:
                loaded_img = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(loaded_img, (self.width, self.height))
            except Exception as e:
                print(f"Gagal muat imej bot di {image_path}: {e}")

    def move(self):
        if self.side == "LEFT":
            self.target_x = 240
        else:
            self.target_x = 540

        if self.x < self.target_x:
            self.x += self.speed
            if self.x > self.target_x: self.x = self.target_x
        elif self.x > self.target_x:
            self.x -= self.speed
            if self.x < self.target_x: self.x = self.target_x

    def is_moving(self):
        return self.x != self.target_x

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.polygon(surface, BROWN, [
                (self.x, self.y), 
                (self.x + self.width, self.y), 
                (self.x + self.width - 20, self.y + self.height), 
                (self.x + 20, self.y + self.height)
            ])
            pygame.draw.polygon(surface, BLACK, [
                (self.x, self.y), 
                (self.x + self.width, self.y), 
                (self.x + self.width - 20, self.y + self.height), 
                (self.x + 20, self.y + self.height)
            ], 2)

class GameManager:
    def __init__(self):
        self.lang = "EN"
        self.state = "MENU" 
        self.current_level = 1
        self.score = 0
        self.time_left = 120
        self.entities = []
        self.moves_count = 0
        self.reason_fail = ""
        
        self.background_image = None
        try:
            loaded_bg = pygame.image.load("assets/images/background.jpg").convert()
            self.background_image = pygame.transform.scale(loaded_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Gagal muat imej background: {e}")
            
        self.init_level()

    def init_level(self):
        self.boat = Boat("assets/images/boat.png")
        self.moves_count = 0
        self.reason_fail = ""
        
        if self.current_level == 1:
            self.time_left = 120
            self.entities = [
                Entity(1, "Explorer", YELLOW, "assets/images/explorer.png"),
                Entity(2, "Tiger", ORANGE, "assets/images/tiger.png"),
                Entity(3, "Monkey", GRAY, "assets/images/monkey.png"),
                Entity(4, "Banana", YELLOW, "assets/images/banana.png")
            ]
        elif self.current_level ==2:
            self.time_left = 120
            self.entities = [
                Entity(1, "Explorer", YELLOW, "assets/images/explorer.png"),
                Entity(2, "Tiger", ORANGE, "assets/images/tiger.png"),
                Entity(3, "Monkey", GRAY, "assets/images/monkey.png"),
                Entity(4, "Banana", YELLOW, "assets/images/banana.png"),
                Entity(5, "Treasure", RED, "assets/images/treasure.png")
]
        else:  
            self.time_left = 150
            self.entities = [
                Entity(1, "Explorer", YELLOW, "assets/images/explorer.png"),
                Entity(2, "Tiger", ORANGE, "assets/images/tiger.png"),
                Entity(3, "Monkey", GRAY, "assets/images/monkey.png"),
                Entity(4, "Banana", YELLOW, "assets/images/banana.png"),
                Entity(5, "Treasure", RED, "assets/images/treasure.png"),
                Entity(6, "Elephant", GREEN, "assets/images/elephant.png")
            ]
        if not pygame.mixer.music.get_busy():
         pygame.mixer.music.play(-1)

    def handle_load(self, entity_id):
        if self.boat.is_moving() or self.state != "PLAYING":
            return

        target = None
        for e in self.entities:
            if e.id == entity_id:
                target = e
                break
        if not target: return

        if target in self.boat.passengers:
            self.boat.passengers.remove(target)
            target.side = self.boat.side
            click_sound.play()
            self.check_rules()
        elif target.side == self.boat.side:
            if len(self.boat.passengers) < 2:
                self.boat.passengers.append(target)
                target.side = "BOAT"
                click_sound.play()

    def move_boat(self):
        if self.boat.is_moving() or self.state != "PLAYING":
            return

        has_driver = any(p.name in ["Explorer", "Monkey"] for p in self.boat.passengers)
        if not has_driver:
            return

        if self.boat.side == "LEFT":
            self.boat.side = "RIGHT"
        else:
            self.boat.side = "LEFT"
        
        boat_sound.play()
        self.moves_count += 1
        self.check_rules()

    def check_rules(self):
        left_side = [e.name for e in self.entities if e.side == "LEFT"]
        right_side = [e.name for e in self.entities if e.side == "RIGHT"]
        boat_side = [e.name for e in self.entities if e.side == "BOAT"]

        if "Explorer" not in left_side and not (self.boat.side == "LEFT" and "Explorer" in boat_side):
            if "Tiger" in left_side and "Monkey" in left_side:
                self.state = "GAMEOVER"
                pygame.mixer.music.stop()
                lose_sound.play()
                self.reason_fail = "Tiger ate Monkey!" if self.lang == "EN" else "Harimau makan Monyet!"
                return
            if "Monkey" in left_side and "Banana" in left_side:
                self.state = "GAMEOVER"
                pygame.mixer.music.stop()
                lose_sound.play()
                self.reason_fail = "Monkey ate Banana!" if self.lang == "EN" else "Monyet makan Pisang!"
                return
            
           
               

        if "Explorer" not in right_side and not (self.boat.side == "RIGHT" and "Explorer" in boat_side):
            if "Tiger" in right_side and "Monkey" in right_side:
                self.state = "GAMEOVER"
                pygame.mixer.music.stop()
                lose_sound.play()
                self.reason_fail = "Tiger ate Monkey!" if self.lang == "EN" else "Harimau makan Monyet!"
                return
            if "Monkey" in right_side and "Banana" in right_side:
                self.state = "GAMEOVER"
                pygame.mixer.music.stop()
                lose_sound.play()
                self.reason_fail = "Monkey ate Banana!" if self.lang == "EN" else "Monyet makan Pisang!"
                return

            
            

        all_landed_right = True
        for e in self.entities:
            if e.side != "RIGHT":
                all_landed_right = False
                break

        if all_landed_right and not self.boat.is_moving():
            level_bonus = self.current_level * 200
            self.score += int((self.time_left * 10) - (self.moves_count * 5) + level_bonus)
            pygame.mixer.music.stop()
            self.state = "WIN_STAGE"
            win_sound.play()

    def update_timer(self, dt):
        if self.state == "PLAYING":
            self.time_left -= dt
            if self.time_left <= 0:
                self.time_left = 0
                self.state = "GAMEOVER"
                lose_sound.play()
                self.reason_fail = "Time's Up!" if self.lang == "EN" else "Masa Tamat!"

    def draw_game(self, surface):
        if self.background_image:
         bg = self.background_image.copy()

         bg.set_alpha(120)
         surface.blit(bg, (0,0))

         soft_layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
         soft_layer.fill((255, 255, 255, 40))
         surface.blit(soft_layer, (0,0))

        else:
            surface.fill(GREEN)
            pygame.draw.rect(surface, BLUE, (250, 0, 500, SCREEN_HEIGHT))

        self.boat.move()
        self.boat.draw(surface)

        left_idx, right_idx = 0, 0
        for e in self.entities:
            if e.side == "LEFT":
                ex = 50 + (left_idx % 2) * 80
                ey = 220 + (left_idx // 2) * 110
                e.draw(surface, ex, ey)
                left_idx += 1
            elif e.side == "RIGHT":
                ex = 800 + (right_idx % 2) * 80
                ey = 250 + (right_idx // 2) * 110
                e.draw(surface, ex, ey)
                right_idx += 1
            elif e.side == "BOAT":
                b_idx = self.boat.passengers.index(e)
                # --- LARASAN KETINGGIAN IDEAL DI SINI ---
                spacing = 75  # jarak antara entity atas bot

                total_width = (len(self.boat.passengers) - 1) * spacing
                start_x = self.boat.x + (self.boat.width // 2) - (total_width // 2)

                ex = start_x + (b_idx * spacing)
                ey = self.boat.y + 5   # lebih natural duduk atas bot
                e.draw(surface, ex, ey)

        t = TEXTS[self.lang]
        lbl_lvl = FONT_SUB.render(f"{t['level']} {self.current_level}", True, BLACK)
        lbl_scr = FONT_SUB.render(f"{t['score']} {self.score}", True, BLACK)
        lbl_tim = FONT_SUB.render(f"{t['time']} {int(self.time_left)}s", True, RED if self.time_left < 20 else BLACK)
        lbl_ctrl = FONT_BODY.render(t["controls"], True, BLACK)
        lbl_move = FONT_SUB.render(f"Moves: {self.moves_count}", True, BLACK)
        max_time = 120 if self.current_level < 3 else 150

        pygame.draw.rect(surface, (200,200,200),
                (SCREEN_WIDTH-220, 60, 200, 20))

        remaining = int((self.time_left / max_time) * 200)

        pygame.draw.rect(surface, (0,255,0),
                (SCREEN_WIDTH-220, 60, remaining, 20))   
        surface.blit(lbl_lvl, (30, 20))
        surface.blit(lbl_scr, (30, 55))
        surface.blit(lbl_tim, (SCREEN_WIDTH - lbl_tim.get_width() - 20, 20))

        surface.blit(lbl_move, (30, 90))
        pygame.draw.rect(
        surface,
        (255, 255, 255),
        (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50),
        border_radius=10
)

        if self.current_level == 1:
            control_text = (
        "1-Explorer | 2-Tiger | 3-Monkey | 4-Banana | "
        "SPACE-Move | P-Pause | R-Restart"
    )
        elif self.current_level ==2:
            control_text = (
        "1-Explorer | 2-Tiger | 3-Monkey | 4-Banana | 5-Treasure | "
        "SPACE-Move | P-Pause | R-Restart"
    )
        else:
         control_text = (
        "1-Explorer | 2-Tiger | 3-Monkey | 4-Banana | 5-Treasure | 6-Elephant | "
        "SPACE-Move | P-Pause | R-Restart"
    )

        lbl_ctrl = FONT_BODY.render(control_text, True, BLACK)



        ctrl_rect = lbl_ctrl.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 25))
        surface.blit(lbl_ctrl, ctrl_rect)
        if self.state == "PAUSED":
            self.draw_multi_line_overlay(surface, [t["paused"], t["paused_sub"]])
        elif self.state == "GAMEOVER":
            self.draw_multi_line_overlay(surface, [t["game_over"], self.reason_fail, "Press R to Restart"])
        elif self.state == "WIN_STAGE":
            if self.current_level < 3:
                self.draw_multi_line_overlay(
                    surface, [t["win"], f"{t['win_sub']} {self.current_level} !", t["next_lvl"]])
            else:
                self.draw_multi_line_overlay(surface, ["ALL LEVELS CLEARED!", f"Final Score: {self.score}", "Press ENTER to return to Menu"])

    def draw_multi_line_overlay(self, surface, lines):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        
        start_y = SCREEN_HEIGHT // 2 - (len(lines) * 25)
        for i, line in enumerate(lines):
            font_used = FONT_TITLE if i == 0 else FONT_SUB
            txt_surface = font_used.render(line, True, YELLOW if i != 0 else ORANGE)
            rect = txt_surface.get_rect(center=(SCREEN_WIDTH // 2, start_y + (i * 55)))
            surface.blit(txt_surface, rect)

    def draw_menu(self, surface):
        if self.background_image:
            surface.blit(self.background_image, (0, 0))
        else:
            surface.fill(BLACK)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        surface.blit(overlay, (0, 0))

        t = TEXTS[self.lang]
        
        txt_title = FONT_TITLE.render(t["title"], True, GREEN)
        txt_start = FONT_SUB.render(t["start"], True, WHITE)
        txt_instr = FONT_SUB.render(t["instr_btn"], True, WHITE)
        txt_lang = FONT_SUB.render(t["lang_btn"], True, YELLOW)
        txt_exit = FONT_SUB.render(t["exit_btn"], True, RED)

        menu_box = pygame.Surface((700, 380), pygame.SRCALPHA)
        menu_box.fill((0, 0, 0, 150))
        surface.blit(menu_box, (150, 120))

        surface.blit(txt_title, (txt_title.get_rect(center=(SCREEN_WIDTH//2, 150))))
        surface.blit(txt_start, (txt_start.get_rect(center=(SCREEN_WIDTH//2, 280))))
        surface.blit(txt_instr, (txt_instr.get_rect(center=(SCREEN_WIDTH//2, 340))))
        surface.blit(txt_lang, (txt_lang.get_rect(center=(SCREEN_WIDTH//2, 400))))
        surface.blit(txt_exit, (txt_exit.get_rect(center=(SCREEN_WIDTH//2, 460))))

    def draw_instructions(self, surface):
        surface.fill(BLACK)
        t = TEXTS[self.lang]

        txt_title = FONT_TITLE.render(t["instructions"], True, GREEN)
        surface.blit(txt_title, (txt_title.get_rect(center=(SCREEN_WIDTH//2, 80))))

        r1 = FONT_SUB.render(t["rule1"], True, WHITE)
        r2 = FONT_SUB.render(t["rule2"], True, WHITE)
        r3 = FONT_SUB.render(t["rule3"], True, WHITE)
        r4 = FONT_SUB.render(t["rule4"], True, WHITE)
        back = FONT_BODY.render(t["back_menu"], True, YELLOW)

        surface.blit(r1, (80, 200))
        surface.blit(r2, (80, 260))
        surface.blit(r3, (80, 320))
        surface.blit(r4, (80, 380))
        surface.blit(back, (back.get_rect(center=(SCREEN_WIDTH//2, 550))))


def main():
    manager = GameManager()
    last_time = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()
        dt = (current_time - last_time) / 1000.0
        last_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if manager.state == "MENU":
                    if event.key == pygame.K_RETURN:
                        click_sound.play()
                        manager.state = "PLAYING"
                    elif event.key == pygame.K_i:
                        click_sound.play()
                        manager.state = "INSTRUCTIONS"
                    elif event.key == pygame.K_l:
                        click_sound.play()
                        manager.lang = "MS" if manager.lang == "EN" else "EN"
                    elif event.key == pygame.K_ESCAPE:
                        click_sound.play()
                        pygame.time.delay(200)
                        pygame.quit()
                        sys.exit()

                elif manager.state == "INSTRUCTIONS":
                    if event.key == pygame.K_BACKSPACE:
                        click_sound.play()
                        manager.state = "MENU"

                elif manager.state == "PLAYING":
                    if event.key == pygame.K_SPACE:
                        manager.move_boat()
                    elif event.key == pygame.K_p:
                        manager.state = "PAUSED"
                    elif event.key == pygame.K_r:
                        manager.init_level()
                    elif event.key == pygame.K_1: manager.handle_load(1)
                    elif event.key == pygame.K_2: manager.handle_load(2)
                    elif event.key == pygame.K_3: manager.handle_load(3)
                    elif event.key == pygame.K_4: manager.handle_load(4)
                    elif event.key == pygame.K_5: manager.handle_load(5)
                    elif event.key == pygame.K_6: manager.handle_load(6)

                elif manager.state == "PAUSED":
                    if event.key == pygame.K_p:
                        manager.state = "PLAYING"

                elif manager.state == "GAMEOVER":
                    if event.key == pygame.K_r:
                        manager.init_level()
                        manager.state = "PLAYING"

                elif manager.state == "WIN_STAGE":
                    if event.key == pygame.K_RETURN:
                        enter_sound.play()

                        if manager.current_level == 1:
                            manager.current_level = 2
                            manager.init_level()
                            manager.state = "PLAYING"

                        elif manager.current_level ==2:
                            manager.current_level = 3
                            manager.init_level()
                            manager.state = "PLAYING"
                        
                        else:
                            manager.current_level = 1
                            manager.score = 0
                            manager.init_level()
                            manager.state = "MENU"

        manager.update_timer(dt)

        if manager.state == "MENU":
            manager.draw_menu(screen)
        elif manager.state == "INSTRUCTIONS":
            manager.draw_instructions(screen)
        else:
            manager.draw_game(screen)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

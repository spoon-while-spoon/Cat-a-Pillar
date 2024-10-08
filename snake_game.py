import pygame
import random
import time
import sys
import os

# Pygame initialisieren
pygame.init()

# Bildschirmgröße
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Farben definieren
BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
CYBERPUNK_PURPLE = (199, 0, 255)
CYBERPUNK_BLUE = (0, 255, 255)
CYBERPUNK_GREEN = (0, 255, 0)
MATRIX_GREEN = (0, 255, 65)
DARK_GREY = (30, 30, 30)
LIGHT_GREY = (200, 200, 200)

# Schriftarten laden
font_small = pygame.font.SysFont('Arial', 25)
font_medium = pygame.font.SysFont('Arial', 35)
font_large = pygame.font.SysFont('Arial', 50)
matrix_font = pygame.font.SysFont('Courier', 15, bold=True)

# Bildschirm erstellen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake 2')

# Uhr erstellen
clock = pygame.time.Clock()

# Funktion zum Ermitteln des Speicherorts der Highscore-Dateien
def get_highscore_file_path(mode='classic', level=None):
    # Basisverzeichnis ermitteln
    if sys.platform == 'darwin':
        # macOS spezifisches Verzeichnis
        base_dir = os.path.expanduser('~/Library/Application Support/Snake 2')
    elif sys.platform.startswith('win'):
        # Windows-Verzeichnis
        base_dir = os.path.join(os.environ.get('APPDATA'), 'Snake 2')
    else:
        # Für andere Betriebssysteme, z. B. Linux
        base_dir = os.path.expanduser('~/.snake2')

    # Verzeichnis erstellen, falls es nicht existiert
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # Dateiname bestimmen
    if mode == 'classic':
        filename = 'highscores.txt'
    elif mode == 'fun' and level is not None:
        filename = f'highscores_level_{level}.txt'
    else:
        filename = 'highscores.txt'

    return os.path.join(base_dir, filename)

# Highscores laden
def load_highscores(mode='classic', level=None):
    highscores = []
    filepath = get_highscore_file_path(mode, level)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                if line.strip() == '':
                    continue
                name, score = line.strip().split(',')
                highscores.append((name, int(score)))
    return highscores

# Highscores speichern
def save_highscore(name, score, mode='classic', level=None):
    highscores = load_highscores(mode, level)
    highscores.append((name, score))
    highscores.sort(key=lambda x: x[1], reverse=True)
    highscores = highscores[:10]  # Top 10 speichern
    filepath = get_highscore_file_path(mode, level)
    with open(filepath, 'w') as f:
        for entry in highscores:
            f.write('{},{}\n'.format(entry[0], entry[1]))

# Highscores löschen
def clear_highscores():
    filepath_classic = get_highscore_file_path('classic')
    if os.path.exists(filepath_classic):
        os.remove(filepath_classic)
    for i in range(1, 6):
        filepath_fun = get_highscore_file_path('fun', i)
        if os.path.exists(filepath_fun):
            os.remove(filepath_fun)

# Prüfen, ob neuer Highscore
def is_new_highscore(score, mode='classic', level=None):
    highscores = load_highscores(mode, level)
    if len(highscores) < 10:
        return True
    elif score > highscores[-1][1]:
        return True
    return False

# Schwierigkeitsgrade
difficulty_levels = {
    'Einfach': {'speed': 10, 'point_value': 1, 'extra_time': 5},
    'Mittel': {'speed': 15, 'point_value': 2, 'extra_time': 4},
    'Schwer': {'speed': 20, 'point_value': 3, 'extra_time': 3},
    'Extrem': {'speed': 25, 'point_value': 4, 'extra_time': 2}
}

def main_menu():
    selected = 0
    menu_options = ['Spiel Starten', 'Fun Mode', 'Highscores Ansehen', 'Highscores Löschen', 'Beenden']

    while True:
        screen.fill(DARK_GREY)
        title = font_large.render("Snake 2", True, CYBERPUNK_GREEN)
        rect = title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
        screen.blit(title, rect)

        for idx, option in enumerate(menu_options):
            color = CYBERPUNK_GREEN if idx == selected else LIGHT_GREY
            text = font_medium.render(option, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + idx * 50))
            screen.blit(text, rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_options)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_options)
                if event.key == pygame.K_RETURN:
                    if selected == 0:
                        difficulty = select_difficulty()
                        if difficulty is not None:
                            main(difficulty=difficulty)
                    elif selected == 1:
                        select_fun_level()
                    elif selected == 2:
                        display_highscores()
                    elif selected == 3:
                        clear_highscores()
                        message("Highscores gelöscht!", CYBERPUNK_GREEN, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 200)
                        pygame.display.update()
                        time.sleep(1)
                    elif selected == 4:
                        pygame.quit()
                        sys.exit()

def main(mode='classic', level=None, difficulty=None):
    # Schwierigkeitsgrad auswählen, falls nicht übergeben
    if difficulty is None:
        difficulty = select_difficulty()
        if difficulty is None:
            return  # Benutzer hat zurück gedrückt

    # Startanimation
    matrix_animation()

    # Spiel initialisieren
    settings = difficulty_levels[difficulty]
    snake_speed = settings['speed']
    normal_speed = snake_speed  # Normalgeschwindigkeit speichern
    sprint_speed = snake_speed * 1.5  # Sprintgeschwindigkeit
    point_value = settings['point_value']
    extra_point_time = settings['extra_time']
    snake_block = 20

    # Sprint-Funktion Variablen
    sprint_active = False
    sprint_start_time = 0
    SPRINT_THRESHOLD = 0.2  # Sekunden

    # Snake-Startposition
    snake_list = []
    snake_length = 1
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    dx = snake_block  # Initiale Bewegung nach rechts
    dy = 0

    # Punktposition
    while True:
        food_x = round(random.randrange(0, SCREEN_WIDTH - snake_block) / 20.0) * 20.0
        food_y = round(random.randrange(0, SCREEN_HEIGHT - snake_block) / 20.0) * 20.0
        if [food_x, food_y] not in snake_list:
            break

    # Variablen für Extra-Punkte
    extra_food_visible = False
    extra_food_timer = 0
    extra_food_x = 0
    extra_food_y = 0
    points_since_last_extra = 0

    # Punktezahl
    score = 0

    # Für das "Essen" der Schlange
    growing_segments = []

    game_over = False
    game_close = False

    # Tastenstatus für Sprint-Funktion
    key_hold_start_time = None

    # Hindernisse für Fun Mode
    obstacles = []
    moving_obstacles = []
    if mode == 'fun':
        obstacles, moving_obstacles = generate_obstacles(level)

    # Feststellen, ob das Level eine Wand hat
    has_wall = False
    if mode == 'fun' and level in [1, 3]:
        has_wall = True

    while not game_over:

        while game_close:
            screen.fill(DARK_GREY)
            message("Game Over!", CYBERPUNK_PURPLE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50)
            message("Drücke Enter zum Fortfahren", WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 10)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_over = True
                        game_close = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        # Ereignisse verarbeiten
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause_screen()
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -snake_block
                    dy = 0
                    key_hold_start_time = time.time()
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = snake_block
                    dy = 0
                    key_hold_start_time = time.time()
                elif event.key == pygame.K_UP and dy == 0:
                    dy = -snake_block
                    dx = 0
                    key_hold_start_time = time.time()
                elif event.key == pygame.K_DOWN and dy == 0:
                    dy = snake_block
                    dx = 0
                    key_hold_start_time = time.time()
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    sprint_active = False
                    snake_speed = normal_speed
                    key_hold_start_time = None

        # Sprint-Funktion
        current_direction_key = None
        if dx == -snake_block:
            current_direction_key = pygame.K_LEFT
        elif dx == snake_block:
            current_direction_key = pygame.K_RIGHT
        elif dy == -snake_block:
            current_direction_key = pygame.K_UP
        elif dy == snake_block:
            current_direction_key = pygame.K_DOWN

        if current_direction_key and keys[current_direction_key]:
            if key_hold_start_time is None:
                key_hold_start_time = time.time()
            elif time.time() - key_hold_start_time >= SPRINT_THRESHOLD:
                sprint_active = True
                snake_speed = sprint_speed
        else:
            sprint_active = False
            snake_speed = normal_speed
            key_hold_start_time = None

        # Bewegung
        x += dx
        y += dy

        # Bildschirm verlassen und auf der anderen Seite erscheinen (wenn keine Wand)
        if not has_wall:
            if x >= SCREEN_WIDTH:
                x = 0
            elif x < 0:
                x = SCREEN_WIDTH - snake_block
            if y >= SCREEN_HEIGHT:
                y = 0
            elif y < 0:
                y = SCREEN_HEIGHT - snake_block
        else:
            # Im Fun Mode mit Wänden
            if x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
                game_close = True

        screen.fill(BLACK)

        # Hindernisse zeichnen
        for obstacle in obstacles:
            pygame.draw.rect(screen, LIGHT_GREY, obstacle)

        # Bewegliche Hindernisse aktualisieren und zeichnen
        for mobstacle in moving_obstacles:
            mobstacle.move()
            mobstacle.draw(screen)
            # Kollision mit beweglichen Hindernissen prüfen
            if mobstacle.rect.collidepoint(x, y):
                game_close = True

        # Punkt zeichnen (rund)
        pygame.draw.circle(screen, CYBERPUNK_GREEN, (int(food_x + snake_block / 2), int(food_y + snake_block / 2)), snake_block // 2)

        # Extra-Punkt
        if not extra_food_visible and points_since_last_extra >= 6:
            extra_food_visible = True
            extra_food_timer = time.time()
            while True:
                extra_food_x = round(random.randrange(0, SCREEN_WIDTH - snake_block) / 20.0) * 20.0
                extra_food_y = round(random.randrange(0, SCREEN_HEIGHT - snake_block) / 20.0) * 20.0
                new_food_rect = pygame.Rect(extra_food_x, extra_food_y, snake_block, snake_block)
                collision = any(new_food_rect.colliderect(obstacle) for obstacle in obstacles)
                collision |= any(new_food_rect.colliderect(mobstacle.rect) for mobstacle in moving_obstacles)
                if [extra_food_x, extra_food_y] not in snake_list and not collision:
                    break
        if extra_food_visible:
            time_left = extra_point_time - (time.time() - extra_food_timer)
            if time_left <= 0:
                extra_food_visible = False
                points_since_last_extra = 0
            else:
                # Blinkgeschwindigkeit erhöhen
                blink_frequency = max(0.1, time_left / extra_point_time)
                if (time.time() * (1 / blink_frequency)) % 2 < 1:
                    pygame.draw.circle(screen, CYBERPUNK_PURPLE, (int(extra_food_x + snake_block / 2), int(extra_food_y + snake_block / 2)), snake_block // 2)

        # Snake-Kopf und -Körper
        snake_head = [x, y]
        snake_list.append(snake_head)

        # Überprüfung auf Kollision mit sich selbst
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        # Überprüfung auf Kollision mit Hindernissen
        snake_rect = pygame.Rect(x, y, snake_block, snake_block)
        if any(snake_rect.colliderect(obstacle) for obstacle in obstacles):
            game_close = True

        # Schlange zeichnen
        draw_snake(snake_block, snake_list, growing_segments)

        # Punkte anzeigen
        display_score(score)

        # Überprüfung, ob Punkt gefressen wurde
        if x == food_x and y == food_y:
            while True:
                food_x = round(random.randrange(0, SCREEN_WIDTH - snake_block) / 20.0) * 20.0
                food_y = round(random.randrange(0, SCREEN_HEIGHT - snake_block) / 20.0) * 20.0
                new_food_rect = pygame.Rect(food_x, food_y, snake_block, snake_block)
                collision = any(new_food_rect.colliderect(obstacle) for obstacle in obstacles)
                collision |= any(new_food_rect.colliderect(mobstacle.rect) for mobstacle in moving_obstacles)
                if [food_x, food_y] not in snake_list and not collision:
                    break
            score += point_value
            points_since_last_extra += 1
            growing_segments.append(len(snake_list))

        # Überprüfung, ob Extra-Punkt gefressen wurde
        if extra_food_visible and x == extra_food_x and y == extra_food_y:
            extra_food_visible = False
            score += point_value * 3  # Dreifache Punkte
            points_since_last_extra = 0
            growing_segments.append(len(snake_list))

        # Bewegung der Verdickung entlang der Schlange
        for i in range(len(growing_segments)):
            growing_segments[i] -= 1

        # Überprüfen, ob die Verdickung das Ende erreicht hat
        while growing_segments and growing_segments[0] <= 0:
            snake_length += 1
            growing_segments.pop(0)

        # Schlange kürzen, falls nötig
        if len(snake_list) > snake_length:
            del snake_list[0]

        pygame.display.update()
        clock.tick(snake_speed)

    # Nach dem Spiel Highscore eingeben und anzeigen
    if is_new_highscore(score, mode, level):
        winner_animation()
        name = get_player_name()
        save_highscore(name, score, mode, level)
    else:
        message("Leider kein Highscore erreicht.", WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        pygame.display.update()
        time.sleep(2)
    display_highscores(mode, level)
    main_menu()

def draw_snake(snake_block, snake_list, growing_segments):
    for idx, segment in enumerate(snake_list):
        if idx == len(snake_list) - 1:
            # Kopf der Schlange (abgerundet)
            pygame.draw.rect(screen, CYBERPUNK_BLUE, [segment[0], segment[1], snake_block, snake_block], border_radius=5)
        else:
            # Prüfen, ob dieser Abschnitt verdickt ist
            distance_from_head = len(snake_list) - idx - 1
            if distance_from_head in growing_segments:
                # Verdickter Abschnitt
                thickness = snake_block + 4
                offset = -2
                pygame.draw.rect(screen, WHITE, [segment[0] + offset, segment[1] + offset, thickness, thickness])
            else:
                # Normales Segment
                pygame.draw.rect(screen, WHITE, [segment[0], segment[1], snake_block, snake_block])
    # Schwanz der Schlange (abgerundet)
    if len(snake_list) > 1:
        tail = snake_list[0]
        pygame.draw.rect(screen, WHITE, [tail[0], tail[1], snake_block, snake_block], border_radius=5)

def message(msg, color, x, y):
    mesg = font_medium.render(msg, True, color)
    rect = mesg.get_rect(center=(x, y))
    screen.blit(mesg, rect)

def display_score(score):
    value = font_small.render("Punkte: " + str(score), True, WHITE)
    screen.blit(value, [10, 10])

def select_difficulty():
    selecting = True
    difficulties = list(difficulty_levels.keys())
    selected = 0

    while selecting:
        screen.fill(DARK_GREY)
        title = font_large.render("Wähle einen Schwierigkeitsgrad", True, CYBERPUNK_GREEN)
        rect = title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
        screen.blit(title, rect)

        for idx, level in enumerate(difficulties):
            color = CYBERPUNK_GREEN if idx == selected else LIGHT_GREY
            text = font_medium.render(level, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + idx * 50))
            screen.blit(text, rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(difficulties)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(difficulties)
                if event.key == pygame.K_LEFT:
                    return None  # Benutzer möchte zurückgehen
                if event.key == pygame.K_RETURN:
                    return difficulties[selected]

def get_player_name():
    name = ""
    entering = True

    while entering:
        screen.fill(DARK_GREY)
        prompt = font_medium.render("Neuer Highscore! Gib deinen Namen ein:", True, WHITE)
        rect = prompt.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
        screen.blit(prompt, rect)

        name_surface = font_medium.render(name, True, CYBERPUNK_GREEN)
        rect = name_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(name_surface, rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name != "":
                    entering = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10 and event.unicode.isprintable():
                        name += event.unicode
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    return name

def display_highscores(mode='classic', level=None):
    highscores = load_highscores(mode, level)
    showing = True

    while showing:
        screen.fill(DARK_GREY)
        if mode == 'classic':
            title_text = "Highscores"
        else:
            title_text = f"Highscores - Level {level}"
        title = font_large.render(title_text, True, CYBERPUNK_GREEN)
        rect = title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6))
        screen.blit(title, rect)

        for idx, (name, score) in enumerate(highscores[:10]):
            text = font_medium.render(f"{idx+1}. {name} - {score}", True, LIGHT_GREY)
            rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3 + idx * 40))
            screen.blit(text, rect)

        message("Drücke eine Taste zum Fortfahren oder Linkspfeil zum Zurückgehen", WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 5 / 6)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    return  # Zurück zum Hauptmenü
                else:
                    showing = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def matrix_animation():
    # Parameter für die Animation
    columns = int(SCREEN_WIDTH / 10)
    drops = [0] * columns
    speed = 30  # Geschwindigkeit der Animation
    start_time = time.time()
    duration = 1.5  # Dauer der Animation in Sekunden

    characters = [chr(i) for i in range(33, 127)]  # ASCII-Zeichen

    while time.time() - start_time < duration:
        # Bildschirm etwas abdunkeln, um den "Regen"-Effekt zu erzeugen
        screen.fill((0, 0, 0, 10))

        for i in range(len(drops)):
            char = random.choice(characters)
            char_render = matrix_font.render(char, True, MATRIX_GREEN)
            x_pos = i * 10
            y_pos = drops[i] * 10

            screen.blit(char_render, (x_pos, y_pos))

            drops[i] += 1

            if drops[i] * 10 > SCREEN_HEIGHT or random.random() > 0.95:
                drops[i] = 0

        pygame.display.update()
        clock.tick(speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    # Am Ende der Animation den Bildschirm leeren
    screen.fill(BLACK)
    pygame.display.update()

def winner_animation():
    duration = 2  # Dauer der Animation in Sekunden
    start_time = time.time()
    while time.time() - start_time < duration:
        screen.fill(DARK_GREY)
        message("Neuer Highscore!", CYBERPUNK_PURPLE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def pause_screen():
    paused = True
    while paused:
        screen.fill(DARK_GREY)
        message("Pause", CYBERPUNK_GREEN, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        instructions = [
            "Spielsteuerung:",
            "- Pfeiltasten: Schlange bewegen",
            "- Leertaste: Pause",
            "- Sprint: Richtungstaste gedrückt halten",
            "",
            "Drücke Leertaste, um fortzufahren"
        ]
        for idx, line in enumerate(instructions):
            text = font_small.render(line, True, WHITE)
            rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + idx * 30))
            screen.blit(text, rect)

        pygame.display.update()
        clock.tick(5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False

def select_fun_level():
    levels = [
        "Level 1: Wand um das Spielfeld",
        "Level 2: Hindernisse auf dem Spielfeld",
        "Level 3: Wand & Hindernisse",
        "Level 4: Bewegliche Hindernisse",
        "Level 5: Zufällige Hindernisse"
    ]
    selected = 0
    selecting = True

    while selecting:
        screen.fill(DARK_GREY)
        title = font_large.render("Fun Mode - Wähle ein Level", True, CYBERPUNK_GREEN)
        rect = title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6))
        screen.blit(title, rect)

        for idx, level in enumerate(levels):
            color = CYBERPUNK_GREEN if idx == selected else LIGHT_GREY
            text = font_small.render(level, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3 + idx * 40))
            screen.blit(text, rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(levels)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(levels)
                if event.key == pygame.K_LEFT:
                    return  # Zurück zum Hauptmenü
                if event.key == pygame.K_RETURN:
                    difficulty = select_difficulty()
                    if difficulty is not None:
                        main(mode='fun', level=selected + 1, difficulty=difficulty)

def generate_obstacles(level):
    obstacles = []
    moving_obstacles = []
    snake_block = 20
    obstacle_size = snake_block * 3  # Größere Hindernisse (60x60 Pixel)
    if level == 1:
        # Wand um das Spielfeld (wird in main() behandelt)
        pass
    elif level == 2:
        # Feste Hindernisse auf dem Spielfeld
        for _ in range(5):
            x = round(random.randrange(0, SCREEN_WIDTH - obstacle_size) / 20.0) * 20.0
            y = round(random.randrange(0, SCREEN_HEIGHT - obstacle_size) / 20.0) * 20.0
            rect = pygame.Rect(x, y, obstacle_size, obstacle_size)
            obstacles.append(rect)
    elif level == 3:
        # Wand und Hindernisse
        for _ in range(5):
            x = round(random.randrange(0, SCREEN_WIDTH - obstacle_size) / 20.0) * 20.0
            y = round(random.randrange(0, SCREEN_HEIGHT - obstacle_size) / 20.0) * 20.0
            rect = pygame.Rect(x, y, obstacle_size, obstacle_size)
            obstacles.append(rect)
    elif level == 4:
        # Bewegliche Hindernisse
        for _ in range(3):
            x = round(random.randrange(0, SCREEN_WIDTH - obstacle_size) / 20.0) * 20.0
            y = round(random.randrange(0, SCREEN_HEIGHT - obstacle_size) / 20.0) * 20.0
            dx = random.choice([-snake_block // 2, snake_block // 2])
            dy = random.choice([-snake_block // 2, snake_block // 2])
            mobstacle = MovingObstacle(x, y, obstacle_size, obstacle_size, dx, dy)
            moving_obstacles.append(mobstacle)
    elif level == 5:
        # Zufällige Hindernisse, die während des Spiels erscheinen (Implementierung optional)
        pass  # Kann nach Bedarf implementiert werden
    return obstacles, moving_obstacles

class MovingObstacle:
    def __init__(self, x, y, width, height, dx, dy):
        self.rect = pygame.Rect(x, y, width, height)
        self.dx = dx
        self.dy = dy

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Randkollision prüfen und Richtung ändern
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.dx = -self.dx
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.dy = -self.dy

    def draw(self, screen):
        pygame.draw.rect(screen, LIGHT_GREY, self.rect)

if __name__ == "__main__":
    main_menu()

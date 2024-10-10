import pygame
import random
import time
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (200, 200, 0)
DARK_GREY = (30, 30, 30)
LIGHT_GREY = (200, 200, 200)

# Fonts
font_path = resource_path(os.path.join('assets', 'PressStart2P.ttf'))
try:
    retro_font = pygame.font.Font(font_path, 20)  # Use the bundled font file
except:
    retro_font = pygame.font.SysFont('Courier', 20)  # Fallback font

font_small = retro_font
font_medium = pygame.font.SysFont('Courier', 30)
font_large = pygame.font.SysFont('Courier', 50)
matrix_font = pygame.font.SysFont('Courier', 15, bold=True)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Cat-a-Pillar © M.Fischbach')

# Clock
clock = pygame.time.Clock()

# Load sounds
menu_music = resource_path(os.path.join('assets', 'menu.wav'))
game_music = resource_path(os.path.join('assets', 'game.wav'))

# Global variables to track if 'Autism' difficulty is unlocked and used
autism_unlocked = False
autism_used = False

# Function to get the highscore file path
def get_highscore_file_path(mode='classic', level=None):
    # Determine the base directory
    if sys.platform == 'darwin':
        # macOS specific directory
        base_dir = os.path.expanduser('~/Library/Application Support/catapillar')
    elif sys.platform.startswith('win'):
        # Windows directory
        base_dir = os.path.join(os.environ.get('APPDATA'), 'Catapillar')
    else:
        # For other operating systems, e.g., Linux
        base_dir = os.path.expanduser('~/.catapillar')

    # Create the directory if it doesn't exist
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # Determine the filename
    if mode == 'classic':
        filename = 'highscores.txt'
    elif mode == 'fun' and level is not None:
        filename = f'highscores_level_{level}.txt'
    else:
        filename = 'highscores.txt'

    return os.path.join(base_dir, filename)

# Highscore functions
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

def save_highscore(name, score, mode='classic', level=None):
    highscores = load_highscores(mode, level)
    highscores.append((name, score))
    highscores.sort(key=lambda x: x[1], reverse=True)
    highscores = highscores[:10]  # Keep top 10
    filepath = get_highscore_file_path(mode, level)
    with open(filepath, 'w') as f:
        for entry in highscores:
            f.write('{},{}\n'.format(entry[0], entry[1]))

def clear_highscores():
    filepath_classic = get_highscore_file_path('classic')
    if os.path.exists(filepath_classic):
        os.remove(filepath_classic)
    for i in range(1, 6):
        filepath_fun = get_highscore_file_path('fun', i)
        if os.path.exists(filepath_fun):
            os.remove(filepath_fun)

def is_new_highscore(score, mode='classic', level=None):
    highscores = load_highscores(mode, level)
    if len(highscores) < 10:
        return True
    elif score > highscores[-1][1]:
        return True
    return False

# Difficulty levels
difficulty_levels = {
    'Easy': {'speed': 10, 'point_value': 1, 'extra_time': 5},
    'Medium': {'speed': 20, 'point_value': 2, 'extra_time': 4},
    'Hard': {'speed': 25, 'point_value': 3, 'extra_time': 3},
    'Harder': {'speed': 30, 'point_value': 4, 'extra_time': 2},
    'Ridiculous': {'speed': 50, 'point_value': 6, 'extra_time': 2},
    'Autism': {'speed': 100, 'point_value': 10, 'extra_time': 1}
}

def start_screen():
    start = True
    # Animation variables
    title_y = SCREEN_HEIGHT // 4
    press_start_visible = True
    last_blink_time = time.time()
    blink_interval = 0.5  # Blink every 0.5 seconds

    while start:
        screen.fill(BLACK)
        
        # Display the game logo
        title = font_large.render("Cat-a-Pillar", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH / 2, title_y))
        screen.blit(title, title_rect)
        
        # Display the subtitle "© Martin Fischbach" unter dem Titel
        subtitle = font_small.render("© Martin Fischbach", True, GREEN)
        # Positioniere das Subtitle direkt unter dem Titel mit einem Abstand von 20 Pixeln
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH / 2, title_rect.bottom + 20))
        screen.blit(subtitle, subtitle_rect)

        # Blinking "Press Any Key to Start"
        if press_start_visible:
            prompt = font_small.render("Press Any Key to Start", True, WHITE)
            prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(prompt, prompt_rect)

        # Update the blinking
        current_time = time.time()
        if current_time - last_blink_time > blink_interval:
            press_start_visible = not press_start_visible
            last_blink_time = current_time

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                start = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def main_menu():
    global autism_unlocked, autism_used  # Declare globals to modify them

    # Play menu music
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play(-1)  # Loop indefinitely

    start_screen()  # Call the start screen before showing the main menu
    selected = 0
    menu_options = ['Start Game', 'Fun Mode', 'View Highscores', 'Clear Highscores', 'Exit']

    # Define the secret cheat code: Up, Right, Down, Left, Up, Right, Down, Left, Up, Right, Down, Left
    secret_code = [
        pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT,
        pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT,
        pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT
    ]
    input_sequence = []

    while True:
        screen.fill(BLACK)
        # **Änderung: Titel im Hauptmenü von "SnakeMF" zu "Cat-a-Pillar" geändert**
        title = font_large.render("Cat-a-Pillar", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6))
        screen.blit(title, title_rect)
        
        # **Änderung: Copyright-Text unter dem Titel hinzugefügt**
        copyright_text = font_small.render("© Martin Fischbach", True, GREEN)
        copyright_rect = copyright_text.get_rect(center=(SCREEN_WIDTH / 2, title_rect.bottom + 20))
        screen.blit(copyright_text, copyright_rect)

        for idx, option in enumerate(menu_options):
            color = GREEN if idx == selected else LIGHT_GREY
            text = font_small.render(option, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + idx * 40))
            screen.blit(text, rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Secret code detection
                input_sequence.append(event.key)
                # Keep the input_sequence length manageable
                if len(input_sequence) > len(secret_code):
                    input_sequence.pop(0)
                if input_sequence == secret_code:
                    # Unlock 'Autism' difficulty
                    if not autism_unlocked:
                        autism_unlocked = True
                        autism_used = False
                        message_display("Cheat Code Activated!\n'Autism' Difficulty Unlocked!", GREEN, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100)
                elif not secret_code[:len(input_sequence)] == input_sequence:
                    input_sequence = []

                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_options)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_options)
                if event.key == pygame.K_RETURN:
                    if selected == 0:
                        pygame.mixer.music.stop()
                        difficulty = select_difficulty()
                        if difficulty is not None:
                            main(mode='classic', difficulty=difficulty)
                            # Nach dem Spiel prüfen, ob 'Autism' gespielt wurde
                            if difficulty == 'Autism':
                                autism_unlocked = False  # Sperren nach einmaligem Spielen
                                autism_used = False
                        pygame.mixer.music.load(menu_music)
                        pygame.mixer.music.play(-1)
                    elif selected == 1:
                        pygame.mixer.music.stop()
                        select_fun_level()
                        pygame.mixer.music.load(menu_music)
                        pygame.mixer.music.play(-1)
                    elif selected == 2:
                        display_highscores()
                    elif selected == 3:
                        clear_highscores()
                        message("Highscores cleared!", GREEN, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 200)
                        pygame.display.update()
                        time.sleep(1)
                    elif selected == 4:
                        pygame.quit()
                        sys.exit()


def main(mode='classic', level=None, difficulty=None):
    # Play game music
    pygame.mixer.music.load(game_music)
    pygame.mixer.music.play(-1)

    # Initialize game variables
    if difficulty is None:
        difficulty = select_difficulty()
        if difficulty is None:
            return  # User pressed back

    settings = difficulty_levels[difficulty]
    snake_speed = settings['speed']
    normal_speed = snake_speed  # Store normal speed
    sprint_speed = snake_speed * 1.5  # Sprint speed
    point_value = settings['point_value']
    extra_point_time = settings['extra_time']
    snake_block = 20

    # Sprint variables
    sprint_active = False
    sprint_start_time = 0
    SPRINT_THRESHOLD = 0.2  # Seconds

    # Snake start position
    snake_list = []
    snake_length = 1
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    dx = snake_block  # Initial movement to the right
    dy = 0

    # Food position
    while True:
        food_x = round(random.randrange(0, SCREEN_WIDTH - snake_block) / 20.0) * 20.0
        food_y = round(random.randrange(0, SCREEN_HEIGHT - snake_block) / 20.0) * 20.0
        if [food_x, food_y] not in snake_list:
            break

    # Extra food variables
    extra_food_visible = False
    extra_food_timer = 0
    extra_food_x = 0
    extra_food_y = 0
    points_since_last_extra = 0

    # Score
    score = 0

    # Growing segments
    growing_segments = []

    game_over = False
    game_close = False

    # Key hold status for sprint
    key_hold_start_time = None

    # Obstacles for Fun Mode
    obstacles = []
    moving_obstacles = []
    if mode == 'fun':
        obstacles, moving_obstacles = generate_obstacles(level)

    # Check if level has walls
    has_wall = False
    if mode == 'fun' and level in [1, 3]:
        has_wall = True

    while not game_over:

        while game_close:
            screen.fill(BLACK)
            message("Game Over!", RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50)
            message("Press Enter to Continue", WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 10)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_over = True
                        game_close = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        # Event handling
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

        # Sprint functionality
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

        # Movement
        x += dx
        y += dy

        # Screen wrapping or collision with wall
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
            # In Fun Mode with walls
            if x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
                game_close = True

        screen.fill(BLACK)

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, LIGHT_GREY, obstacle)

        # Update and draw moving obstacles
        for mobstacle in moving_obstacles:
            mobstacle.move()
            mobstacle.draw(screen)
            # Collision with moving obstacles
            if mobstacle.rect.collidepoint(x, y):
                game_close = True

        # Draw food
        pygame.draw.circle(screen, GREEN, (int(food_x + snake_block / 2), int(food_y + snake_block / 2)), snake_block // 2)

        # Extra food
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
                # Calculate multiplier
                time_elapsed = time.time() - extra_food_timer
                time_fraction = time_elapsed / extra_point_time  # From 0 to 1
                max_multiplier = 6  # Maximum multiplier
                min_multiplier = 3  # Minimum multiplier
                multiplier = max_multiplier - (max_multiplier - min_multiplier) * time_fraction
                multiplier = max(multiplier, min_multiplier)  # Ensure at least min_multiplier

                # Blink frequency increases as time runs out
                blink_frequency = max(0.1, time_left / extra_point_time)
                if (time.time() * (1 / blink_frequency)) % 2 < 1:
                    pygame.draw.circle(screen, YELLOW, (int(extra_food_x + snake_block / 2), int(extra_food_y + snake_block / 2)), snake_block // 2)

        # Snake head and body
        snake_head = [x, y]
        snake_list.append(snake_head)

        # Collision with self
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        # Collision with obstacles
        snake_rect = pygame.Rect(x, y, snake_block, snake_block)
        if any(snake_rect.colliderect(obstacle) for obstacle in obstacles):
            game_close = True

        # Draw snake
        draw_snake(snake_block, snake_list, growing_segments)

        # Display score
        display_score(score)

        # Eating food
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
            growing_segments.append(0)  # Start thickening from the head

        # Eating extra food
        if extra_food_visible and x == extra_food_x and y == extra_food_y:
            extra_food_visible = False
            time_elapsed = time.time() - extra_food_timer
            time_fraction = time_elapsed / extra_point_time  # From 0 to 1
            max_multiplier = 6  # Maximum multiplier
            min_multiplier = 3  # Minimum multiplier
            multiplier = max(max_multiplier - (max_multiplier - min_multiplier) * time_fraction, min_multiplier)
            score += int(point_value * multiplier)
            points_since_last_extra = 0
            growing_segments.append(0)

        # Update growing_segments distances
        growing_segments = [distance + 1 for distance in growing_segments]

        # Remove segments that have reached the tail
        if growing_segments and growing_segments[0] >= len(snake_list):
            snake_length += 1
            growing_segments.pop(0)

        # Trim snake
        if len(snake_list) > snake_length:
            del snake_list[0]

        pygame.display.update()
        clock.tick(snake_speed)

    # After the game, enter highscore if applicable
    if is_new_highscore(score, mode, level):
        winner_animation()
        name = get_player_name()
        save_highscore(name, score, mode, level)
    else:
        message("No Highscore Achieved.", WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        pygame.display.update()
        time.sleep(2)
    # Stop game music when returning to menu
    pygame.mixer.music.stop()
    display_highscores(mode, level)
    main_menu()


def retro_mode():
    # Retro Graphics Mode
    # Play game music
    pygame.mixer.music.load(game_music)
    pygame.mixer.music.play(-1)

    # Use smaller screen size for retro feel
    retro_screen_width = 400
    retro_screen_height = 300
    retro_block_size = 10

    # Adjust the display
    retro_screen = pygame.Surface((retro_screen_width, retro_screen_height))

    # Initialize game variables specific to retro mode
    x = retro_screen_width / 2
    y = retro_screen_height / 2
    dx = retro_block_size
    dy = 0
    snake_list = []
    snake_length = 1

    # Food position
    food_x = round(random.randrange(0, retro_screen_width - retro_block_size) / retro_block_size) * retro_block_size
    food_y = round(random.randrange(0, retro_screen_height - retro_block_size) / retro_block_size) * retro_block_size

    game_over = False
    game_close = False

    snake_speed = 10  # Fixed speed for retro mode

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            message("Game Over!", RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            pygame.display.update()
            time.sleep(2)
            game_over = True
            game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -retro_block_size
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = retro_block_size
                    dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dy = -retro_block_size
                    dx = 0
                elif event.key == pygame.K_DOWN and dy == 0:
                    dy = retro_block_size
                    dx = 0

        x += dx
        y += dy

        # Boundary collision
        if x >= retro_screen_width or x < 0 or y >= retro_screen_height or y < 0:
            game_close = True

        # Self-collision
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        # Eating food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, retro_screen_width - retro_block_size) / retro_block_size) * retro_block_size
            food_y = round(random.randrange(0, retro_screen_height - retro_block_size) / retro_block_size) * retro_block_size
            snake_length += 1

        # Drawing everything on the retro screen
        retro_screen.fill(BLACK)
        for segment in snake_list:
            pygame.draw.rect(retro_screen, WHITE, [segment[0], segment[1], retro_block_size, retro_block_size])
        pygame.draw.rect(retro_screen, GREEN, [food_x, food_y, retro_block_size, retro_block_size])

        # Scaling up the retro screen to the main screen
        scaled_screen = pygame.transform.scale(retro_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_screen, (0, 0))

        pygame.display.update()
        clock.tick(snake_speed)

    # Stop game music when returning to menu
    pygame.mixer.music.stop()


def draw_snake(snake_block, snake_list, growing_segments):
    for idx, segment in enumerate(snake_list):
        # Calculate distance from head
        distance_from_head = len(snake_list) - idx - 1
        if distance_from_head in growing_segments:
            # Thickened segment
            thickness = snake_block + 4
            offset = -2
            pygame.draw.rect(screen, YELLOW, [segment[0] + offset, segment[1] + offset, thickness, thickness])
        else:
            # Normal segment
            pygame.draw.rect(screen, WHITE, [segment[0], segment[1], snake_block, snake_block])

    # Draw the head (rounded)
    head = snake_list[-1]
    pygame.draw.rect(screen, RED, [head[0], head[1], snake_block, snake_block], border_radius=5)

    # Draw the tail (rounded)
    if len(snake_list) > 1:
        tail = snake_list[0]
        pygame.draw.rect(screen, WHITE, [tail[0], tail[1], snake_block, snake_block], border_radius=5)


def message(msg, color, x, y):
    mesg = font_medium.render(msg, True, color)
    rect = mesg.get_rect(center=(x, y))
    screen.blit(mesg, rect)


def message_display(msg, color, x, y):
    """Displays a multi-line message."""
    lines = msg.split('\n')
    for idx, line in enumerate(lines):
        mesg = font_medium.render(line, True, color)
        rect = mesg.get_rect(center=(x, y + idx * 40))
        screen.blit(mesg, rect)
    pygame.display.update()
    time.sleep(2)  # Display the message for 2 seconds


def display_score(score):
    value = font_small.render("Score: " + str(score), True, WHITE)
    screen.blit(value, [10, 10])


def select_difficulty():
    global autism_unlocked, autism_used  # Access global variables
    selecting = True
    # Build the list of difficulties based on whether 'Autism' is unlocked
    difficulties = list(difficulty_levels.keys())
    if not autism_unlocked:
        difficulties.remove('Autism')
    selected = 0

    # Variables for blinking effect
    autism_blink_visible = True
    last_blink_time = time.time()
    blink_interval = 0.5  # Blink every 0.5 seconds

    while selecting:
        screen.fill(BLACK)
        title = font_large.render("Select Difficulty", True, GREEN)
        rect = title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
        screen.blit(title, rect)

        for idx, level in enumerate(difficulties):
            if level == 'Autism' and autism_unlocked:
                # Handle blinking effect for 'Autism'
                current_time = time.time()
                if current_time - last_blink_time > blink_interval:
                    autism_blink_visible = not autism_blink_visible
                    last_blink_time = current_time
                if autism_blink_visible:
                    color = YELLOW if idx == selected else LIGHT_GREY
                else:
                    color = BLACK  # Invisible when not visible
            else:
                color = GREEN if idx == selected else LIGHT_GREY
            text = font_small.render(level, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + idx * 40))
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
                    return None  # User wants to go back
                if event.key == pygame.K_RETURN:
                    return difficulties[selected]


def get_player_name():
    name = ""
    entering = True

    while entering:
        screen.fill(BLACK)
        prompt = font_medium.render("New Highscore! Enter your name:", True, WHITE)
        rect = prompt.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
        screen.blit(prompt, rect)

        name_surface = font_medium.render(name, True, GREEN)
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
        screen.fill(BLACK)
        if mode == 'classic':
            title_text = "Highscores"
        else:
            title_text = f"Highscores - Level {level}"
        title = font_large.render(title_text, True, GREEN)
        rect = title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6))
        screen.blit(title, rect)

        for idx, (name, score) in enumerate(highscores[:10]):
            text = font_small.render(f"{idx+1}. {name} - {score}", True, LIGHT_GREY)
            rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3 + idx * 30))
            screen.blit(text, rect)

        message("Press any key to continue", WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 5 / 6)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                showing = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def select_fun_level():
    levels = [
        "Level 1: Wall around the playing field",
        "Level 2: Obstacles on the playing field",
        "Level 3: Wall & Obstacles",
        "Level 4: Moving Obstacles",
        "Level 5: Random Obstacles"
    ]
    selected = 0
    selecting = True

    while selecting:
        screen.fill(BLACK)
        title = font_large.render("Fun Mode - Select Level", True, GREEN)
        rect = title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6))
        screen.blit(title, rect)

        for idx, level in enumerate(levels):
            color = GREEN if idx == selected else LIGHT_GREY
            text = font_small.render(level, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3 + idx * 30))
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
                    return  # Go back to main menu
                if event.key == pygame.K_RETURN:
                    difficulty = select_difficulty()
                    if difficulty is not None:
                        main(mode='fun', level=selected + 1, difficulty=difficulty)


def generate_obstacles(level):
    obstacles = []
    moving_obstacles = []
    snake_block = 20
    obstacle_size = snake_block * 3  # Larger obstacles (60x60 pixels)
    if level == 1:
        # Wall around the playing field (handled in main())
        pass
    elif level == 2:
        # Static obstacles on the field
        for _ in range(5):
            x = round(random.randrange(0, SCREEN_WIDTH - obstacle_size) / 20.0) * 20.0
            y = round(random.randrange(0, SCREEN_HEIGHT - obstacle_size) / 20.0) * 20.0
            rect = pygame.Rect(x, y, obstacle_size, obstacle_size)
            obstacles.append(rect)
    elif level == 3:
        # Wall and obstacles
        for _ in range(5):
            x = round(random.randrange(0, SCREEN_WIDTH - obstacle_size) / 20.0) * 20.0
            y = round(random.randrange(0, SCREEN_HEIGHT - obstacle_size) / 20.0) * 20.0
            rect = pygame.Rect(x, y, obstacle_size, obstacle_size)
            obstacles.append(rect)
    elif level == 4:
        # Moving obstacles
        for _ in range(3):
            x = round(random.randrange(0, SCREEN_WIDTH - obstacle_size) / 20.0) * 20.0
            y = round(random.randrange(0, SCREEN_HEIGHT - obstacle_size) / 20.0) * 20.0
            dx = random.choice([-snake_block // 2, snake_block // 2])
            dy = random.choice([-snake_block // 2, snake_block // 2])
            mobstacle = MovingObstacle(x, y, obstacle_size, obstacle_size, dx, dy)
            moving_obstacles.append(mobstacle)
    elif level == 5:
        # Random obstacles (implement as needed)
        pass
    return obstacles, moving_obstacles


class MovingObstacle:
    def __init__(self, x, y, width, height, dx, dy):
        self.rect = pygame.Rect(x, y, width, height)
        self.dx = dx
        self.dy = dy

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Check for boundary collision and change direction
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.dx = -self.dx
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.dy = -self.dy

    def draw(self, screen):
        pygame.draw.rect(screen, LIGHT_GREY, self.rect)


def pause_screen():
    paused = True
    while paused:
        screen.fill(BLACK)
        message("Paused", GREEN, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        instructions = [
            "Game Controls:",
            "- Arrow Keys: Move Snake",
            "- Spacebar: Pause",
            "- Sprint: Hold Direction Key",
            "",
            "Press Spacebar to Continue"
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


def winner_animation():
    duration = 2  # Duration in seconds
    start_time = time.time()
    while time.time() - start_time < duration:
        screen.fill(BLACK)
        message("New Highscore!", YELLOW, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main_menu()

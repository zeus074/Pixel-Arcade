import machine
import neopixel
import time
import random

# --- IMPOSTAZIONI HARDWARE ---
NEOPIXEL_PIN = 2; MATRIX_WIDTH = 16; MATRIX_HEIGHT = 16; NUM_PIXELS = MATRIX_WIDTH * MATRIX_HEIGHT
BUTTON_LEFT_PIN = 16; BUTTON_RIGHT_PIN = 17; BUTTON_ACCELERATE_PIN = 18
BUTTON_BRAKE_PIN = 19; BUTTON_START_PIN = 20; BUZZER_PIN = 21

# --- INIZIALIZZAZIONE HARDWARE ---
pixels = neopixel.NeoPixel(machine.Pin(NEOPIXEL_PIN), NUM_PIXELS)
btn_left = machine.Pin(BUTTON_LEFT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
btn_right = machine.Pin(BUTTON_RIGHT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
btn_accelerate = machine.Pin(BUTTON_ACCELERATE_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
btn_brake = machine.Pin(BUTTON_BRAKE_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
btn_start = machine.Pin(BUTTON_START_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
buzzer = machine.PWM(machine.Pin(BUZZER_PIN)); buzzer.duty_u16(0)

# --- FONT 3x5 PIXEL ---
FONT = {
    'A': [0b111, 0b101, 0b111, 0b101, 0b101], 'B': [0b110, 0b101, 0b110, 0b101, 0b110],
    'C': [0b011, 0b100, 0b100, 0b100, 0b011], 'D': [0b110, 0b101, 0b101, 0b101, 0b110],
    'E': [0b111, 0b100, 0b110, 0b100, 0b111], 'F': [0b111, 0b100, 0b110, 0b100, 0b100],
    'G': [0b011, 0b100, 0b101, 0b101, 0b011], 'H': [0b101, 0b101, 0b111, 0b101, 0b101],
    'I': [0b111, 0b010, 0b010, 0b010, 0b111], 'J': [0b001, 0b001, 0b001, 0b101, 0b111],
    'L': [0b100, 0b100, 0b100, 0b100, 0b111], 'M': [0b101, 0b111, 0b111, 0b101, 0b101],
    'N': [0b101, 0b111, 0b111, 0b111, 0b101], 'O': [0b010, 0b101, 0b101, 0b101, 0b010],
    'P': [0b110, 0b101, 0b110, 0b100, 0b100], 'R': [0b110, 0b101, 0b110, 0b101, 0b101],
    'S': [0b011, 0b100, 0b010, 0b001, 0b110], 'T': [0b111, 0b010, 0b010, 0b010, 0b010],
    'U': [0b101, 0b101, 0b101, 0b101, 0b111], 'V': [0b101, 0b101, 0b101, 0b010, 0b010],
    'Y': [0b101, 0b101, 0b010, 0b010, 0b010], 'Z': [0b111, 0b001, 0b010, 0b100, 0b111],
    '0': [0b111, 0b101, 0b101, 0b101, 0b111], '1': [0b010, 0b110, 0b010, 0b010, 0b111],
    '2': [0b111, 0b001, 0b111, 0b100, 0b111], '3': [0b111, 0b001, 0b111, 0b001, 0b111],
    '4': [0b101, 0b101, 0b111, 0b001, 0b001], '5': [0b111, 0b100, 0b111, 0b001, 0b111],
    '6': [0b111, 0b100, 0b111, 0b101, 0b111], '7': [0b111, 0b001, 0b010, 0b010, 0b010],
    '8': [0b111, 0b101, 0b111, 0b101, 0b111], '9': [0b111, 0b101, 0b111, 0b001, 0b111],
    ' ': [0b000, 0b000, 0b000, 0b000, 0b000],
}
image_data = [
    (6, 90, 0),     (0, 0, 0),     (138, 95, 54),     (138, 95, 54),     (0, 0, 0),     (138, 95, 54),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (138, 95, 54),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (138, 95, 54),     (138, 95, 54),     (0, 0, 0),
    (0, 0, 0),     (138, 95, 54),     (0, 0, 0),     (138, 95, 54),     (0, 0, 0),     (138, 95, 54),     (0, 0, 0),     (138, 95, 54),     (0, 0, 0),     (138, 95, 54),     (0, 0, 0),     (0, 0, 0),     (138, 95, 54),     (0, 0, 0),     (6, 90, 0),     (6, 90, 0),
    (6, 90, 0),     (0, 0, 0),     (138, 95, 54),     (138, 95, 54),     (0, 0, 0),     (0, 0, 0),     (138, 95, 54),     (0, 0, 0),     (138, 95, 54),     (138, 95, 54),     (138, 95, 54),     (0, 0, 0),     (0, 0, 0),     (138, 95, 54),     (138, 95, 54),     (0, 0, 0),
    (0, 0, 0),     (138, 95, 54),     (0, 0, 0),     (138, 95, 54),     (0, 0, 0),     (138, 95, 54),     (0, 0, 0),     (138, 95, 54),     (0, 0, 0),     (138, 95, 54),     (0, 0, 0),     (0, 0, 0),     (138, 95, 54),     (0, 0, 0),     (6, 90, 0),     (6, 90, 0),
    (6, 90, 0),     (0, 0, 0),     (138, 95, 54),     (138, 95, 54),     (0, 0, 0),     (138, 95, 54),     (0, 0, 0),     (0, 0, 0),     (138, 95, 54),     (0, 0, 0),     (138, 95, 54),     (0, 0, 0),     (138, 95, 54),     (0, 0, 0),     (138, 95, 54),     (0, 0, 0),
    (6, 90, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (6, 90, 0),     (6, 90, 0),
    (6, 90, 0),     (6, 90, 0),     (6, 90, 0),     (72, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (32, 26, 35),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (72, 0, 0),     (6, 90, 0),
    (6, 90, 0),     (151, 142, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (32, 26, 35),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (151, 142, 0),     (6, 90, 0),     (6, 90, 0),     (6, 90, 0),
    (6, 90, 0),     (6, 90, 0),     (6, 90, 0),     (72, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (32, 26, 35),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (72, 0, 0),     (6, 90, 0),
    (6, 90, 0),     (151, 142, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (32, 26, 35),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (151, 142, 0),     (6, 90, 0),     (6, 90, 0),     (6, 90, 0),
    (6, 90, 0),     (6, 90, 0),     (72, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (32, 26, 35),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (72, 0, 0),     (6, 90, 0),     (6, 90, 0),
    (6, 90, 0),     (6, 90, 0),     (151, 142, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (32, 26, 35),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (151, 142, 0),     (6, 90, 0),     (6, 90, 0),
    (6, 90, 0),     (6, 90, 0),     (72, 0, 0),     (0, 0, 0),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (0, 0, 0),     (32, 26, 35),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (72, 0, 0),     (6, 90, 0),     (6, 90, 0),
    (6, 90, 0),     (6, 90, 0),     (151, 142, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (32, 26, 35),     (0, 0, 0),     (155, 155, 155),     (155, 155, 155),     (155, 155, 155),     (0, 0, 0),     (151, 142, 0),     (6, 90, 0),     (6, 90, 0),
    (6, 90, 0),     (6, 90, 0),     (72, 0, 0),     (0, 0, 0),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (0, 0, 0),     (32, 26, 35),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (72, 0, 0),     (6, 90, 0),     (6, 90, 0),
    (6, 90, 0),     (6, 90, 0),     (151, 142, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (32, 26, 35),     (0, 0, 0),     (155, 155, 155),     (155, 155, 155),     (155, 155, 155),     (0, 0, 0),     (151, 142, 0),     (6, 90, 0),     (6, 90, 0),
]
# --- COSTANTI DI GIOCO ---
BLACK = (0, 0, 0); WHITE = (20, 20, 20); RED = (25, 0, 0); YELLOW = (25, 15, 0)
GREEN = (0, 25, 0); BLUE_OIL = (0, 0, 25); GRAY = (10, 10, 10); HUD_SPEED_COLOR = (0, 15, 25)
LIVES_COLOR = (20, 0, 25)

PLAYER_WIDTH = 3; PLAYER_HEIGHT = 4; PLAYER_Y_POS = MATRIX_HEIGHT - PLAYER_HEIGHT

MAX_SPEED = 100.0; ACCELERATION = 2.0; BRAKING = 5.0; NATURAL_DECELERATION = 0.5
MAX_LATERAL_SPEED = 1.5; CURVE_FORCE = 0.2; OIL_SLICK_EFFECT = 0.4
MIN_SPEED_TO_SLIDE = 40.0

INITIAL_ROAD_WIDTH = 9; MIN_ROAD_WIDTH = 8; MAX_ROAD_WIDTH = 14
INITIAL_LIVES = 3

# --- VARIABILI DI STATO GLOBALI ---
game_state = 'START_SCREEN'
player_x = 0; speed = 0.0; score = 0; lives = 0
road_data = []; obstacles = []
last_scroll_time = 0; road_scroll_interval = 500
on_oil_slick = 0
road_direction_momentum = 0
straight_road_counter = 0
last_rock_side = 'none'
plaza_mode_active = False
plaza_timer = 0
np = neopixel.NeoPixel(machine.Pin(NEOPIXEL_PIN), NUM_PIXELS)

# --- FUNZIONI HELPER ---
def xy_to_index(x, y):
    if x < 0 or x >= MATRIX_WIDTH or y < 0 or y >= MATRIX_HEIGHT: return -1
    if y % 2 == 0: return y * MATRIX_WIDTH + (MATRIX_WIDTH - 1 - x)
    else: return y * MATRIX_WIDTH + x

def clear_display(): pixels.fill(BLACK)

def play_tone(frequency, duration_ms, volume=32768):
    if frequency > 0: buzzer.freq(frequency); buzzer.duty_u16(volume)
    time.sleep_ms(duration_ms)
    buzzer.duty_u16(0)

# <<< MODIFICA: Logica di respawn sicura corretta
def find_safe_spawn_x():
    """Scansiona la corsia per trovare una coordinata X sicura per il respawn."""
    road_left, road_right = road_data[-1]
    lane_center = (road_left + road_right) / 2
    
    # Calcola la x ideale del giocatore per essere al centro
    ideal_player_x = int(lane_center - (PLAYER_WIDTH / 2))
    
    # Crea una lista di posizioni da controllare, partendo da quella ideale
    positions_to_check = [ideal_player_x]
    for offset in range(1, MATRIX_WIDTH // 2):
        positions_to_check.append(ideal_player_x - offset)
        positions_to_check.append(ideal_player_x + offset)
        
    for x_pos in positions_to_check:
        is_safe = True
        
        # 1. Controlla se la posizione è valida per la larghezza dello schermo
        if x_pos < 0 or x_pos + PLAYER_WIDTH > MATRIX_WIDTH:
            continue
            
        # 2. Controlla che l'intero corpo dell'auto sia dentro i bordi della strada
        for y_offset in range(PLAYER_HEIGHT):
            y = PLAYER_Y_POS + y_offset
            if not (0 <= y < len(road_data)): continue
            
            row_left_border, row_right_border = road_data[y]
            player_left_edge = x_pos
            player_right_edge = x_pos + PLAYER_WIDTH - 1
            
            if player_left_edge < row_left_border or player_right_edge > row_right_border:
                is_safe = False
                break
        if not is_safe: continue

        # 3. Controlla che il corpo non collida con ostacoli
        player_rect = (x_pos, PLAYER_Y_POS, PLAYER_WIDTH, PLAYER_HEIGHT)
        for obs in obstacles:
            if (player_rect[0] <= obs['x'] < player_rect[0] + player_rect[2] and
                player_rect[1] <= obs['y'] < player_rect[1] + player_rect[3]):
                is_safe = False
                break
        if not is_safe: continue
        
        # Se tutti i controlli sono passati, abbiamo trovato una posizione sicura
        return x_pos

    # Failsafe: se nessuna posizione è sicura, restituisce comunque la posizione ideale
    return ideal_player_x

# --- FUNZIONI DI DISEGNO ---
def draw_text(text, start_x, y, color):
    current_x = start_x
    for char in text.upper():
        if char in FONT:
            char_data = FONT[char]
            for row, bits in enumerate(char_data):
                for col in range(3):
                    if (bits >> (2 - col)) & 1:
                        idx = xy_to_index(current_x + col, y + row)
                        if idx != -1: pixels[idx] = color
            current_x += 4

def draw_road():
    # (invariato)
    for y, row in enumerate(road_data):
        left_border, right_border = row
        for x in range(MATRIX_WIDTH):
            idx = xy_to_index(x, y);
            if idx == -1: continue
            if x < left_border or x > right_border: pixels[idx] = GREEN
            elif x == left_border or x == right_border: pixels[idx] = RED if (y + int(score / 10)) % 2 == 0 else YELLOW
            else: pixels[idx] = BLACK
    for obs in obstacles:
        idx = xy_to_index(obs['x'], obs['y']);
        if idx != -1: pixels[idx] = GRAY if obs['type'] == 'rock' else BLUE_OIL

def draw_player():
    # (invariato)
    car_color = WHITE
    if on_oil_slick > 0 and (time.ticks_ms() // 100) % 2 == 0: car_color = BLUE_OIL
    for y_offset in range(PLAYER_HEIGHT):
        for x_offset in range(PLAYER_WIDTH):
            is_part_of_car = True
            if y_offset == 0 and (x_offset == 0 or x_offset == 2): is_part_of_car = False
            elif y_offset == 2 and (x_offset == 0 or x_offset == 2): is_part_of_car = False
            if is_part_of_car:
                px = int(player_x) + x_offset; py = PLAYER_Y_POS + y_offset
                idx = xy_to_index(px, py)
                if idx != -1: pixels[idx] = car_color

def draw_hud():
    # (invariato)
    for i in range(lives): pixels[xy_to_index(i, 0)] = LIVES_COLOR
    speed_bar_width = int((speed / MAX_SPEED) * (MATRIX_WIDTH / 2))
    for i in range(speed_bar_width): pixels[xy_to_index(MATRIX_WIDTH - 1 - i, 0)] = HUD_SPEED_COLOR


# --- FUNZIONI DI LOGICA DI GIOCO ---
def reset_game():
    global player_x, speed, score, lives, road_data, obstacles, game_state, on_oil_slick, road_direction_momentum, straight_road_counter, last_rock_side, plaza_mode_active, plaza_timer
    player_x = MATRIX_WIDTH / 2 - PLAYER_WIDTH / 2
    speed = 0.0; score = 0; lives = INITIAL_LIVES; on_oil_slick = 0
    road_direction_momentum = 0; straight_road_counter = 0; last_rock_side = 'none'
    plaza_mode_active = False; plaza_timer = 0
    road_data = []; obstacles = []
    center = MATRIX_WIDTH // 2; width = INITIAL_ROAD_WIDTH // 2
    for _ in range(MATRIX_HEIGHT): road_data.append((center - width, center + width))
    game_state = 'PLAYING'
    play_tone(880, 50); play_tone(1047, 100)

def update_road():
    # (invariato)
    global road_data, obstacles, score, road_direction_momentum, straight_road_counter, last_rock_side, plaza_mode_active, plaza_timer
    road_data.pop()
    obstacles = [obs for obs in obstacles if obs['y'] < MATRIX_HEIGHT - 1]
    for obs in obstacles: obs['y'] += 1
    last_left, last_right = road_data[0]
    new_left, new_right = last_left, last_right
    current_width = new_right - new_left
    if plaza_mode_active:
        plaza_timer -= 1
        if plaza_timer <= 0: plaza_mode_active = False
        if current_width < MAX_ROAD_WIDTH:
            new_left = max(0, new_left - 1)
            new_right = min(MATRIX_WIDTH - 1, new_right + 1)
    else:
        difficulty_factor = min(1.0, score / 1000)
        if random.random() < 0.25 + (difficulty_factor * 0.1):
            momentum_change = random.choice([-1, 0, 0, 1])
            road_direction_momentum += momentum_change
            road_direction_momentum = max(-2, min(2, road_direction_momentum))
        if road_direction_momentum != 0:
            actual_shift = 1 if road_direction_momentum > 0 else -1
            new_left += actual_shift; new_right += actual_shift
            straight_road_counter = 0; last_rock_side = 'none'
        else:
            straight_road_counter += 1
            if random.random() < 0.20:
                width_change = random.choice([-1, 0, 1, 1, 1])
                new_width = (new_right - new_left) + width_change
                if MIN_ROAD_WIDTH <= new_width <= MAX_ROAD_WIDTH:
                    new_left -= width_change; new_right += width_change
            if straight_road_counter > 25 and random.random() < 0.1:
                plaza_mode_active = True
                plaza_timer = random.randint(30, 50)
    new_left = max(0, min(new_left, MATRIX_WIDTH - MIN_ROAD_WIDTH))
    new_right = min(MATRIX_WIDTH - 1, max(new_left + MIN_ROAD_WIDTH - 1, new_right))
    road_data.insert(0, (new_left, new_right))
    if (straight_road_counter > 10 or plaza_mode_active) and speed > 30:
        spawn_type = None
        chance_mod = 1.5 if plaza_mode_active else 1.0
        if random.random() < (0.25 * chance_mod): spawn_type = 'rock'
        elif random.random() < (0.15 * chance_mod): spawn_type = 'oil'
        if spawn_type == 'rock':
            if last_rock_side == 'none': last_rock_side = random.choice(['left', 'right'])
            side_to_place = last_rock_side
            lane_center = new_left + ((new_right - new_left) // 2)
            if side_to_place == 'left':
                obs_x = random.randint(new_left + 1, lane_center - 1) if lane_center - 1 > new_left else new_left + 1
            else:
                obs_x = random.randint(lane_center + 1, new_right - 1) if new_right - 1 > lane_center else new_right - 1
            obstacles.insert(0, {'type': 'rock', 'x': obs_x, 'y': 0})
        elif spawn_type == 'oil':
            obs_x = random.randint(new_left + 1, new_right - 1)
            obstacles.insert(0, {'type': 'oil', 'x': obs_x, 'y': 0})

def handle_input():
    # (invariato)
    global player_x, speed, on_oil_slick
    move_speed = (speed / MAX_SPEED) * MAX_LATERAL_SPEED
    if btn_accelerate.value() == 0: move_speed = max(move_speed, 0.4)
    if on_oil_slick > 0 and random.random() < OIL_SLICK_EFFECT: move_speed = 0
    if btn_left.value() == 0 and player_x > 0: player_x -= move_speed
    if btn_right.value() == 0 and player_x < MATRIX_WIDTH - PLAYER_WIDTH: player_x += move_speed
    if btn_accelerate.value() == 0: speed = min(MAX_SPEED, speed + ACCELERATION)
    elif btn_brake.value() == 0: speed = max(0, speed - BRAKING)
    else: speed = max(0, speed - NATURAL_DECELERATION)

def update_game_state():
    # (invariato)
    global player_x, lives, game_state, score, on_oil_slick
    road_front_y = PLAYER_Y_POS; road_back_y = PLAYER_Y_POS + PLAYER_HEIGHT - 1
    if 0 <= road_front_y < len(road_data) and 0 <= road_back_y < len(road_data):
        road_center_front = (road_data[road_front_y][0] + road_data[road_front_y][1]) / 2
        road_center_back = (road_data[road_back_y][0] + road_data[road_back_y][1]) / 2
        curve_direction = road_center_front - road_center_back
        if abs(curve_direction) > 0.5 and speed > MIN_SPEED_TO_SLIDE:
            player_x -= curve_direction * CURVE_FORCE * (speed / MAX_SPEED)
    if on_oil_slick > 0:
        if random.random() < 0.5: player_x += random.choice([-1, 1]) * 0.5
        on_oil_slick -= 1
        if on_oil_slick == 0: play_tone(600, 50)
    player_x = max(0, min(player_x, MATRIX_WIDTH - PLAYER_WIDTH))
    player_left = int(player_x); player_right = int(player_x + PLAYER_WIDTH - 1)
    crashed = False
    for y_offset in range(PLAYER_HEIGHT):
        y = PLAYER_Y_POS + y_offset
        if 0 <= y < len(road_data):
            road_left, road_right = road_data[y]
            if player_left < road_left or player_right > road_right: crashed = True; break
    if crashed: handle_crash(); return
    player_rect = (int(player_x), PLAYER_Y_POS, PLAYER_WIDTH, PLAYER_HEIGHT)
    for obs in list(obstacles):
        if (player_rect[0] <= obs['x'] < player_rect[0] + player_rect[2] and
            player_rect[1] <= obs['y'] < player_rect[1] + player_rect[3]):
            if obs['type'] == 'rock': handle_crash(crashed_obstacle=obs); return
            elif obs['type'] == 'oil':
                if on_oil_slick == 0: on_oil_slick = 30; play_tone(220, 150)
                obstacles.remove(obs)
    if speed > 1: score += speed / 50.0

def handle_crash(crashed_obstacle=None):
    global lives, game_state, speed, player_x, on_oil_slick
    lives -= 1; speed = 0; buzzer.duty_u16(0)
    if crashed_obstacle and crashed_obstacle in obstacles: obstacles.remove(crashed_obstacle)
    player_center_x = int(player_x + PLAYER_WIDTH / 2); player_center_y = int(PLAYER_Y_POS + PLAYER_HEIGHT / 2)
    for i in range(5):
        idx_crash = xy_to_index(player_center_x, player_center_y)
        if idx_crash != -1: pixels[idx_crash] = RED if i % 2 == 0 else BLACK
        pixels.write(); play_tone(300 - i * 40, 50)
    if lives <= 0: game_state = 'GAME_OVER'
    else:
        player_x = find_safe_spawn_x() # <<< MODIFICA: Usa la nuova funzione
        on_oil_slick = 0; time.sleep_ms(1000)

# --- SCHERMATE DI STATO ---
def show_image(image):
    for i in range(256):
        np[i] = image[i]
    np.write()
    return False
        

def show_start_screen():
    # (invariato)
    show_image(image_data)
    while btn_start.value() == 1:
        if not btn_start.value() and not btn_accelerate.value() and not btn_brake.value():
            machine.reset() #torno al menù
        time.sleep_ms(10)
        if not btn_start.value() and not btn_accelerate.value() and not btn_brake.value():
            machine.reset() #torno al menù

def show_game_over_screen():
    # (invariato)
    global game_state
    buzzer.duty_u16(0)
    play_tone(440, 100); play_tone(349, 100); play_tone(261, 200)
    clear_display()
    draw_text("SCORE", 0, 2, RED)
    score_str = str(int(score))
    score_x = (MATRIX_WIDTH - (len(score_str) * 4 - 1)) // 2
    draw_text(score_str, score_x, 9, YELLOW)
    pixels.write()
    time.sleep(5)
    game_state = 'START_SCREEN'

# --- CICLO DI GIOCO PRINCIPALE ---
while True:
    # (invariato)
    if game_state == 'START_SCREEN':
        show_start_screen()
        reset_game()
    elif game_state == 'PLAYING':
        current_time = time.ticks_ms()
        handle_input()
        update_game_state()
        if game_state != 'PLAYING': continue
        if speed > 0:
            max_interval = 1000; min_interval = 20
            road_scroll_interval = max_interval - (speed / MAX_SPEED) * (max_interval - min_interval)
            if time.ticks_diff(current_time, last_scroll_time) > road_scroll_interval:
                update_road()
                last_scroll_time = current_time
        if speed > 1:
            engine_freq = int(80 + (speed / MAX_SPEED) * 150)
            buzzer.freq(engine_freq); buzzer.duty_u16(5000)
        else:
            buzzer.duty_u16(0)
        clear_display()
        draw_road(); draw_player(); draw_hud()
        pixels.write()
        time.sleep_ms(20)
    elif game_state == 'GAME_OVER':
        show_game_over_screen()
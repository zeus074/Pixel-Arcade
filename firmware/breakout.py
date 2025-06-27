import machine
import neopixel
import time
import random

# --- Configurazione Hardware ---
NEOPIXEL_PIN = 2
BUTTON_LEFT_PIN = 16
BUTTON_RIGHT_PIN = 17
BUTTON_FIRE_PIN = 18
BUTTON_FIRE2_PIN = 19
BUTTON_START_PIN = 20
BUZZER_PIN = 21

# --- Configurazione Display ---
MATRIX_WIDTH = 16
MATRIX_HEIGHT = 16
NUM_PIXELS = MATRIX_WIDTH * MATRIX_HEIGHT

# --- Inizializzazione Hardware ---
np = neopixel.NeoPixel(machine.Pin(NEOPIXEL_PIN), NUM_PIXELS)
btn_left = machine.Pin(BUTTON_LEFT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
btn_right = machine.Pin(BUTTON_RIGHT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
btn_start = machine.Pin(BUTTON_START_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
btn_fire = machine.Pin(BUTTON_FIRE_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
btn_fire2 = machine.Pin(BUTTON_FIRE2_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
buzzer = machine.PWM(machine.Pin(BUZZER_PIN))
buzzer.duty_u16(0)

# --- Configurazione Gioco ---
# Colori
BLACK = (0, 0, 0); WHITE = (30, 30, 30); RED = (30, 0, 0)
BLUE = (0, 0, 30); YELLOW = (30, 30, 0); ORANGE = (35, 15, 0)
MAGENTA = (30, 0, 30); CYAN = (0, 30, 30); GREEN = (0, 30, 0)
PADDLE_COLOR = BLUE; BALL_COLOR = WHITE; LIFE_COLOR = (20, 0, 0)
SCORE_COLOR = YELLOW
BRICK_COLORS = [MAGENTA, RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, (15,0,20)]

image_data = [
    (115, 23, 86),     (0, 0, 0),     (115, 23, 86),     (0, 0, 0),     (1, 10, 125),     (1, 10, 125),     (0, 0, 0),     (72, 1, 1),     (72, 1, 1),     (72, 1, 1),     (0, 0, 0),     (123, 13, 0),     (0, 0, 0),     (0, 0, 0),     (53, 129, 0),     (53, 129, 0),
    (53, 129, 0),     (0, 0, 0),     (53, 129, 0),     (0, 0, 0),     (123, 13, 0),     (0, 0, 0),     (72, 1, 1),     (0, 0, 0),     (72, 1, 1),     (0, 0, 0),     (1, 10, 125),     (0, 0, 0),     (0, 0, 0),     (115, 23, 86),     (0, 0, 0),     (115, 23, 86),
    (0, 0, 0),     (115, 23, 86),     (115, 23, 86),     (0, 0, 0),     (0, 0, 0),     (1, 10, 125),     (0, 0, 0),     (72, 1, 1),     (0, 0, 0),     (72, 1, 1),     (0, 0, 0),     (123, 13, 0),     (0, 0, 0),     (0, 0, 0),     (53, 129, 0),     (53, 129, 0),
    (53, 129, 0),     (0, 0, 0),     (53, 129, 0),     (0, 0, 0),     (123, 13, 0),     (0, 0, 0),     (72, 1, 1),     (0, 0, 0),     (72, 1, 1),     (0, 0, 0),     (1, 10, 125),     (0, 0, 0),     (0, 0, 0),     (115, 23, 86),     (0, 0, 0),     (115, 23, 86),
    (115, 23, 86),     (0, 0, 0),     (115, 23, 86),     (0, 0, 0),     (1, 10, 125),     (1, 10, 125),     (0, 0, 0),     (72, 1, 1),     (72, 1, 1),     (0, 0, 0),     (123, 13, 0),     (123, 13, 0),     (0, 0, 0),     (0, 0, 0),     (53, 129, 0),     (53, 129, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (80, 80, 80),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (1, 10, 125),     (1, 55, 155),     (1, 55, 155),     (1, 55, 155),     (1, 55, 155),     (1, 10, 125),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
]

# Layout Pala e Vite
PADDLE_WIDTH = 3
PADDLE_Y = MATRIX_HEIGHT - 2
LIVES_Y = MATRIX_HEIGHT - 1
paddle_x = (MATRIX_WIDTH - PADDLE_WIDTH) // 2

# Palla
ball_pos = {'x': 8.0, 'y': 10.0}
ball_vel = {'x': 0.0, 'y': 0.0}
# ########################################################################### #
# MODIFICA: Aumento velocità iniziale
# ########################################################################### #
INITIAL_SPEED_MS = 60 # Valore più basso = più veloce
MIN_SPEED_MS = 25
game_speed_ms = INITIAL_SPEED_MS

# Mattoncini e Punteggio
bricks = []; BRICK_ROWS = 8; BRICK_WIDTH = 2
score = 0; lives = 3
game_state = "START_SCREEN"

# ########################################################################### #
# NOVITÀ: Font a pixel per visualizzare il punteggio
# ########################################################################### #
FONT = {
    '0': [(0,0),(0,1),(0,2),(0,3),(0,4), (1,0),(1,4), (2,0),(2,1),(2,2),(2,3),(2,4)],
    '1': [(1,0),(1,1),(1,2),(1,3),(1,4), (0,1)],
    '2': [(0,0),(1,0),(2,0), (2,1),(2,2), (0,2),(1,2), (0,3), (0,4),(1,4),(2,4)],
    '3': [(0,0),(1,0),(2,0), (2,1),(2,2), (1,2), (2,3), (0,4),(1,4),(2,4)],
    '4': [(0,0),(0,1),(0,2), (1,2), (2,0),(2,1),(2,2),(2,3),(2,4)],
    '5': [(0,0),(1,0),(2,0), (0,1), (0,2),(1,2),(2,2), (2,3), (0,4),(1,4),(2,4)],
    '6': [(0,0),(1,0),(2,0), (0,1), (0,2),(1,2),(2,2), (0,3),(0,4), (2,3),(2,4),(1,4)],
    '7': [(0,0),(1,0),(2,0), (2,1),(2,2),(2,3),(2,4)],
    '8': [(0,0),(1,0),(2,0), (0,1),(2,1), (1,2), (0,3),(2,3), (0,4),(1,4),(2,4)],
    '9': [(0,0),(1,0),(2,0), (0,1),(2,1), (0,2),(1,2),(2,2), (2,3), (2,4)]
}
# --- Funzioni di Utilità ---
def clear_matrix(): np.fill(BLACK)
def xy_to_index(x, y):
    x, y = int(x), int(y)
    if y % 2 == 0: return y * MATRIX_WIDTH + (MATRIX_WIDTH - 1 - x)
    else: return y * MATRIX_WIDTH + x
def draw_pixel(x, y, color):
    if 0 <= x < MATRIX_WIDTH and 0 <= y < MATRIX_HEIGHT:
        np[xy_to_index(x, y)] = color
def play_tone(freq, duration_ms):
    if freq > 0:
        buzzer.freq(freq); buzzer.duty_u16(32768); time.sleep_ms(duration_ms)
    buzzer.duty_u16(0)

# --- Funzioni di Gioco ---
def setup_bricks():
    global bricks; bricks.clear()
    for row in range(BRICK_ROWS):
        for col in range(MATRIX_WIDTH // BRICK_WIDTH):
            bricks.append({'x': col * BRICK_WIDTH, 'y': row, 'width': BRICK_WIDTH, 'color': BRICK_COLORS[row], 'active': True})

def reset_ball_and_paddle():
    global paddle_x, ball_pos, ball_vel, game_speed_ms
    paddle_x = (MATRIX_WIDTH - PADDLE_WIDTH) // 2
    ball_pos['x'] = float(random.randint(6, 9)); ball_pos['y'] = float(PADDLE_Y - 3)
    ball_vel['x'] = random.choice([-0.5, 0.5]); ball_vel['y'] = -0.5
    game_speed_ms = min(INITIAL_SPEED_MS, game_speed_ms + 5)

def start_new_game():
    global lives, score, game_state, game_speed_ms
    lives = 3; score = 0
    game_speed_ms = INITIAL_SPEED_MS
    setup_bricks(); reset_ball_and_paddle()
    game_state = "PLAYING"
    play_tone(1318, 50); play_tone(1568, 80)

def draw_number(number_str, start_x, start_y, color):
    """Disegna un numero usando il FONT a pixel."""
    offset_x = 0
    for char in number_str:
        if char in FONT:
            for (px, py) in FONT[char]:
                draw_pixel(start_x + offset_x + px, start_y + py, color)
            offset_x += 4 # Spazio tra le cifre (3 di larghezza + 1 di spazio)

def show_final_score():
    """Mostra la schermata del punteggio finale."""
    clear_matrix()
    score_str = str(score)
    # Calcola la posizione iniziale per centrare il numero
    text_width = len(score_str) * 4 - 1
    start_x = (MATRIX_WIDTH - text_width) // 2
    draw_number(score_str, start_x, 6, SCORE_COLOR)
    np.write()
    play_tone(1046, 100); time.sleep_ms(120); play_tone(1318, 100); time.sleep_ms(120); play_tone(1568, 200)
    time.sleep(4) # Mostra il punteggio per 4 secondi

def draw_game():
    clear_matrix()
    for brick in bricks:
        if brick['active']:
            for i in range(brick['width']): draw_pixel(brick['x'] + i, brick['y'], brick['color'])
    for i in range(PADDLE_WIDTH): draw_pixel(paddle_x + i, PADDLE_Y, PADDLE_COLOR)
    draw_pixel(ball_pos['x'], ball_pos['y'], BALL_COLOR)
    for i in range(lives): draw_pixel(i, LIVES_Y, LIFE_COLOR)
    np.write()
    
# --- Ciclo Principale del Gioco ---
while True:
    def show_image(image):
        for i in range(256):
            np[i] = image[i]
        np.write()
        return False

    if game_state == "START_SCREEN":
        #draw_game() # Mostra una demo statica
        #clear_matrix()
        #draw_number("5", 6, 6, WHITE) # Lettera S per Start
        #np.write()
        show_image(image_data)
        if not btn_start.value() and not btn_fire.value() and not btn_fire2.value():
            machine.reset() #torno al menù
            
        if btn_start.value() == 0: start_new_game()
            
    elif game_state == "PLAYING":
        # 1. Input
        if btn_left.value() == 0 and paddle_x > 0: paddle_x -= 1
        if btn_right.value() == 0 and paddle_x < (MATRIX_WIDTH - PADDLE_WIDTH): paddle_x += 1
            
        # 2. Logica
        if game_speed_ms > MIN_SPEED_MS: game_speed_ms -= 0.02
        
        ball_pos['x'] += ball_vel['x']; ball_pos['y'] += ball_vel['y']
        ball_ix, ball_iy = int(ball_pos['x']), int(ball_pos['y'])

        # Collisioni Muri (con anti-incastramento)
        if ball_pos['x'] <= 0: ball_pos['x'] = 0; ball_vel['x'] *= -1; play_tone(600, 15)
        elif ball_pos['x'] >= MATRIX_WIDTH - 1: ball_pos['x'] = MATRIX_WIDTH - 1.1; ball_vel['x'] *= -1; play_tone(600, 15)
        if ball_pos['y'] <= 0: ball_pos['y'] = 0; ball_vel['y'] *= -1; play_tone(600, 15)
            
        # ########################################################################### #
        # MODIFICA: Correzione rimbalzo sulla pala
        # ########################################################################### #
        if ball_vel['y'] > 0 and ball_iy == PADDLE_Y and paddle_x <= ball_ix < paddle_x + PADDLE_WIDTH:
            play_tone(987, 20)
            ball_pos['y'] = PADDLE_Y - 0.1 # Spinge la palla appena sopra la pala
            ball_vel['y'] *= -1
            if ball_ix == paddle_x: ball_vel['x'] = -0.7 # Angolo più aggressivo
            elif ball_ix == paddle_x + 1: ball_vel['x'] *= 0.5 # Colpo centrale smorzato
            else: ball_vel['x'] = 0.7

        # Collisione Mattoncini
        bricks_left = False
        for brick in bricks:
            if brick['active']:
                bricks_left = True
                if brick['y'] == ball_iy and brick['x'] <= ball_ix < brick['x'] + brick['width']:
                    play_tone(1396, 20); brick['active'] = False; score += 10
                    ball_pos['y'] += -ball_vel['y']; ball_vel['y'] *= -1
                    break
        
        # Livello Superato
        if not bricks_left:
            play_tone(1568, 250); setup_bricks(); reset_ball_and_paddle()
            game_speed_ms = max(MIN_SPEED_MS, game_speed_ms - 10)
            
        # Palla Persa
        if ball_pos['y'] >= MATRIX_HEIGHT:
            lives -= 1
            if lives <= 0: game_state = "GAME_OVER"; play_tone(440, 200); time.sleep_ms(50); play_tone(330, 300)
            else:
                if game_speed_ms <= INITIAL_SPEED_MS-5: game_speed_ms -= 5 # reimposto la velocità, ma solo un tantino
                play_tone(523, 200); time.sleep(1); reset_ball_and_paddle()

        # 3. Disegno e Pausa
        draw_game()
        time.sleep_ms(int(game_speed_ms))
        
    elif game_state == "GAME_OVER":
        show_final_score()
        game_state = "START_SCREEN"
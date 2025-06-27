import machine
import neopixel
import time
import random

# --- Configurazione Hardware ---
NEOPIXEL_PIN = 2
# Giocatore 1 (in basso)
P1_LEFT_PIN = 16
P1_RIGHT_PIN = 17
# Giocatore 2 (in alto)
P2_LEFT_PIN = 18
P2_RIGHT_PIN = 19
# Tasto Start/Servizio
START_PIN = 20
BUZZER_PIN = 21

# --- Configurazione Display e Gioco ---
MATRIX_WIDTH = 16; MATRIX_HEIGHT = 16; NUM_PIXELS = MATRIX_WIDTH * MATRIX_HEIGHT

# Colori
BLACK = (0, 0, 0); BALL_COLOR = (40, 40, 40)
P1_COLOR = (0, 35, 0); P2_COLOR = (0, 0, 35) # Verde per G1, Blu per G2
WINNER_COLOR = (40, 30, 0) # Giallo oro per il vincitore

# Parametri di Gioco
PADDLE_WIDTH = 3
P1_Y = MATRIX_HEIGHT - 2 # Pala G1 sulla penultima riga
P2_Y = 0                 # Pala G2 sulla prima riga
WINNING_SCORE = 5
INITIAL_SPEED_MS = 60 # Più basso = più veloce
MIN_SPEED_MS = 5

# --- Inizializzazione Hardware ---
np = neopixel.NeoPixel(machine.Pin(NEOPIXEL_PIN), NUM_PIXELS)
p1_left = machine.Pin(P1_LEFT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
p1_right = machine.Pin(P1_RIGHT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
p2_left = machine.Pin(P2_LEFT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
p2_right = machine.Pin(P2_RIGHT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
btn_start = machine.Pin(START_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
buzzer = machine.PWM(machine.Pin(BUZZER_PIN)); buzzer.duty_u16(0)

# --- FONT per il messaggio di vittoria ---
FONT = { '1':[(1,0),(1,1),(1,2),(1,3),(1,4),(0,1)], '2':[(0,0),(1,0),(2,0),(2,1),(2,2),(0,2),(1,2),(0,3),(0,4),(1,4),(2,4)] }

image_data = [
    (155, 155, 155),     (155, 155, 155),     (0, 0, 0),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (155, 155, 155),     (155, 155, 155),
    (155, 155, 155),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (155, 155, 155),     (155, 155, 155),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (155, 155, 155),     (155, 155, 155),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (155, 155, 155),
    (155, 155, 155),     (155, 155, 155),     (0, 0, 0),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (155, 155, 155),
    (155, 155, 155),     (155, 155, 155),     (0, 0, 0),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (155, 155, 155),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (155, 155, 155),     (155, 155, 155),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (1, 55, 155),     (1, 55, 155),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (155, 155, 155),     (155, 155, 155),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (123, 13, 0),     (123, 13, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (123, 13, 0),     (123, 13, 0),     (123, 13, 0),     (123, 13, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (1, 55, 155),     (1, 55, 155),     (1, 55, 155),     (1, 55, 155),     (0, 0, 0),
    (0, 0, 0),     (1, 55, 155),     (1, 55, 155),     (1, 55, 155),     (1, 55, 155),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (123, 13, 0),     (123, 13, 0),     (123, 13, 0),     (123, 13, 0),     (0, 0, 0),
    (0, 0, 0),     (123, 13, 0),     (123, 13, 0),     (123, 13, 0),     (123, 13, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (1, 55, 155),     (1, 55, 155),     (1, 55, 155),     (1, 55, 155),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (1, 55, 155),     (1, 55, 155),     (155, 155, 155),     (155, 155, 155),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (155, 155, 155),     (155, 155, 155),     (123, 13, 0),     (123, 13, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (155, 155, 155),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
]

# --- Variabili Globali di Gioco ---
game_state = "START_SCREEN" # START_SCREEN, PRE_SERVE, PLAYING, GAME_OVER
p1_paddle = {'x': (MATRIX_WIDTH - PADDLE_WIDTH) // 2}
p2_paddle = {'x': (MATRIX_WIDTH - PADDLE_WIDTH) // 2}
ball = {'x': 0, 'y': 0, 'vx': 0, 'vy': 0}
p1_score = 0; p2_score = 0
serving_player = 1
game_speed_ms = INITIAL_SPEED_MS

# --- Funzioni di Utilità e Setup ---
def xy_to_index(x, y):
    x_int, y_int = int(x), int(y)
    if y_int % 2 == 0: return y_int * MATRIX_WIDTH + (MATRIX_WIDTH - 1 - x_int)
    else: return y_int * MATRIX_WIDTH + x_int

# MODIFICA: Aggiunto controllo di sicurezza per prevenire crash
def draw_pixel(x, y, color):
    # Controlla se le coordinate sono valide prima di disegnare
    if 0 <= x < MATRIX_WIDTH and 0 <= y < MATRIX_HEIGHT:
        np[xy_to_index(x, y)] = color
        
def play_tone(freq, dur): buzzer.freq(freq); buzzer.duty_u16(1024); time.sleep_ms(dur); buzzer.duty_u16(0)

def start_new_game():
    global p1_score, p2_score, serving_player, game_state, game_speed_ms
    p1_score = 0; p2_score = 0
    serving_player = 1 # G1 inizia a servire
    game_speed_ms = INITIAL_SPEED_MS
    p1_paddle['x'] = p2_paddle['x'] = (MATRIX_WIDTH - PADDLE_WIDTH) // 2
    game_state = "PRE_SERVE"

# --- Funzioni di Disegno ---
def draw_number(number_str, start_x, start_y, color):
    #... (identica alla versione precedente)
    offset_x = 0
    for char in number_str:
        if char in FONT:
            for (px, py) in FONT[char]: draw_pixel(start_x + offset_x + px, start_y + py, color)
            offset_x += 4
            
def draw_frame():
    #... (identica alla versione precedente)
    np.fill(BLACK)
    for i in range(PADDLE_WIDTH):
        draw_pixel(p1_paddle['x'] + i, P1_Y, P1_COLOR)
        draw_pixel(p2_paddle['x'] + i, P2_Y, P2_COLOR)
    draw_pixel(ball['x'], ball['y'], BALL_COLOR)
    for i in range(p1_score): draw_pixel(i, MATRIX_HEIGHT - 1, P1_COLOR)
    for i in range(p2_score): draw_pixel(MATRIX_WIDTH - 1 - i, MATRIX_HEIGHT - 1, P2_COLOR)
    np.write()
    
def show_winner_screen():
    #... (identica alla versione precedente)
    np.fill(BLACK)
    winner = "1" if p1_score > p2_score else "2"
    draw_number(winner, 6, 6, WINNER_COLOR)
    np.write()
    play_tone(1046, 150); time.sleep_ms(150); play_tone(1318, 150); time.sleep_ms(150); play_tone(1568, 300)
    time.sleep(4)

# --- Funzioni Logica di Gioco ---
def handle_input():
    #... (identica alla versione precedente)
    if p1_left.value() == 0 and p1_paddle['x'] > 0: p1_paddle['x'] -= 1
    if p1_right.value() == 0 and p1_paddle['x'] < (MATRIX_WIDTH - PADDLE_WIDTH): p1_paddle['x'] += 1
    if p2_left.value() == 0 and p2_paddle['x'] > 0: p2_paddle['x'] -= 1
    if p2_right.value() == 0 and p2_paddle['x'] < (MATRIX_WIDTH - PADDLE_WIDTH): p2_paddle['x'] += 1

# MODIFICA: Corretta la logica di collisione per entrambe le pale
def update_game():
    global game_state, game_speed_ms, p1_score, p2_score, serving_player
    
    ball['x'] += ball['vx']; ball['y'] += ball['vy']
    ball_ix, ball_iy = int(ball['x']), int(ball['y'])
    
    if game_speed_ms > MIN_SPEED_MS: game_speed_ms -= 0.04
    
    if ball['x'] <= 0 or ball['x'] >= MATRIX_WIDTH - 1:
        ball['vx'] *= -1; ball['x'] = max(0.1, min(MATRIX_WIDTH - 1.1, ball['x'])); play_tone(600, 15)
        
    # Pala G2 (in alto)
    if ball['vy'] < 0 and ball_iy == P2_Y and p2_paddle['x'] -1 <= ball_ix < p2_paddle['x'] + PADDLE_WIDTH + 1:
        ball['vy'] *= -1
        ball['y'] = P2_Y + 1 # Spinge la palla appena sotto la pala
        play_tone(987, 20)
        if ball_ix < p2_paddle['x'] + 1: ball['vx'] = -0.6
        elif ball_ix > p2_paddle['x'] + 1: ball['vx'] = 0.6
        else: ball['vx'] *= 0.8
            
    # Pala G1 (in basso)
    if ball['vy'] > 0 and ball_iy == P1_Y and p1_paddle['x'] -1 <= ball_ix < p1_paddle['x'] + PADDLE_WIDTH + 1:
        ball['vy'] *= -1
        ball['y'] = P1_Y - 0.1 # Spinge la palla appena sopra la pala
        play_tone(880, 20)
        if ball_ix < p1_paddle['x'] + 1: ball['vx'] = -0.6
        elif ball_ix > p1_paddle['x'] + 1: ball['vx'] = 0.6
        else: ball['vx'] *= 0.8

    # Palla persa / Punto
    point_scored = False
    if ball['y'] < 0: # G1 segna
        p1_score += 1; serving_player = 2; point_scored = True; play_tone(1318, 150)
    elif ball['y'] >= MATRIX_HEIGHT: # G2 segna
        p2_score += 1; serving_player = 1; point_scored = True; play_tone(523, 150)
        
    if point_scored:
        if p1_score >= WINNING_SCORE or p2_score >= WINNING_SCORE:
            game_state = "GAME_OVER"
        else:
            game_state = "PRE_SERVE"
            p1_paddle['x'] = p2_paddle['x'] = (MATRIX_WIDTH - PADDLE_WIDTH) // 2

def show_image(image):
    for i in range(256):
        np[i] = image[i]
    np.write()
    return False

# --- Ciclo Principale (invariato)---
while True:
    if game_state == "START_SCREEN":
        show_image(image_data)
        #np.fill(BLACK); np.write()
        if not btn_start.value() and not p2_left.value() and not p2_right.value():
            machine.reset() #torno al menù
            
        if btn_start.value() == 0:
            start_new_game()

    elif game_state == "PRE_SERVE":
        handle_input()
        if serving_player == 1:
            ball['x'] = p1_paddle['x'] + (PADDLE_WIDTH // 2); ball['y'] = P1_Y - 1
        else:
            ball['x'] = p2_paddle['x'] + (PADDLE_WIDTH // 2); ball['y'] = P2_Y + 1
        ball['vx'], ball['vy'] = 0, 0
        
        if btn_start.value() == 0:
            if serving_player == 1: ball['vy'] = -0.6
            else: ball['vy'] = 0.6
            ball['vx'] = random.choice([-0.3, 0.3])
            game_state = "PLAYING"
            play_tone(1000, 50); time.sleep_ms(200)
            
        draw_frame()

    elif game_state == "PLAYING":
        handle_input()
        update_game()
        draw_frame()
        time.sleep_ms(int(game_speed_ms))

    elif game_state == "GAME_OVER":
        show_winner_screen()
        game_state = "START_SCREEN"
        
    time.sleep_ms(10)
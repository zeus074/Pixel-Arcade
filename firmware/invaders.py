# SPDX-FileCopyrightText: 2024 Francesco Vannini
#
# SPDX-License-Identifier: MIT

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

# --- Configurazione Display e Gioco ---
MATRIX_WIDTH = 16
MATRIX_HEIGHT = 16
NUM_PIXELS = MATRIX_WIDTH * MATRIX_HEIGHT
PLAYER_TURRET_Y_POS = 14
SHIELD_Y_POS = 12

# --- Colori (R, G, B) ---
BLACK = (0, 0, 0)
WHITE = (50, 50, 50)
PLAYER_COLOR = (0, 100, 255)
PLAYER_PROJECTILE_COLOR = (0, 255, 0)
ALIEN_PROJECTILE_COLOR = (255, 0, 100)
SHIELD_COLOR = (40, 100, 0)
LIFE_COLOR = (200, 0, 0)
TEXT_COLOR = (200, 100, 0)

# --- Stati del gioco ---
STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_PLAYER_HIT = 3
STATE_NEXT_LEVEL = 4
np = neopixel.NeoPixel(machine.Pin(NEOPIXEL_PIN), NUM_PIXELS)
# --- FONT 3x5 per i numeri ---
FONT = {
    '0': [(0,0),(1,0),(2,0),(0,1),(2,1),(0,2),(2,2),(0,3),(2,3),(0,4),(1,4),(2,4)],
    '1': [(1,0),(1,1),(1,2),(1,3),(1,4)],
    '2': [(0,0),(1,0),(2,0),(2,1),(0,2),(1,2),(2,2),(0,3),(0,4),(1,4),(2,4)],
    '3': [(0,0),(1,0),(2,0),(2,1),(1,2),(2,3),(0,4),(1,4),(2,4)],
    '4': [(0,0),(2,0),(0,1),(2,1),(0,2),(1,2),(2,2),(2,3),(2,4)],
    '5': [(0,0),(1,0),(2,0),(0,1),(0,2),(1,2),(2,2),(2,3),(0,4),(1,4),(2,4)],
    '6': [(0,0),(1,0),(2,0),(0,1),(0,2),(1,2),(2,2),(0,3),(2,3),(0,4),(1,4),(2,4)],
    '7': [(0,0),(1,0),(2,0),(2,1),(2,2),(2,3),(2,4)],
    '8': [(0,0),(1,0),(2,0),(0,1),(2,1),(1,2),(0,3),(2,3),(0,4),(1,4),(2,4)],
    '9': [(0,0),(1,0),(2,0),(0,1),(2,1),(0,2),(1,2),(2,2),(2,3),(0,4),(1,4),(2,4)],
}
image_data = [
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (100, 100, 100),     (100, 100, 100),     (0, 0, 0),     (100, 100, 100),     (100, 100, 100),     (0, 0, 0),     (100, 100, 100),     (100, 100, 100),     (0, 0, 0),     (100, 100, 100),     (100, 100, 100),     (0, 0, 0),     (100, 100, 100),     (100, 100, 100),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (100, 100, 100),     (100, 100, 100),     (0, 0, 0),     (100, 100, 100),     (100, 100, 100),     (0, 0, 0),     (100, 100, 100),     (100, 100, 100),     (0, 0, 0),     (100, 100, 100),     (100, 100, 100),     (0, 0, 0),     (100, 100, 100),     (100, 100, 100),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (100, 100, 100),     (100, 100, 100),     (0, 0, 0),     (100, 100, 100),     (100, 100, 100),     (0, 0, 0),     (100, 100, 100),     (100, 100, 100),     (0, 0, 0),     (100, 100, 100),     (100, 100, 100),     (0, 0, 0),     (100, 100, 100),     (100, 100, 100),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (151, 142, 0),     (151, 142, 0),     (0, 0, 0),     (151, 142, 0),     (151, 142, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (151, 142, 0),     (0, 0, 0),     (0, 0, 0),     (151, 142, 0),     (151, 142, 0),     (0, 0, 0),     (151, 142, 0),     (151, 142, 0),
    (0, 0, 0),     (151, 142, 0),     (0, 0, 0),     (0, 0, 0),     (151, 142, 0),     (0, 0, 0),     (151, 142, 0),     (0, 0, 0),     (151, 142, 0),     (0, 0, 0),     (151, 142, 0),     (0, 0, 0),     (151, 142, 0),     (0, 0, 0),     (0, 0, 0),     (151, 142, 0),
    (151, 142, 0),     (151, 142, 0),     (0, 0, 0),     (151, 142, 0),     (151, 142, 0),     (0, 0, 0),     (0, 0, 0),     (151, 142, 0),     (0, 0, 0),     (151, 142, 0),     (0, 0, 0),     (151, 142, 0),     (0, 0, 0),     (0, 0, 0),     (151, 142, 0),     (151, 142, 0),
    (0, 0, 0),     (151, 142, 0),     (0, 0, 0),     (0, 0, 0),     (151, 142, 0),     (0, 0, 0),     (151, 142, 0),     (151, 142, 0),     (151, 142, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (151, 142, 0),     (0, 0, 0),     (151, 142, 0),     (0, 0, 0),
    (151, 142, 0),     (151, 142, 0),     (0, 0, 0),     (151, 142, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (151, 142, 0),     (0, 0, 0),     (151, 142, 0),     (0, 0, 0),     (151, 142, 0),     (151, 142, 0),     (0, 0, 0),     (151, 142, 0),     (151, 142, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 55, 155),     (0, 55, 155),     (0, 0, 0),     (0, 0, 0),     (0, 55, 155),     (0, 55, 155),     (0, 0, 0),     (0, 0, 0),     (0, 55, 155),     (0, 55, 155),     (0, 0, 0),     (0, 0, 0),     (0, 55, 155),     (0, 55, 155),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (6, 90, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (6, 90, 0),     (6, 90, 0),     (6, 90, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
]
# --- Inizializzazione Hardware ---
pixels = neopixel.NeoPixel(machine.Pin(NEOPIXEL_PIN), NUM_PIXELS)
button_left = machine.Pin(BUTTON_LEFT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
button_right = machine.Pin(BUTTON_RIGHT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
button_fire = machine.Pin(BUTTON_FIRE_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
button_fire2 = machine.Pin(BUTTON_FIRE2_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
button_start = machine.Pin(BUTTON_START_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
try:
    buzzer = machine.PWM(machine.Pin(BUZZER_PIN))
    buzzer.duty_u16(0)
except:
    print("Buzzer non trovato.")
    buzzer = None

# --- Variabili Globali del Gioco ---
game_state = STATE_MENU
player_pos = 0
player_lives = 0
score = 0
level = 0
player_projectile = {'x': 0, 'y': 0, 'active': False}
aliens = []
alien_projectiles = []
shields = []
alien_direction = 0
alien_move_timer = 0
alien_move_speed = 0
alien_fire_threshold = 97
initial_alien_speed = 600
num_aliens_start = 0
hit_animation_timer = 0

# --- Funzioni di Utilità ---
def map_pixel(x, y):
    if x < 0 or x >= MATRIX_WIDTH or y < 0 or y >= MATRIX_HEIGHT: return -1
    if y % 2 == 0: return y * MATRIX_WIDTH + (MATRIX_WIDTH - 1 - x)
    else: return y * MATRIX_WIDTH + x

def set_pixel(x, y, color):
    idx = map_pixel(x, y)
    if idx != -1: pixels[idx] = color

def clear_display():
    pixels.fill(BLACK)

def play_tone(frequency, duration):
    if not buzzer: return
    buzzer.freq(frequency)
    buzzer.duty_u16(1000)
    time.sleep_ms(duration)
    buzzer.duty_u16(0)

def draw_text(text, start_x, start_y, color):
    char_spacing = 4
    for char in text:
        if char in FONT:
            for p in FONT[char]:
                set_pixel(start_x + p[0], start_y + p[1], color)
        start_x += char_spacing

# --- Funzioni di Gioco ---
def create_aliens():
    global num_aliens_start
    aliens.clear()
    for row in range(3):
        for i in range(5):
            x_pos = i * 3 + 1
            y_pos = row * 2 + 2
            aliens.append({'x': x_pos, 'y': y_pos, 'width': 2, 'active': True})
    num_aliens_start = len(aliens)

def create_shields():
    """ MODIFICA v1.3: Nuovo layout degli scudi come da richiesta.
        4 blocchi da 2 pixel, con 2 pixel di spazio tra loro. """
    shields.clear()
    # Scudo (2px) + Spazio (2px) = Blocco da 4 pixel.
    for i in range(4): # Per i 4 scudi
        # Calcola la x di base per il blocco (0, 4, 8, 12)
        block_start_x = i * 4
        # Lo scudo vero e proprio parte dal secondo pixel del suo blocco (offset +1)
        shield_pixel_1_x = block_start_x + 1
        shield_pixel_2_x = block_start_x + 2
        
        shields.append({'x': shield_pixel_1_x, 'y': SHIELD_Y_POS, 'active': True})
        shields.append({'x': shield_pixel_2_x, 'y': SHIELD_Y_POS, 'active': True})

def start_new_level():
    global level, alien_move_speed, alien_move_timer, alien_direction, alien_fire_threshold, player_pos, game_state
    level += 1
    create_aliens()
    create_shields()
    player_projectile['active'] = False
    alien_projectiles.clear()
    player_pos = MATRIX_WIDTH // 2
    base_speed = initial_alien_speed - (level * 50)
    alien_move_speed = max(150, base_speed)
    alien_fire_threshold = max(92, 98 - level)
    alien_direction = -1
    alien_move_timer = time.ticks_add(time.ticks_ms(), alien_move_speed)
    game_state = STATE_PLAYING

def setup_new_game():
    global player_lives, score, level
    player_lives = 3
    score = 0
    level = 0
    start_new_level()

def draw_elements(draw_player=True):
    clear_display()
    for i in range(player_lives): set_pixel(i, 0, LIFE_COLOR)
    if draw_player:
        set_pixel(player_pos - 1, PLAYER_TURRET_Y_POS + 1, PLAYER_COLOR)
        set_pixel(player_pos,     PLAYER_TURRET_Y_POS + 1, PLAYER_COLOR)
        set_pixel(player_pos + 1, PLAYER_TURRET_Y_POS + 1, PLAYER_COLOR)
        set_pixel(player_pos, PLAYER_TURRET_Y_POS, PLAYER_COLOR)
    if player_projectile['active']: set_pixel(player_projectile['x'], player_projectile['y'], PLAYER_PROJECTILE_COLOR)
    for alien in aliens:
        if alien['active']:
            for i in range(alien['width']): set_pixel(alien['x'] + i, alien['y'], WHITE)
    for proj in alien_projectiles:
        if proj['active']: set_pixel(proj['x'], proj['y'], ALIEN_PROJECTILE_COLOR)
    for shield_part in shields:
        if shield_part['active']: set_pixel(shield_part['x'], shield_part['y'], SHIELD_COLOR)
    pixels.write()

def handle_input():
    global player_pos
    if button_left.value() == 0: player_pos = max(1, player_pos - 1)
    if button_right.value() == 0: player_pos = min(MATRIX_WIDTH - 2, player_pos + 1)
    if button_fire.value() == 0 and not player_projectile['active']:
        player_projectile['x'] = player_pos
        player_projectile['y'] = PLAYER_TURRET_Y_POS - 1
        player_projectile['active'] = True
        play_tone(880, 50)

def update_game_state():
    global game_state, score, alien_direction, alien_move_timer, alien_move_speed
    
    # Aggiorna proiettile giocatore
    if player_projectile['active']:
        player_projectile['y'] -= 1
        if player_projectile['y'] < 1: player_projectile['active'] = False
        else:
            for alien in aliens:
                if alien['active'] and player_projectile['y'] == alien['y'] and \
                   alien['x'] <= player_projectile['x'] < alien['x'] + alien['width']:
                    alien['active'] = False
                    player_projectile['active'] = False
                    score += 10 * level
                    play_tone(220, 100)
                    break
            if player_projectile['active']:
                for shield in shields:
                    if shield['active'] and shield['x'] == player_projectile['x'] and shield['y'] == player_projectile['y']:
                        shield['active'] = False
                        player_projectile['active'] = False
                        break
    
    # Aggiorna movimento alieni
    if time.ticks_diff(alien_move_timer, time.ticks_ms()) < 0:
        active_aliens_count = sum(1 for a in aliens if a['active'])
        current_speed = alien_move_speed
        if active_aliens_count == 1: current_speed = 75
        alien_move_timer = time.ticks_add(time.ticks_ms(), current_speed)
        play_tone(50, 20)
        
        move_down = False
        for alien in aliens:
            if alien['active']:
                if (alien['x'] <= 0 and alien_direction == -1) or \
                   (alien['x'] + alien['width'] - 1 >= MATRIX_WIDTH - 1 and alien_direction == 1):
                    move_down = True
                    alien_direction *= -1
                    break
        
        for alien in aliens:
            if alien['active']:
                if move_down: alien['y'] += 1
                else: alien['x'] += alien_direction
                if alien['y'] >= PLAYER_TURRET_Y_POS:
                    game_state = STATE_GAME_OVER
                    play_tone(110, 500)
                    return

        # --- CORREZIONE v1.3: Logica di distruzione scudi spostata e corretta ---
        # Controlla la posizione DEGLI ALIENI DOPO che si sono mossi.
        max_alien_y = 0
        for alien in aliens:
            if alien['active']:
                max_alien_y = max(max_alien_y, alien['y'])
        
        # Se la Y più bassa degli alieni tocca gli scudi e gli scudi sono ancora attivi...
        if max_alien_y >= SHIELD_Y_POS and any(s['active'] for s in shields):
            play_tone(100, 150) # Suono "crunch"
            for shield in shields: 
                shield['active'] = False # ...distruggili tutti.
    
    # Aggiorna proiettili alieni
    if random.randint(0, 100) > alien_fire_threshold and any(a['active'] for a in aliens):
        bottom_aliens = {}
        for alien in aliens:
            if alien['active']:
                for i in range(alien['width']):
                    col = alien['x'] + i
                    if col not in bottom_aliens or alien['y'] > bottom_aliens[col]['y']:
                        bottom_aliens[col] = alien
        if bottom_aliens:
            shooter_alien = random.choice(list(bottom_aliens.values()))
            shooter_x = shooter_alien['x'] + random.randint(0, shooter_alien['width']-1)
            alien_projectiles.append({'x': shooter_x, 'y': shooter_alien['y'] + 1, 'active': True})

    for proj in list(alien_projectiles):
        if proj['active']:
            proj['y'] += 1
            if proj['y'] >= MATRIX_HEIGHT: proj['active'] = False
            for shield in shields:
                if shield['active'] and shield['x'] == proj['x'] and shield['y'] == proj['y']:
                    shield['active'] = False
                    proj['active'] = False
                    break
            if proj['active']:
                is_hit = (proj['y'] == PLAYER_TURRET_Y_POS + 1 and player_pos - 1 <= proj['x'] <= player_pos + 1) or \
                         (proj['y'] == PLAYER_TURRET_Y_POS and proj['x'] == player_pos)
                if is_hit:
                    proj['active'] = False
                    game_state = STATE_PLAYER_HIT
                    global hit_animation_timer
                    hit_animation_timer = time.ticks_add(time.ticks_ms(), 1500)
                    play_tone(150, 400)
                    return

    alien_projectiles[:] = [p for p in alien_projectiles if p['active']]

    if not any(a['active'] for a in aliens):
        game_state = STATE_NEXT_LEVEL
        play_tone(440, 100); time.sleep_ms(50); play_tone(550, 100); time.sleep_ms(50); play_tone(660, 200)

def show_image(image):
    for i in range(256):
        np[i] = image[i]
    np.write()
    return False


# --- Ciclo Principale del Gioco ---
while True:
    if game_state == STATE_MENU:
        #clear_display()
        #pixels.write()
        show_image(image_data)
        if not button_start.value() and not button_fire.value() and not button_fire2.value():
            machine.reset() #torno al menù
            
        if button_start.value() == 0:
            setup_new_game()
            time.sleep_ms(300)

    elif game_state == STATE_PLAYING:
        handle_input()
        update_game_state()
        draw_elements()

    elif game_state == STATE_PLAYER_HIT:
        is_visible = (time.ticks_diff(hit_animation_timer, time.ticks_ms()) // 150) % 2 == 0
        draw_elements(draw_player=is_visible)
        if time.ticks_diff(hit_animation_timer, time.ticks_ms()) < 0:
            player_lives -= 1
            if player_lives <= 0:
                game_state = STATE_GAME_OVER
            else:
                player_pos = MATRIX_WIDTH // 2
                alien_projectiles.clear()
                game_state = STATE_PLAYING

    elif game_state == STATE_NEXT_LEVEL:
        clear_display()
        draw_text(str(level + 1), 6, 5, TEXT_COLOR)
        pixels.write()
        time.sleep(2)
        start_new_level()
        
    elif game_state == STATE_GAME_OVER:
        clear_display()
        draw_text(str(score), 1, 5, TEXT_COLOR)
        pixels.write()
        time.sleep(5)
        game_state = STATE_MENU

    time.sleep_ms(20)
import machine
import neopixel
import time
import random

# --- Configurazione Hardware ---
NEOPIXEL_PIN = 2; BUTTON_LEFT_PIN = 16; BUTTON_RIGHT_PIN = 17
BUTTON_UP_PIN = 18; BUTTON_DOWN_PIN = 19; BUZZER_PIN = 21
BUTTON_START = 20

# --- Configurazione Display e Gioco ---
MATRIX_WIDTH = 16; MATRIX_HEIGHT = 16; NUM_PIXELS = MATRIX_WIDTH * MATRIX_HEIGHT

# Colori (con luminosità rivista)
BLACK = (0, 0, 0); WALL_COLOR = (0, 0, 30); PLAYER_COLOR = (40, 40, 0)
DOT_COLOR = (2, 2, 2); ORANGE = (40, 15, 0); SCORE_COLOR = (40, 40, 40)
POWER_PILL_COLOR = ORANGE; GHOST_COLORS = [(25,0,0), (0,25,25)]
FRIGHTENED_COLOR = (10, 0, 80) # MODIFICA: Blu più scuro e distinguibile
FRIGHTENED_FLASH_COLOR = (30, 30, 30) # Colore del lampeggio finale
EATEN_COLOR = (20, 20, 20)

# Parametri di Gioco
PLAYER_SPEED_MS = 180; GHOST_SPEED_MS = 240
FRIGHTENED_DURATION_S = 7; FRIGHTENED_WARNING_S = 2 # Lampeggia negli ultimi 2 secondi

# --- Inizializzazione Hardware ---
np = neopixel.NeoPixel(machine.Pin(NEOPIXEL_PIN), NUM_PIXELS)
btn_left = machine.Pin(BUTTON_LEFT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
btn_right = machine.Pin(BUTTON_RIGHT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
btn_up = machine.Pin(BUTTON_UP_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
btn_down = machine.Pin(BUTTON_DOWN_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
buzzer = machine.PWM(machine.Pin(BUZZER_PIN)); buzzer.duty_u16(0)
btn_start = machine.Pin(BUTTON_START, machine.Pin.IN, machine.Pin.PULL_UP)

# --- Labirinto ---
LEVEL_1 = [
    "################",
    "#O............O#",
    "#.##.####.#.##.#",
    "#..#......#.#..#",
    "##.#.####.#.##.#",
    "#....# GG #....#",
    "####.# ## #.####",
    "     #  # #     ",
    "####.# ## #.####",
    "#....#....#....#",
    "##.#.####.#.##.#",
    "#..#....P...#..#",
    "#.##.####.####.#",
    "#O............O#",
    "################",
]
LEVEL_2 = [ "################",
            "#O.........#..O#",
            "#.##.#.##.####.#",
            "#....# G.G #...#",
            "#.##.#####.##.##",
            "...#....P.......",
            "##.###.##.###.##",
            "#...#..##..#...#",
            "##.###.##.###.##",
            "#..#...##...#..#",
            "#.##.#.##.#.##.#",
            "#....#....#....#",
            "#.##.#.##.##.#.#",
            "#O............O#",
            "################" ]

LEVEL_3 = [ "################",
            "#O...........#O#",
            "#.###.#.##.#.#.#",
            "#...#.#.GG.#.#.#",
            "#.#.#.#.##.#.#.#",
            "#...#.#....#.#.#",
            "###.#.##.###.#.#",
            "    .P....G.    ",
            "###.#.######.#.#",
            "#...#........#.#",
            "###.#.######.#.#",
            "#...#...##.....#",
            "#.###.######.###",
            "#O............O#",
            "################" ]

ALL_LEVELS = [LEVEL_1, LEVEL_2, LEVEL_3]

# --- FONT per il punteggio ---
FONT = { '0':[(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(1,4),(2,0),(2,1),(2,2),(2,3),(2,4)],'1':[(1,0),(1,1),(1,2),(1,3),(1,4),(0,1)],'2':[(0,0),(1,0),(2,0),(2,1),(2,2),(0,2),(1,2),(0,3),(0,4),(1,4),(2,4)],'3':[(0,0),(1,0),(2,0),(2,1),(2,2),(1,2),(2,3),(0,4),(1,4),(2,4)],'4':[(0,0),(0,1),(0,2),(1,2),(2,0),(2,1),(2,2),(2,3),(2,4)],'5':[(0,0),(1,0),(2,0),(0,1),(0,2),(1,2),(2,2),(2,3),(0,4),(1,4),(2,4)],'6':[(0,0),(1,0),(2,0),(0,1),(0,2),(1,2),(2,2),(0,3),(0,4),(2,3),(2,4),(1,4)],'7':[(0,0),(1,0),(2,0),(2,1),(2,2),(2,3),(2,4)],'8':[(0,0),(1,0),(2,0),(0,1),(2,1),(1,2),(0,3),(2,3),(0,4),(1,4),(2,4)],'9':[(0,0),(1,0),(2,0),(0,1),(2,1),(0,2),(1,2),(2,2),(2,3),(2,4)] }

# --- Variabili Globali di Gioco ---
game_state = "START_SCREEN"; player = {}; ghosts = []; walls = set(); dots = set(); power_pills = set()
score = 0; lives = 3; frightened_end_tick = 0; last_player_move = 0; last_ghost_move = 0; level_start_tick = 0
current_level_index = 2

image_data = [
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (80, 0, 0),     (80, 0, 0),     (80, 0, 0),
    (80, 0, 0),     (0, 0, 0),     (80, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (3, 3, 16),     (0, 0, 0),     (3, 3, 16),     (3, 3, 16),     (0, 0, 0),     (0, 0, 0),     (3, 3, 16),     (0, 0, 0),     (0, 0, 0),     (3, 3, 16),
    (3, 3, 16),     (0, 0, 0),     (3, 3, 16),     (3, 3, 16),     (0, 0, 0),     (3, 3, 16),     (0, 0, 0),     (3, 3, 16),     (3, 3, 16),     (3, 3, 16),     (0, 0, 0),     (80, 0, 0),     (0, 0, 0),     (80, 0, 0),     (80, 0, 0),     (80, 0, 0),
    (80, 0, 0),     (0, 0, 0),     (0, 0, 0),     (80, 0, 0),     (0, 0, 0),     (0, 0, 0),     (3, 3, 16),     (0, 0, 0),     (3, 3, 16),     (3, 3, 16),     (3, 3, 16),     (0, 0, 0),     (3, 3, 16),     (0, 0, 0),     (3, 3, 16),     (3, 3, 16),
    (3, 3, 16),     (0, 0, 0),     (0, 0, 0),     (3, 3, 16),     (0, 0, 0),     (3, 3, 16),     (0, 0, 0),     (3, 3, 16),     (0, 0, 0),     (3, 3, 16),     (0, 0, 0),     (80, 0, 0),     (0, 0, 0),     (80, 0, 0),     (0, 0, 0),     (80, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (81, 62, 1),     (81, 62, 1),     (81, 62, 1),     (81, 62, 1),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (81, 62, 1),     (81, 62, 1),     (81, 62, 1),     (81, 62, 1),     (81, 62, 1),     (81, 62, 1),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (81, 62, 1),     (81, 62, 1),     (81, 62, 1),     (81, 62, 1),     (81, 62, 1),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (81, 62, 1),     (0, 0, 0),     (0, 0, 0),     (81, 62, 1),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (81, 62, 1),     (81, 62, 1),     (81, 62, 1),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (81, 62, 1),     (81, 62, 1),     (81, 62, 1),     (81, 62, 1),     (81, 62, 1),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (81, 62, 1),     (81, 62, 1),     (81, 62, 1),     (81, 62, 1),     (81, 62, 1),     (81, 62, 1),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (81, 62, 1),     (81, 62, 1),     (81, 62, 1),     (81, 62, 1),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
]

# --- Funzioni di Utilità e Setup ---
def xy_to_index(x, y):
    x_int, y_int = int(x), int(y)
    if y_int % 2 == 0: return y_int * MATRIX_WIDTH + (MATRIX_WIDTH - 1 - x_int)
    else: return y_int * MATRIX_WIDTH + x_int
def draw_pixel(x, y, color): np[xy_to_index(x, y)] = color
def play_tone(freq, dur): buzzer.freq(freq); buzzer.duty_u16(1024); time.sleep_ms(dur); buzzer.duty_u16(0)

def setup_level(is_new_life):
    #... (Questa funzione è identica alla versione precedente)
    global player, ghosts, walls, dots, power_pills, level_start_tick
    level_start_tick = time.ticks_ms()
    
    layout = ALL_LEVELS[current_level_index]
    
    if not is_new_life:
        walls.clear(); dots.clear(); power_pills.clear(); ghosts.clear()
        player_start_pos = (0, 0); ghost_starts = []
        for y, row in enumerate(layout):
            for x, char in enumerate(row):
                if char == '#': walls.add((x, y))
                elif char == '.': dots.add((x, y)) #and (x + y) % 2 == 0: dots.add((x, y))
                elif char == 'O': power_pills.add((x, y))
                elif char == 'P': player_start_pos = (x, y)
                elif char == 'G': ghost_starts.append((x, y))
        player = {'x': player_start_pos[0], 'y': player_start_pos[1], 'dx': 0, 'dy': 0, 'next_dx': -1, 'next_dy': 0, 'start': player_start_pos}
        personalities = ['AGGRESSIVE', 'RANDOM']; release_times = [1000, 5000]
        for i in range(len(ghost_starts)):
            if i >= 2: break
            ghosts.append({'x': ghost_starts[i][0], 'y': ghost_starts[i][1], 'dx': 0, 'dy': 0, 
                           'color': GHOST_COLORS[i], 'state': 'IN_HOUSE', 'home': ghost_starts[i],
                           'personality': personalities[i], 'release_time': release_times[i]})
    else:
        player['x'], player['y'] = player['start']; player['dx'], player['dy'] = 0,0; player['next_dx'], player['next_dy'] = -1,0
        for ghost in ghosts:
            ghost['x'], ghost['y'] = ghost['home']; ghost['state'] = 'IN_HOUSE'

def start_new_game():
    global score, lives, game_state, last_player_move, last_ghost_move
    score = 0; lives = 3; current_level_index = 0
    setup_level(is_new_life=False)
    game_state = "PLAYING"
    last_player_move = last_ghost_move = time.ticks_ms()

# --- Funzioni Logica di Gioco ---
# (handle_input, move_player, move_ghosts sono identiche alla versione precedente)
def handle_input():
    if btn_up.value() == 0: player['next_dx'], player['next_dy'] = 0, -1
    elif btn_down.value() == 0: player['next_dx'], player['next_dy'] = 0, 1
    elif btn_left.value() == 0: player['next_dx'], player['next_dy'] = -1, 0
    elif btn_right.value() == 0: player['next_dx'], player['next_dy'] = 1, 0
def move_player():
    px, py=player['x'], player['y']; pdx, pdy=player['dx'], player['dy']; pndx,pndy=player['next_dx'],player['next_dy']
    if (pndx, pndy) != (pdx, pdy) and (px + pndx, py + pndy) not in walls: player['dx'], player['dy'] = pndx, pndy
    if (px + player['dx'], py + player['dy']) not in walls:
        player['x'] += player['dx']; player['y'] += player['dy']
        if player['x'] < 0: player['x'] = MATRIX_WIDTH - 1
        if player['x'] >= MATRIX_WIDTH: player['x'] = 0
def move_ghosts():
    for ghost in ghosts:
        if ghost['state']=='IN_HOUSE': continue
        gx,gy=ghost['x'],ghost['y']; target_x,target_y=player['x'],player['y']
        if ghost['state']=='FRIGHTENED': target_x,target_y=-1,-1
        elif ghost['state']=='EATEN': target_x,target_y=ghost['home']
        possible_moves=[]
        for dx,dy in [(0,-1),(0,1),(-1,0),(1,0)]:
            if (dx,dy)==(-ghost['dx'],-ghost['dy']): continue
            if (gx+dx,gy+dy) not in walls: possible_moves.append((dx,dy))
        if not possible_moves and (gx-ghost['dx'],gy-ghost['dy']) not in walls: possible_moves.append((-ghost['dx'],-ghost['dy']))
        best_move=(0,0)
        if possible_moves:
            use_random_move=(ghost['personality']=='RANDOM' and random.random()<0.4)
            if ghost['state']=='FRIGHTENED' or use_random_move: best_move=random.choice(possible_moves)
            else:
                min_dist=999
                for dx,dy in possible_moves:
                    dist=abs(gx+dx-target_x)+abs(gy+dy-target_y)
                    if dist<min_dist: min_dist=dist; best_move=(dx,dy)
        ghost['dx'],ghost['dy']=best_move; ghost['x']+=best_move[0]; ghost['y']+=best_move[1]
        if ghost['state']=='EATEN' and (ghost['x'],ghost['y'])==ghost['home']: ghost['state']='CHASING'

def check_game_state():
    #... (Questa funzione è identica alla versione precedente)
    global score, lives, game_state, frightened_end_tick
    px,py=player['x'],player['y']
    if (px,py) in dots: dots.remove((px,py)); score+=10; play_tone(1200,10)
    if (px,py) in power_pills:
        power_pills.remove((px,py)); score+=50; play_tone(1500,150)
        frightened_end_tick=time.ticks_add(time.ticks_ms(),FRIGHTENED_DURATION_S*1000)
        for g in ghosts:
            if g['state']=='CHASING': g['state']='FRIGHTENED'
    if frightened_end_tick!=0 and time.ticks_diff(frightened_end_tick,time.ticks_ms())<=0:
        frightened_end_tick=0
        for g in ghosts:
            if g['state']=='FRIGHTENED': g['state']='CHASING'
    for ghost in ghosts:
        if ghost['state']=='IN_HOUSE' and time.ticks_diff(time.ticks_ms(),level_start_tick)>ghost['release_time']:
            ghost['state']='CHASING'; play_tone(800,50)
    for ghost in ghosts:
        if (px,py)==(ghost['x'],ghost['y']) and ghost['state']!='IN_HOUSE':
            if ghost['state']=='FRIGHTENED': ghost['state']='EATEN'; score+=200; play_tone(2000,100)
            elif ghost['state']=='CHASING':
                lives-=1; play_tone(440,300); time.sleep_ms(50); play_tone(330,500)
                if lives<=0: game_state="GAME_OVER"
                else: setup_level(is_new_life=True)
                return
    if not dots and not power_pills: game_state="LEVEL_CLEAR"; play_tone(2500,500)

# --- Funzioni di Disegno e Schermate ---
def draw_number(number_str, start_x, start_y, color):
    offset_x = 0
    for char in number_str:
        if char in FONT:
            for (px, py) in FONT[char]: draw_pixel(start_x + offset_x + px, start_y + py, color)
            offset_x += 4

def draw_frame():
    np.fill(BLACK)
    for x, y in walls: draw_pixel(x, y, WALL_COLOR)
    for x, y in dots: draw_pixel(x, y, DOT_COLOR)
    if (time.ticks_ms() // 200) % 2 == 0:
        for x, y in power_pills: draw_pixel(x, y, POWER_PILL_COLOR)
    
    for ghost in ghosts:
        color = ghost['color']
        if ghost['state'] == 'FRIGHTENED':
            # MODIFICA: Logica per il lampeggio di avvertimento
            is_ending = time.ticks_diff(frightened_end_tick, time.ticks_ms()) < (FRIGHTENED_WARNING_S * 1000)
            if is_ending and (time.ticks_ms() // 150) % 2 == 0:
                color = FRIGHTENED_FLASH_COLOR
            else:
                color = FRIGHTENED_COLOR
        elif ghost['state'] == 'EATEN': color = EATEN_COLOR
        draw_pixel(ghost['x'], ghost['y'], color)
        
    draw_pixel(player['x'], player['y'], PLAYER_COLOR)
    for i in range(lives): draw_pixel(MATRIX_WIDTH - 2 - i, MATRIX_HEIGHT - 1, PLAYER_COLOR)
    np.write()
    
def show_image(image, wait_for_press=False):
    for i in range(256):
        np[i] = image[i]
    np.write()
    
    if not wait_for_press:
        return False
        
    while btn_start.value():
        time.sleep(0.05)
    return True

def draw_start_screen():
    show_image(image_data, wait_for_press=False)
    
def show_final_score():
    np.fill(BLACK)
    score_str = str(score)
    text_width = len(score_str) * 4 - 1
    start_x = (MATRIX_WIDTH - text_width) // 2
    if start_x < 0: start_x = 0
    draw_number(score_str, start_x, 6, SCORE_COLOR)
    np.write()
    play_tone(523,100); time.sleep_ms(120); play_tone(440,100); time.sleep_ms(120); play_tone(392,200)
    time.sleep(4) # Mostra il punteggio per 4 secondi

# --- Ciclo Principale (MODIFICATO) ---
game_state = "START_SCREEN"
while True:
    current_tick = time.ticks_ms()

    if game_state == "START_SCREEN":
        draw_start_screen()

        if not btn_start.value() and not btn_up.value() and not btn_down.value():
            machine.reset() #torno al menù
            
        if not btn_start.value():
            start_new_game()
        #if not all(btn.value() == 1 for btn in [btn_up, btn_down, btn_left, btn_right]):
            #start_new_game()

    elif game_state == "PLAYING":
        handle_input()
        if time.ticks_diff(current_tick, last_player_move) > PLAYER_SPEED_MS:
            move_player(); last_player_move = current_tick
        if time.ticks_diff(current_tick, last_ghost_move) > GHOST_SPEED_MS:
            move_ghosts(); last_ghost_move = current_tick
        check_game_state()
        draw_frame()

    elif game_state == "LEVEL_CLEAR":
        for i in range(4): np.fill(BLACK); np.write(); time.sleep_ms(150); draw_frame(); time.sleep_ms(150)
        
        # MODIFICA: Logica di progressione livello
        current_level_index += 1
        if current_level_index >= len(ALL_LEVELS):
            current_level_index = 0 # Torna al primo livello
            
        setup_level(is_new_life=False)
        game_state = "PLAYING"
    
    elif game_state == "GAME_OVER":
        show_final_score()
        game_state = "START_SCREEN"
        
    time.sleep_ms(10)
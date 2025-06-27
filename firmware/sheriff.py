import machine
import utime
import urandom
import neopixel

# --- Hardware Configuration ---
NEOPIXEL_PIN = 2
MATRIX_WIDTH = 16
MATRIX_HEIGHT = 16
NUM_PIXELS = MATRIX_WIDTH * MATRIX_HEIGHT

RUN_BUTTON_PIN = 16
APPROACH_BUTTON_PIN = 17  # NUOVO: Approccio/Interagisci
SHOOT_BUTTON_PIN = 18
SHOOT_BUTTON2_PIN = 19
START_BUTTON_PIN = 20
BUZZER_PIN = 21

# --- Game Configuration ---
REACTION_TIME_MS = 500
INITIAL_DIFFICULTY_DELAY = 2000 # Time before a character acts

# --- Pin Initialization ---
run_button = machine.Pin(RUN_BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
approach_button = machine.Pin(APPROACH_BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
shoot_button = machine.Pin(SHOOT_BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
shoot_button2 = machine.Pin(SHOOT_BUTTON2_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
start_button = machine.Pin(START_BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
buzzer = machine.PWM(machine.Pin(BUZZER_PIN))

# --- NeoPixel Matrix Setup ---
pixels = neopixel.NeoPixel(machine.Pin(NEOPIXEL_PIN), NUM_PIXELS)

def map_pixel(x, y):
    if y % 2 == 0:
        return y * MATRIX_WIDTH + (MATRIX_WIDTH - 1 - x)
    else:
        return y * MATRIX_WIDTH + x

def set_pixel(x, y, color):
    if 0 <= x < MATRIX_WIDTH and 0 <= y < MATRIX_HEIGHT:
        pixels[map_pixel(x, y)] = color

def clear_matrix():
    pixels.fill(O)
    # Non è necessario pixels.write() qui, verrà chiamato dalle funzioni di disegno

# --- Sound Effects ---
def play_tone(frequency, duration):
    buzzer.freq(frequency)
    buzzer.duty_u16(1000)
    utime.sleep_ms(duration)
    buzzer.duty_u16(0)

def sound_shoot(): play_tone(1500, 50); play_tone(1000, 100)
def sound_game_over(): play_tone(500, 500); utime.sleep_ms(50); play_tone(400, 500)
def sound_explosion(): play_tone(2000, 100); play_tone(100, 500)
def sound_success(): play_tone(2000, 100)
def sound_run_success(): play_tone(2200, 150)

# --- Graphics & Colors ---
BLACK = (0, 0, 0)
WHITE = (20, 20, 20)
RED = (200, 0, 0)
SKIN = (180, 130, 90)
BROWN = (100, 50, 20)
BLUE = (0, 0, 150)
YELLOW = (200, 200, 0)
GREY = (50, 50, 50)
PINK = (255, 105, 180)
SCORE_COLOR = (0, 100, 255) # Blu per il punteggio

# --- NUOVA SEZIONE: FONT PER I NUMERI (3x5 pixel) ---
FONT = {
    '0': [1,1,1, 1,0,1, 1,0,1, 1,0,1, 1,1,1],
    '1': [0,1,0, 1,1,0, 0,1,0, 0,1,0, 1,1,1],
    '2': [1,1,1, 0,0,1, 1,1,1, 1,0,0, 1,1,1],
    '3': [1,1,1, 0,0,1, 0,1,1, 0,0,1, 1,1,1],
    '4': [1,0,1, 1,0,1, 1,1,1, 0,0,1, 0,0,1],
    '5': [1,1,1, 1,0,0, 1,1,1, 0,0,1, 1,1,1],
    '6': [1,1,1, 1,0,0, 1,1,1, 1,0,1, 1,1,1],
    '7': [1,1,1, 0,0,1, 0,1,0, 0,1,0, 0,1,0],
    '8': [1,1,1, 1,0,1, 1,1,1, 1,0,1, 1,1,1],
    '9': [1,1,1, 1,0,1, 1,1,1, 0,0,1, 1,1,1],
}
FONT_WIDTH = 3
FONT_HEIGHT = 5
M = (32, 7, 1)		#MARRONE
O = (0, 0, 0)		#NERO
P = (138, 95, 54)	#PELLE
W = (100, 100, 100)	#BIANCO
G = (0, 48, 10)		#VERDE
B = (0, 55, 155)	#BLU-CIANO
V = (29, 0, 20)		#VIOLA
R = (72, 0, 0)		#ROSSO
L = (0 , 10, 125) 	#BLU SCURO
H = (32, 26, 35)	#GRIGIO
N = (117, 60, 2)	#MARRONE CHIARO
Y = (151, 142, 0)	#GIALLO
Z = (0, 48, 25)		#VIOLA CHIARO
Q = (15, 5, 0)		#MARRONE SCURO
# --- Grafica Personaggi e Animazioni (DA COMPLETARE CON LA TUA ARTE) ---
sheriff = [
    O, M, M, O,
    M, M, M, M,
    O, P, P, O,
    O, P, P, O,   
    O, W, W, O,
    O, P, G, O, 
    O, P, G, O,
    O, P, G, O,
    O, P, G, O,
    O, P, B, O, 
    O, P, B, O,
    O, B, B, O, 
    O, B, B, O,
    O, B, B, O, 
    O, M, M, O,
    O, M, M, M
]
sheriff_shooting = [
    O, M, M, O,
    M, M, M, M,
    O, P, P, O,
    O, P, P, O,   
    O, W, W, O,
    P, G, G, O, 
    P, G, G, O,
    P, G, G, O,
    P, P, W, W,
    O, B, B, O, 
    O, B, B, O,
    O, B, B, O, 
    O, B, B, O,
    O, B, B, O, 
    O, M, M, O,
    O, M, M, M	]

bandit_idle = [
    O,O,O,O,O,O,O,O,O,M,M,O,
    O,O,O,O,O,O,O,O,M,M,M,M,
    O,O,O,O,O,O,O,O,O,P,P,O,
    O,O,O,O,O,O,O,O,O,V,V,O,
    O,O,O,O,O,O,O,O,O,V,P,O,
    O,O,O,O,O,O,O,O,O,R,P,O,
    O,O,O,O,O,O,O,O,O,R,P,O,
    O,O,O,O,O,O,O,O,O,R,P,O,
    O,O,O,O,O,O,O,O,O,R,P,O,
    O,O,O,O,O,O,O,O,O,R,P,O,
    O,O,O,O,O,O,O,O,O,L,L,O,
    O,O,O,O,O,O,O,O,O,L,L,O,
    O,O,O,O,O,O,O,O,O,L,L,O,
    O,O,O,O,O,O,O,O,O,L,L,O,
    O,O,O,O,O,O,O,O,O,M,M,O,
    O,O,O,O,O,O,O,O,M,M,M,O	]
bandit_shooting = [
    O,O,O,O,O,O,O,O,O,M,M,O,
    O,O,O,O,O,O,O,O,M,M,M,M,
    O,O,O,O,O,O,O,O,O,P,P,O,
    O,O,O,O,O,O,O,O,O,V,V,O,
    O,O,O,O,O,O,O,O,O,V,P,O,
    O,O,O,O,O,W,W,O,O,R,P,O,
    O,O,O,O,O,O,P,P,P,P,P,O,
    O,O,O,O,O,O,O,O,O,R,R,O,
    O,O,O,O,O,O,O,O,O,R,R,O,
    O,O,O,O,O,O,O,O,O,R,R,O,
    O,O,O,O,O,O,O,O,O,L,L,O,
    O,O,O,O,O,O,O,O,O,L,L,O,
    O,O,O,O,O,O,O,O,O,L,L,O,
    O,O,O,O,O,O,O,O,O,L,L,O,
    O,O,O,O,O,O,O,O,O,M,M,O,
    O,O,O,O,O,O,O,O,M,M,M,O	]
bomb = [
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,W,O,O,O,
    O,O,O,O,O,O,O,O,O,O,W,O,
    O,O,O,O,O,O,O,W,O,O,O,O,
    O,O,O,O,O,O,O,O,O,W,O,O,
    O,O,O,O,O,O,O,O,O,O,W,O,
    O,O,O,O,O,O,O,O,O,O,W,O,
    O,O,O,O,O,O,O,O,O,R,V,R,
    O,O,O,O,O,O,O,O,O,R,V,R,
    O,O,O,O,O,O,O,O,O,R,V,R,
    O,O,O,O,O,O,O,O,O,R,V,R,
    O,O,O,O,O,O,O,O,O,R,V,R,
    O,O,O,O,O,O,O,O,O,R,V,R,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
]
woman = [
    O,O,O,O,O,O,O,O,O,W,W,O,
    O,O,O,O,O,O,O,O,W,W,W,W,
    O,O,O,O,O,O,O,O,O,P,P,M,
    O,O,O,O,O,O,O,O,O,P,P,M,
    O,O,O,O,O,O,O,O,O,O,P,M,
    O,O,O,O,O,O,O,O,O,O,W,M,
    O,O,O,O,O,O,O,O,O,W,W,W,
    O,O,O,O,O,O,O,O,O,W,P,W,
    O,O,O,O,O,O,O,O,O,W,P,W,
    O,O,O,O,O,O,O,O,W,W,P,W,
    O,O,O,O,O,O,O,O,W,W,P,W,
    O,O,O,O,O,O,O,O,W,W,P,W,
    O,O,O,O,O,O,O,W,W,W,W,W,
    O,O,O,O,O,O,O,W,W,W,W,W,
    O,O,O,O,O,O,O,W,W,W,W,W,
    O,O,O,O,O,O,O,O,O,M,M,O,
]
native_american_idle = [
    O,O,O,O,O,O,O,O,O,W,O,O,
    O,O,O,O,O,O,O,O,O,W,H,W,
    O,O,O,O,O,O,O,O,O,P,P,H,
    O,O,O,O,O,O,O,O,O,P,P,W,
    O,O,O,O,O,O,O,O,O,O,P,O,
    O,O,O,O,O,O,O,O,O,O,P,O,
    O,O,O,O,O,O,O,O,O,M,M,O,
    O,O,O,O,O,O,O,O,O,M,P,O,
    O,O,O,O,O,O,O,O,O,M,P,O,
    O,O,O,O,O,O,O,O,O,M,P,O,
    O,O,O,O,O,O,O,O,O,M,P,O,
    O,O,O,O,O,O,O,O,O,V,V,O,
    O,O,O,O,O,O,O,O,O,V,V,O,
    O,O,O,O,O,O,O,O,O,V,V,O,
    O,O,O,O,O,O,O,O,O,M,M,O,
    O,O,O,O,O,O,O,O,M,M,M,O,
]
native_american_bow = [
    O,O,O,O,O,O,O,O,O,W,O,O,
    O,O,O,O,O,O,O,O,O,W,H,W,
    O,O,O,O,O,O,O,O,O,P,P,H,
    O,O,O,O,O,O,O,O,O,P,P,W,
    O,O,O,O,O,O,O,O,O,O,P,O,
    O,O,O,O,O,O,O,O,O,O,P,O,
    O,O,O,O,O,O,O,N,N,M,M,O,
    O,O,O,O,O,O,N,O,P,M,P,O,
    O,O,O,O,O,W,W,W,O,M,P,O,
    O,O,O,O,O,O,N,O,P,P,P,O,
    O,O,O,O,O,O,O,N,N,M,O,O,
    O,O,O,O,O,O,O,O,O,V,V,O,
    O,O,O,O,O,O,O,O,O,V,V,O,
    O,O,O,O,O,O,O,O,O,V,V,O,
    O,O,O,O,O,O,O,O,O,M,M,O,
    O,O,O,O,O,O,O,O,M,M,M,O,
]
bandit_dead = [
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,M,O,O,O,O,O,O,R,R,R,
    O,O,M,M,V,V,V,P,P,P,P,P,
]
native_american_dead = [
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,M,O,O,O,O,O,O,M,M,M,
    O,O,M,M,V,V,V,P,P,P,P,P,
]
ghost = [
    O,M,M,O,O,O,O,O,O,O,O,O,O,O,O,O,
    M,M,M,M,O,O,O,O,O,O,W,W,O,O,O,O,
    O,W,W,O,O,O,O,O,O,W,W,W,W,O,O,O,
    O,W,W,O,O,O,O,O,O,W,O,W,W,O,O,O,
    O,W,O,O,O,O,O,O,O,W,W,W,W,O,O,O,
    W,O,O,O,O,O,O,O,O,O,W,W,W,O,O,O,
    O,W,W,O,O,O,O,O,O,W,W,W,W,W,O,O,
    W,O,O,O,O,O,W,W,W,W,W,W,W,W,O,O,
    O,W,W,O,O,O,O,O,O,O,W,W,O,W,O,O,
    O,W,O,O,O,O,O,O,W,W,W,O,W,W,O,O,
    O,W,O,O,O,O,O,O,O,O,O,W,W,W,O,O,
    O,W,O,O,O,O,O,O,O,W,W,W,W,W,O,O,
    O,W,O,O,O,O,O,O,O,O,W,W,W,W,W,O,
    O,W,O,O,O,O,O,O,O,O,W,W,W,W,W,O,
    O,M,M,O,O,O,O,O,O,O,O,O,W,W,W,W,
    O,M,M,M,O,W,W,O,O,O,O,O,O,O,O,O,
]
skull = [
    O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,W,W,W,W,W,O,O,O,O,O,O,
    O,O,O,O,W,W,W,W,W,W,W,O,O,O,O,O,
    O,O,O,O,W,O,O,W,O,O,W,O,O,O,O,O,
    O,O,O,O,W,O,O,W,O,O,W,O,O,O,O,O,
    O,O,O,O,W,W,W,W,W,W,W,O,O,O,O,O,
    O,O,O,O,O,W,W,O,W,W,O,O,O,O,O,O,
    O,O,O,O,O,O,W,W,W,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,W,W,W,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,W,W,W,O,O,O,W,W,W,O,O,O,O,
    O,O,O,O,O,O,W,W,W,O,O,O,O,O,O,O,
    O,O,O,W,W,W,O,O,O,W,W,W,O,O,O,O,
]
explosion_anim = [
    O,O,O,O,O,O,O,O,O,O,O,O,R,O,O,O,
    O,M,O,O,O,O,O,O,O,O,O,O,R,O,O,O,
    M,M,O,O,O,O,O,O,R,O,O,O,R,O,O,O,
    M,M,O,O,O,O,O,O,R,O,O,O,R,O,O,O,
    M,M,O,O,O,O,R,O,O,R,O,O,R,O,R,O,
    O,M,O,O,O,O,O,R,O,R,R,O,R,O,R,O,
    O,O,O,O,O,O,R,R,O,O,R,R,R,O,R,O,
    O,O,O,R,O,O,O,R,O,O,O,R,O,R,R,O,
    O,O,O,O,R,R,O,O,R,O,O,R,R,R,R,R,
    O,O,O,O,O,R,R,O,R,R,O,O,R,R,R,R,
    O,O,O,O,O,O,R,O,O,R,R,O,R,R,R,R,
    O,O,R,R,O,O,R,R,O,R,R,R,R,R,Y,R,
    O,O,O,O,R,R,O,R,R,O,R,R,R,R,Y,Y,
    O,O,O,O,O,R,R,O,R,R,R,R,Y,Y,Y,Y,
    O,O,O,O,O,O,R,R,R,R,R,R,Y,Y,Y,W,
    O,O,O,O,R,R,R,R,R,R,Y,Y,Y,Y,W,W,
]
tnt = [
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,R,O,O,
    O,O,O,O,O,O,O,O,R,R,O,O,
    O,O,O,O,O,O,O,R,R,Y,R,O,
    O,O,O,O,O,O,O,R,Y,Y,R,O,
    O,O,O,O,O,O,O,Z,Y,Y,Z,O,
    O,O,O,O,O,O,V,M,Z,Z,M,V,
    O,O,O,O,O,O,M,V,V,V,V,M,
    O,O,O,O,O,O,M,M,M,M,M,M,
    O,O,O,O,O,O,M,M,M,M,M,M,
    O,O,O,O,O,O,V,M,M,M,M,V,
    O,O,O,O,O,O,M,V,V,V,V,M,
    O,O,O,O,O,O,O,M,M,M,M,O,
]
cactus_hit  = [
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,Z,O,O,O,O,
    O,O,O,O,O,O,G,G,O,O,O,O,
    O,O,O,O,G,O,O,Z,O,G,O,O,
    O,O,O,O,O,O,G,G,O,O,O,G,
    O,O,O,O,O,O,O,O,O,O,O,G,
    O,O,O,O,O,O,O,O,O,O,W,G,
    O,O,O,O,O,O,G,G,O,O,G,Z,
    O,O,O,O,G,O,G,G,Z,G,G,G,
    O,O,O,O,O,O,O,G,G,G,G,O,
    O,O,O,O,O,O,O,O,G,Z,O,O,
    O,O,O,O,O,O,O,O,G,G,O,O,
    O,O,O,O,O,O,O,O,G,G,O,O,
    O,O,O,O,O,O,O,O,Z,G,O,O,
    O,O,O,O,O,O,O,O,G,G,O,O,
]
cactus_idle  = [
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,Z,O,O,O,O,
    O,O,O,O,O,O,G,G,O,O,O,O,
    O,O,O,O,O,O,G,Z,O,O,O,Z,
    O,O,O,O,O,O,G,G,O,O,G,G,
    O,O,O,O,O,O,G,G,O,O,Z,G,
    O,O,O,O,O,O,Z,G,O,O,G,G,
    O,O,O,O,O,O,G,G,O,O,G,Z,
    O,O,O,O,O,O,G,G,Z,G,G,G,
    O,O,O,O,O,O,O,G,G,G,G,O,
    O,O,O,O,O,O,O,O,G,Z,O,O,
    O,O,O,O,O,O,O,O,G,G,O,O,
    O,O,O,O,O,O,O,O,G,G,O,O,
    O,O,O,O,O,O,O,O,Z,G,O,O,
    O,O,O,O,O,O,O,O,G,G,O,O,
]
horse = [
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,V,O,O,O,
    O,O,O,O,O,O,O,M,M,V,O,O,
    O,O,O,O,O,O,M,O,M,V,V,O,
    O,O,O,O,O,O,M,M,M,M,V,V,
    O,O,O,O,O,O,O,O,M,M,M,V,
    O,O,O,O,O,O,O,O,O,M,M,M,
    O,O,O,O,O,O,O,O,O,M,M,M,
    O,O,O,O,O,O,O,O,O,O,M,M,
    O,O,O,O,O,O,O,O,O,O,O,M,
    O,O,O,O,O,O,O,O,O,O,O,M,
    O,O,O,O,O,O,O,O,O,O,O,M,
    O,O,O,O,O,O,O,O,O,O,O,M,
    O,O,O,O,O,O,O,O,O,O,O,M,
]
maniscalco_idle = [
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,M,M,O,
    O,O,O,O,O,O,O,O,O,P,P,M,
    O,O,O,O,O,O,O,O,O,P,P,M,
    O,O,O,O,O,O,O,O,O,O,P,O,
    O,O,O,O,O,O,O,O,O,O,P,O,
    O,O,O,O,O,O,O,O,O,M,M,O,
    O,O,O,O,O,O,O,O,O,M,P,O,
    O,O,O,O,O,O,O,O,O,M,P,O,
    O,O,O,O,O,O,O,O,O,M,P,O,
    O,O,O,O,O,O,O,O,O,M,P,O,
    O,O,O,O,O,O,O,O,O,V,V,O,
    O,O,O,O,O,O,O,O,O,V,V,O,
    O,O,O,O,O,O,O,O,O,V,V,O,
    O,O,O,O,O,O,O,O,O,M,M,O,
    O,O,O,O,O,O,O,O,M,M,M,O,
]

maniscalco_lavoro = [ # Simile ma con i 'ferri' (gialli)
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,M,M,O,
    O,O,O,O,O,O,O,O,O,P,P,M,
    O,O,O,O,O,O,O,O,O,P,P,M,
    O,O,O,O,O,O,O,O,O,O,P,O,
    O,O,O,O,O,O,O,O,O,O,P,O,
    O,O,O,O,O,O,O,O,O,M,M,O,
    O,O,O,O,O,O,O,O,O,M,P,O,
    O,O,O,O,O,O,H,H,H,M,P,O,
    O,O,O,O,O,O,H,O,P,P,P,O,
    O,O,O,O,O,O,H,O,H,M,M,O,
    O,O,O,O,O,O,O,O,O,V,V,O,
    O,O,O,O,O,O,O,O,O,V,V,O,
    O,O,O,O,O,O,O,O,O,V,V,O,
    O,O,O,O,O,O,O,O,O,M,M,O,
    O,O,O,O,O,O,O,O,M,M,M,O,
]

cuore = [
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,R,R,O,O,R,R,O,O,O,
    O,O,R,R,R,R,R,R,R,R,O,O,
    O,O,R,R,R,R,R,R,R,R,O,O,
    O,O,R,R,R,R,R,R,R,R,O,O,
    O,O,O,R,R,R,R,R,R,O,O,O,
    O,O,O,O,R,R,R,R,O,O,O,O,
    O,O,O,O,O,R,R,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,
]
ferro = [
    O,O,O,O,O,M,M,M,M,M,M,O,O,O,O,O,
    O,O,O,O,O,M,M,M,M,M,M,O,O,O,O,O,
    M,M,M,M,M,M,M,M,M,M,M,M,M,M,M,M,
    M,M,M,M,M,M,M,M,M,M,M,M,M,M,M,M,
    O,O,Q,Q,Q,P,P,P,P,P,P,Q,Q,Q,O,O,
    O,O,Q,Q,P,P,R,R,R,R,P,P,Q,Q,O,O,
    O,O,Q,P,P,V,V,R,R,V,V,P,P,Q,O,O,
    O,O,Q,P,R,O,O,P,P,O,O,R,P,Q,O,O,
    O,O,Q,P,R,R,P,P,P,P,R,R,P,Q,O,O,
    O,O,O,P,R,R,P,O,O,P,R,R,P,O,O,O,
    O,O,O,P,P,R,R,P,P,R,R,P,P,O,O,O,
    O,O,O,P,P,R,R,O,O,R,R,P,P,O,O,O,
    O,O,O,P,R,R,O,O,O,O,R,R,P,O,O,O,
    O,O,O,O,P,P,P,P,P,P,P,P,O,O,O,O,
    O,O,O,O,O,P,P,P,P,P,P,O,O,O,O,O,
    O,O,O,O,O,O,P,P,P,P,O,O,O,O,O,O,
]
spine = [
    O,O,O,O,O,M,M,M,M,M,M,O,O,O,O,O,
    O,O,O,O,O,M,M,M,W,M,M,O,O,O,O,O,
    M,M,M,M,W,M,M,M,W,M,M,M,W,M,M,M,
    M,W,M,M,M,W,M,M,M,M,M,W,M,M,W,M,
    O,O,Q,Q,Q,P,P,P,P,P,P,Q,Q,Q,O,O,
    O,O,W,Q,P,P,P,P,P,P,P,P,Q,W,O,O,
    O,O,Q,P,P,O,P,P,P,P,O,P,P,Q,O,O,
    O,O,W,P,P,P,O,P,P,O,P,P,P,Q,O,O,
    O,O,Q,W,P,P,P,P,P,P,P,P,W,W,O,O,
    O,O,O,P,P,P,P,O,O,P,P,P,P,O,O,O,
    O,O,W,W,W,P,M,M,M,M,P,W,W,W,O,O,
    G,G,O,P,P,P,O,O,O,O,P,P,P,O,G,G,
    G,G,G,P,W,P,O,O,O,O,P,P,P,G,G,G,
    G,G,W,G,P,P,P,P,P,P,P,W,G,G,G,O,
    O,W,G,G,G,W,P,P,W,P,P,G,W,G,O,O,
    O,G,G,G,W,G,P,P,W,P,G,G,G,G,W,O,
]
logo = [
    O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,M,M,M,M,M,M,O,O,O,O,O,
    O,O,O,O,O,M,M,M,M,M,M,O,O,O,O,O,
    M,M,M,M,M,M,M,M,M,M,M,M,M,M,M,M,
    M,M,M,M,M,M,M,M,M,M,M,M,M,M,M,M,
    O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,
    Y,Y,O,Y,O,Y,Y,Y,Y,R,O,Y,Y,O,Y,Y,
    Y,O,O,Y,O,O,O,Y,O,O,O,Y,O,O,Y,O,
    Y,Y,Y,Y,O,Y,Y,Y,O,Y,O,Y,Y,O,Y,Y,
    O,Y,O,Y,O,O,O,Y,O,Y,O,Y,O,O,Y,O,
    Y,Y,O,Y,O,Y,Y,Y,O,Y,O,Y,O,O,Y,O,
    O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,
]
woman2 = [
    O,O,O,O,O,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O,O,M,M,O,
    O,O,O,O,O,O,O,O,O,P,P,M,
    O,O,O,O,O,O,O,O,O,P,P,M,
    O,O,O,O,O,O,O,O,O,O,P,M,
    O,O,O,O,O,O,O,O,O,O,L,M,
    O,O,O,O,O,O,O,O,O,L,L,L,
    O,O,O,O,O,O,O,O,O,L,P,L,
    O,O,O,O,O,O,O,O,O,L,P,L,
    O,O,O,O,O,O,O,O,L,L,P,L,
    O,O,O,O,O,O,O,O,L,L,P,L,
    O,O,O,O,O,O,O,O,L,L,P,L,
    O,O,O,O,O,O,O,O,L,L,L,L,
    O,O,O,O,O,O,O,O,L,L,L,L,
    O,O,O,O,O,O,O,O,O,O,M,O,
    O,O,O,O,O,O,O,O,O,M,M,O,
]
empty_character = [BLACK for _ in range(12*16)] # Sprite nero per pulire l'area

# --- Drawing Functions ---
def draw_sprite(sprite, offset_x, offset_y, width, height):
    for y in range(height):
        for x in range(width):
            color = sprite[y * width + x]
            set_pixel(x + offset_x, y + offset_y, color)

def show_animation(anim_sprite):
    clear_matrix()
    draw_sprite(anim_sprite, 0, 0, 16, 16)
    pixels.write()

# --- NUOVA FUNZIONE: MOSTRA PUNTEGGIO ---
def show_score(score):
    clear_matrix()
    score_str = str(score)
    num_digits = len(score_str)
    spacing = 1
    total_width = (num_digits * FONT_WIDTH) + ((num_digits - 1) * spacing)
    
    # Calcola la posizione iniziale per centrare il testo
    start_x = (MATRIX_WIDTH - total_width) // 2
    y_pos = (MATRIX_HEIGHT - FONT_HEIGHT) // 2
    
    current_x = start_x
    for char in score_str:
        if char in FONT:
            font_map = FONT[char]
            for i, pixel in enumerate(font_map):
                if pixel == 1:
                    px = i % FONT_WIDTH
                    py = i // FONT_WIDTH
                    set_pixel(current_x + px, y_pos + py, SCORE_COLOR)
        current_x += FONT_WIDTH + spacing
    pixels.write()

# --- Game States ---
def start_screen():
    clear_matrix()
    show_animation(logo)
    while start_button.value() == 1:
        utime.sleep(0.01)
    if not start_button.value() and not shoot_button.value() and not shoot_button2.value():
        machine.reset() #torno al menù

# --- MODIFICATA: Funzione Game Over ---
def game_over(animation, score):
    # Mostra prima l'animazione della sconfitta
    if animation == "explosion": sound_explosion(); show_animation(explosion_anim)
    elif animation == "skull": sound_game_over(); show_animation(skull)
    elif animation == "ghost": sound_game_over(); show_animation(ghost)
    elif animation == "ferro": sound_game_over(); show_animation(ferro)
    elif animation == "spine": sound_game_over(); show_animation(spine)
    
    utime.sleep(2) # Pausa sull'animazione
    
    # Ora mostra il punteggio finale
    show_score(score)
    utime.sleep(2) # Lascia il punteggio visibile per qualche secondo

def game_loop():
    score = 0
    # Valori di base per la difficoltà
    base_reaction_time = 700
    base_char_stay_time = 1500

    clear_matrix(); draw_sprite(sheriff, 0, 0, 4, 16); pixels.write()
    utime.sleep(2)

    while True:
        # La difficoltà aumenta con il punteggio
        difficulty_modifier = max(0.4, 1 - score * 0.05)
        reaction_time_ms = int(base_reaction_time * difficulty_modifier)
        char_stay_time_ms = int(base_char_stay_time * difficulty_modifier)

        clear_matrix()
        draw_sprite(sheriff, 0, 0, 4, 16)
        
        char_list = [
            "bandit", "bomb", "tnt", "woman", "native_american", "cactus", 
            "horse", "maniscalco", "neutral","woman2"
        ]
        character_type = urandom.choice(char_list)
        
        is_opportunity = False # Indica un'azione positiva (es. maniscalco che lavora)
        
        # Disegna il personaggio
        if character_type == "bandit": draw_sprite(bandit_idle, 4, 0, 12, 16)
        elif character_type in ["bomb", "tnt"]: draw_sprite(bomb, 4, 0, 12, 16) # Usa 'bomb' per entrambi
        elif character_type == "woman": draw_sprite(woman, 4, 0, 12, 16)
        elif character_type == "native_american": draw_sprite(native_american_idle, 4, 0, 12, 16)
        elif character_type == "cactus": draw_sprite(cactus_idle, 4, 0, 12, 16)
        elif character_type == "horse": draw_sprite(horse, 4, 0, 12, 16)
        elif character_type == "woman2": draw_sprite(woman2, 4, 0, 12, 16)
        elif character_type == "maniscalco": draw_sprite(maniscalco_idle, 4, 0, 12, 16)
        else: draw_sprite(empty_character, 4, 0, 12, 16)
        pixels.write()

        start_time = utime.ticks_ms()
        action_taken = False
        is_threat = False

        # Loop di reazione immediata e attesa
        while not action_taken and utime.ticks_diff(utime.ticks_ms(), start_time) < char_stay_time_ms:
            
            # Controlla se il personaggio deve evolvere (diventare minaccia/opportunità)
            time_passed = utime.ticks_diff(utime.ticks_ms(), start_time)
            if not is_threat and not is_opportunity and time_passed > (reaction_time_ms / 2):
                if character_type in ["bandit", "native_american"] and urandom.random() < 0.5:
                    is_threat = True
                    if character_type == "bandit": draw_sprite(bandit_shooting, 4, 0, 12, 16)
                    else: draw_sprite(native_american_bow, 4, 0, 12, 16)
                    pixels.write()
                elif character_type == "maniscalco" and urandom.random() < 0.5:
                    is_opportunity = True
                    draw_sprite(maniscalco_lavoro, 4, 0, 12, 16)
                    pixels.write()

            # --- VERIFICA INPUT DEL GIOCATORE ---
            
            # --- AZIONE: SPARARE ---
            if shoot_button.value() == 0:
                action_taken = True
                draw_sprite(sheriff_shooting, 0, 0, 4, 16); pixels.write()
                sound_shoot()
                draw_sprite(sheriff, 0, 0, 4, 16) # Sprite normale
                
                if is_threat: # Corretto!
                    score += 1; sound_success()
                    if character_type == "bandit": draw_sprite(bandit_dead, 4, 0, 12, 16)
                    else: draw_sprite(native_american_dead, 4, 0, 12, 16)
                    pixels.write(); utime.sleep(1)
                elif character_type in ["bomb", "tnt"]: game_over("explosion", score); return
                elif character_type in ["woman2", "woman", "horse", "maniscalco"]: game_over("ghost", score); return
                elif character_type == "cactus":
                    draw_sprite(cactus_hit, 4, 0, 12, 16); pixels.write(); utime.sleep(1)
                else: game_over("skull", score); return
            
            # --- AZIONE: SCAPPARE ---
            elif run_button.value() == 0:
                action_taken = True
                if character_type in ["bomb", "tnt"]: # Corretto!
                    score += 1; sound_run_success()
                    draw_sprite(empty_character, 4, 0, 12, 16); pixels.write(); utime.sleep(1)
                elif character_type in ["bandit", "native_american"]: # Sbagliato!
                    if character_type == "bandit": draw_sprite(bandit_shooting, 4, 0, 12, 16)
                    else: draw_sprite(native_american_bow, 4, 0, 12, 16)
                    pixels.write(); sound_shoot(); utime.sleep(1)
                    game_over("skull", score); return
                else: # Scappare da personaggi non pericolosi è ok
                    draw_sprite(empty_character, 4, 0, 12, 16); pixels.write(); utime.sleep(1)

            # --- AZIONE: APPROCCIO ---
            elif approach_button.value() == 0:
                action_taken = True
                if character_type == "woman" or character_type == "woman2": # Corretto!
                    score += 1; sound_success()
                    draw_sprite(cuore, 4, 0, 12, 16); pixels.write(); utime.sleep(1)
                elif character_type == "maniscalco" and is_opportunity: # Corretto!
                    score += 1; sound_success()
                    # Puoi creare un'animazione di successo o semplicemente scomparire
                    draw_sprite(empty_character, 4, 0, 12, 16); pixels.write(); utime.sleep(1)
                elif character_type == "horse":
                    game_over("ferro", score)
                    return
                elif character_type in ["bomb", "tnt"]:
                    game_over("explosion", score)
                    return
                elif character_type =="cactus":
                    game_over("spine", score)
                    return
                else: # Sbagliato per tutti gli altri casi!
                    game_over("skull", score)
                    return

        # Fine del round se non è stata intrapresa alcuna azione
        if not action_taken:
            if is_threat or character_type in ["bomb", "tnt"]: # Mancata azione su minaccia
                if character_type in ["bomb", "tnt"]:
                    game_over("explosion", score)
                else:
                    game_over("skull", score)
                return
        
        utime.sleep_ms(150) # Breve pausa tra i round

# --- Programma Principale ---
while True:
    start_screen()
    game_loop()
# depth4.py - Versione compatibile con il Launcher
import machine
import neopixel
import time
import random
import gc
import framebuf

# --- Configurazione hardware ---
NEOPIXEL_PIN = 2
BUTTON_LEFT = 16
BUTTON_RIGHT = 17
BUTTON_BOMB_LEFT = 18
BUTTON_BOMB_RIGHT = 19
BUTTON_START = 20
BUZZER_PIN = 21

# --- Configurazione display ---
MATRIX_WIDTH = 16
MATRIX_HEIGHT = 16
NUM_PIXELS = MATRIX_WIDTH * MATRIX_HEIGHT

# --- Inizializzazione hardware ---
np = neopixel.NeoPixel(machine.Pin(NEOPIXEL_PIN), NUM_PIXELS)
btn_left = machine.Pin(BUTTON_LEFT, machine.Pin.IN, machine.Pin.PULL_UP)
btn_right = machine.Pin(BUTTON_RIGHT, machine.Pin.IN, machine.Pin.PULL_UP)
btn_bomb_left = machine.Pin(BUTTON_BOMB_LEFT, machine.Pin.IN, machine.Pin.PULL_UP)
btn_bomb_right = machine.Pin(BUTTON_BOMB_RIGHT, machine.Pin.IN, machine.Pin.PULL_UP)
btn_start = machine.Pin(BUTTON_START, machine.Pin.IN, machine.Pin.PULL_UP)
buzzer = machine.PWM(machine.Pin(BUZZER_PIN))
buzzer.duty_u16(0)

# --- Colori ---
COLOR_SHIP = (0, 150, 0)
COLOR_BOMB = (100, 100, 0)
COLOR_SUB = (0, 0, 150)
COLOR_TORPEDO = (150, 50, 0)
COLOR_EXPLOSION = (200, 200, 200)
COLOR_DESTROYED = (0, 0, 50)
COLOR_DESTROYED2 = (50, 0, 0)
COLOR_DESTROYED3 = (100, 0, 100)
COLOR_SEA = (0, 0, 15)
COLOR_BLACK = (0, 0, 0)
START_WHITE = (50, 50, 50)
COLOR_SEA_DANGER = (15, 0, 0)
COLOR_SEA_EXTENDED = (15, 15, 0)

# Immagini (omesse per brevità, il codice è identico a quello che hai fornito)
image_sub1 = [
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 0, 0),     (0, 8, 55),     (0, 0, 0),
    (0, 0, 0),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 8, 55),     (0, 0, 0),     (0, 8, 55),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (51, 57, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (51, 57, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (0, 0, 0),     (51, 57, 0),
    (51, 57, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (51, 57, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),
    (51, 57, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (51, 57, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (51, 57, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (55, 44, 0),     (55, 44, 0),
    (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),
    (55, 44, 0),     (55, 44, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (55, 44, 0),     (0, 0, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),
    (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),
    (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (55, 44, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),
]

image_sub2 = [
 (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (55,55,55),     (20, 0, 55),     (20,0,55),     (20,0,55),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (20,0,55),     (55,55,55),     (0, 0, 0),     (20,0,55),     (55,55,55),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (55,55,55),     (20,0,55),     (0, 0, 0),     (55,55,55),     (20,0,55),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (20,0,55),     (20,0,55),     (20,0,55),     (55,55,55),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (55,55,55),     (20,0,55),     (0, 0, 0),     (55,55,55),     (20,0,55),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (51, 57, 0),     (51, 57, 0),     (0, 0, 0),     (0, 0, 0),     (51, 57, 0),     (51, 57, 0),     (0, 0, 0),     (0, 0, 0),     (51, 57, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (51, 57, 0),
    (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),
    (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (51, 57, 0),
    (51, 57, 0),     (0, 0, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (0, 0, 0),     (51, 57, 0),     (51, 57, 0),     (0, 0, 0),     (0, 0, 0),     (51, 57, 0),     (51, 57, 0),
    (51, 57, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (51, 57, 0),     (0, 0, 0),     (51, 57, 0),     (51, 57, 0),
    (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),
    (55, 44, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (55, 44, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (0, 0, 0),     (55, 44, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (55, 44, 0),     (55, 44, 0),
    (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (0, 0, 0),     (0, 0, 0),     (55, 44, 0),
    (55, 44, 0),     (55, 44, 0),     (0, 0, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (55, 44, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),
    (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (0, 0, 0),     (55, 44, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),
    (55, 44, 0),     (55, 44, 0),     (0, 0, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),     (55, 44, 0),     (0, 0, 0),
]
# NOTA: Per far funzionare il codice, devi copiare e incollare qui
# le lunghe liste 'image_sub1' e 'image_sub2' dal tuo file originale.

#Funzione immagine
def show_imagex(image_data):
    for i, color in enumerate(image_data):
        np[i] = color
    np.write()

# --- Funzioni Audio ---
def play_tone(frequency, duration):
    if frequency > 0:
        buzzer.freq(frequency)
        buzzer.duty_u16(2000)
    time.sleep(duration)
    buzzer.duty_u16(0)

def play_bomb_sound(): play_tone(300, 0.05); play_tone(200, 0.05)
def play_torpedo_sound(): play_tone(400, 0.05); play_tone(600, 0.05)
def play_explosion_sound(): play_tone(100, 0.1); play_tone(50, 0.05)

# --- Classi del Gioco ---
class GameObject:
    def __init__(self, x, y, color):
        self.x, self.y, self.color = x, y, color
        self.active = True

class Ship:
    def __init__(self):
        self.x, self.color = 7, COLOR_SHIP
        self.state = "NORMAL"
        self.animation_timer = 0
    def move_left(self):
        if self.state == "NORMAL" and self.x > 1: self.x -= 1
    def move_right(self):
        if self.state == "NORMAL" and self.x < 14: self.x += 1
    def hit(self):
        if self.state == "NORMAL":
            self.state = "SINKING"
            self.animation_timer = 5
    def update(self):
        if self.state != "NORMAL":
            self.animation_timer -= 1
            if self.animation_timer <= 0:
                if self.state == "SINKING":
                    self.state = "GONE"
                    self.animation_timer = 5
                elif self.state == "GONE":
                    self.state = "NORMAL"
    def draw(self, display):
        if self.state == "GONE": return
        color = self.color
        if self.state == "SINKING":
            display.set_pixel(self.x, 1, color)
        else:
            for i in range(3):
                display.set_pixel(self.x - 1 + i, 1, color)
            display.set_pixel(self.x, 0, color)

class Bomb(GameObject):
    def __init__(self, x, direction):
        start_x = x if direction == -1 else x + 1
        super().__init__(start_x, 2, COLOR_BOMB)
        self.direction, self.depth_float = direction, 2.0
        self.target_x = max(0, start_x - 2) if direction == -1 else min(MATRIX_WIDTH - 1, start_x + 2)
        self.start_x, self.move_completed = start_x, False
    def update(self):
        self.depth_float += 0.2; self.depth = int(self.depth_float)
        if self.depth >= MATRIX_HEIGHT - 1: self.active = False
        if not self.move_completed and self.depth_float <= 5.0:
            progress = (self.depth_float - 2.0) / 3.0
            self.x = int(self.start_x + (self.target_x - self.start_x) * progress)
        elif not self.move_completed:
            self.x = self.target_x; self.move_completed = True
        if self.x < 0 or self.x >= MATRIX_WIDTH: self.active = False

class Submarine(GameObject):
    def __init__(self, depth):
        self.depth, self.speed = depth, random.uniform(0.1, 0.3 + depth * 0.05)
        self.direction = random.choice([-1, 1])
        x = -1 if self.direction == 1 else MATRIX_WIDTH
        super().__init__(x, depth, COLOR_SUB)
        self.torpedo_timer = random.randint(15, 50)
        self.points, self.hit_flash = 10 + (depth - 3) * 10 + int(self.speed * 100), 0
    def update(self):
        self.x += self.direction * self.speed
        if self.x < -2 or self.x > MATRIX_WIDTH + 1: self.active = False
        if self.hit_flash > 0: self.hit_flash -= 1
        self.torpedo_timer -= 1
        return self.torpedo_timer <= 0
    def hit(self):
        self.hit_flash, self.active = 8, False
    def fire_torpedo(self, difficulty):
        max_delay, min_delay = 150 - int(110 * difficulty), 70 - int(50 * difficulty)
        self.torpedo_timer = random.randint(min_delay, max_delay)
        return Torpedo(int(self.x), self.y)

class Torpedo(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, COLOR_TORPEDO)
        self.speed = 0.2
    def update(self):
        self.y -= self.speed
        if self.y < 2: self.color = COLOR_SEA
        if self.y < 1: self.active = False

class Display:
    def __init__(self):
        self.buffer = [(0, 0, 0)] * NUM_PIXELS
    def clear(self):
        for i in range(len(self.buffer)): self.buffer[i] = (0,0,0)
    def set_pixel(self, x, y, color):
        if 0 <= x < MATRIX_WIDTH and 0 <= y < MATRIX_HEIGHT:
            index = y * MATRIX_WIDTH + (MATRIX_WIDTH - 1 - x) if y % 2 == 0 else y * MATRIX_WIDTH + x
            if 0 <= index < NUM_PIXELS: self.buffer[index] = color
    def update(self):
        for i in range(NUM_PIXELS): np[i] = self.buffer[i]
        np.write()
        
class Game:
    def __init__(self):
        self.display = Display()
        self.reset()
    def reset(self):
        self.ship = Ship()
        self.bombs, self.submarines, self.torpedoes = [], [], []
        self.score, self.destroyed_subs, self.last_submarine_spawn = 0, 0, 0
        self.game_duration, self.extended_time = 90 * 1000, False
        gc.collect()
    def show_image(self, image, wait_for_press=False):
        for i in range(256): np[i] = image[i]
        np.write()
        if not wait_for_press: return False
        while btn_start.value(): time.sleep(0.05)
        return True
    def _run_scrolling_text(self, text):
        text_width_pixels = len(text) * 8
        buffer_width = text_width_pixels + MATRIX_WIDTH
        buf = bytearray(buffer_width * MATRIX_HEIGHT // 8)
        fb = framebuf.FrameBuffer(buf, buffer_width, MATRIX_HEIGHT, framebuf.MONO_HLSB)
        fb.fill(0); fb.text(text, 0, 4, 1)
        max_offset = buffer_width - MATRIX_WIDTH
        for offset in range(max_offset):
            if not btn_start.value(): return True
            for y in range(MATRIX_HEIGHT):
                for x in range(MATRIX_WIDTH):
                    color = START_WHITE if fb.pixel(x + offset, y) else COLOR_BLACK
                    self.display.set_pixel(x, y, color)
            self.display.update()
            time.sleep(0.04)
        return False
    def update_auto_pilot(self):
        if random.random() < 0.08:
            if random.choice([True, False]): self.ship.move_left()
            else: self.ship.move_right()
        if random.random() < 0.04 and len(self.bombs) < 2:
            self.bombs.append(Bomb(self.ship.x, random.choice([-1, 1])))
            play_bomb_sound()
    def show_start_screen(self):
        state = "IMG1"; state_timer = time.ticks_ms()
        while True:
            if not btn_start.value():
                self.display.clear(); self.display.update(); time.sleep(0.5)
                if not btn_bomb_left.value() and not btn_bomb_right.value():
                    machine.reset() #torno al menù
                return
            
            
            current_time = time.ticks_ms()
            elapsed_in_state = time.ticks_diff(current_time, state_timer)
            if state == "IMG1":
                show_imagex(image_sub1) # Usa la funzione corretta
                state = "WAITING1"; state_timer = time.ticks_ms()
            elif state == "WAITING1":
                if elapsed_in_state > 3000: state = "IMG2"; state_timer = time.ticks_ms(); self.reset()
            elif state == "IMG2":
                show_imagex(image_sub2) # Usa la funzione corretta
                state = "WAITING2"; state_timer = time.ticks_ms()
            elif state == "WAITING2":
                if elapsed_in_state > 4000: state = "DEMO"; state_timer = time.ticks_ms(); self.reset()
            elif state == "DEMO":
                if elapsed_in_state > 15000:
                    state = "IMG1"; state_timer = time.ticks_ms()
                    self.display.clear(); self.display.update(); continue
                self.update_auto_pilot(); self.spawn_submarine()
                self.update_game_objects(0.5); self.check_collisions()
                self.draw(99000); time.sleep(0.05)
    def spawn_submarine(self):
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, self.last_submarine_spawn) > random.randint(1500, 3500):
            occupied_depths = {sub.y for sub in self.submarines}
            available_depths = [d for d in range(3, 14) if d not in occupied_depths]
            if available_depths:
                self.submarines.append(Submarine(random.choice(available_depths)))
                self.last_submarine_spawn = current_time
    def handle_input(self):
        if self.ship.state == "NORMAL":
            if not btn_left.value(): self.ship.move_left(); time.sleep(0.1)
            if not btn_right.value(): self.ship.move_right(); time.sleep(0.1)
            if not btn_bomb_left.value() and len(self.bombs) < 3:
                self.bombs.append(Bomb(self.ship.x, -1)); play_bomb_sound(); time.sleep(0.2)
            if not btn_bomb_right.value() and len(self.bombs) < 3:
                self.bombs.append(Bomb(self.ship.x, 1)); play_bomb_sound(); time.sleep(0.2)
    def update_game_objects(self, difficulty):
        self.ship.update()
        for bomb in self.bombs[:]:
            bomb.update();
            if not bomb.active: self.bombs.remove(bomb)
        for sub in self.submarines[:]:
            if sub.active:
                if sub.update() and 0 <= int(sub.x) < MATRIX_WIDTH:
                    self.torpedoes.append(sub.fire_torpedo(difficulty))
                    play_torpedo_sound()
            else: sub.update()
            if not sub.active and sub.hit_flash <= 0: self.submarines.remove(sub)
        for torpedo in self.torpedoes[:]:
            torpedo.update();
            if not torpedo.active: self.torpedoes.remove(torpedo)
    def check_collisions(self):
        for bomb in self.bombs[:]:
            for sub in self.submarines:
                if sub.active and (abs(bomb.x - sub.x) < 1.5 and abs(bomb.depth - sub.y) < 1):
                    play_explosion_sound(); self.score += sub.points
                    self.destroyed_subs += 1; sub.hit()
                    if bomb in self.bombs: self.bombs.remove(bomb)
                    break 
        for torpedo in self.torpedoes[:]:
            if self.ship.state == "NORMAL" and (torpedo.y <= 2 and abs(torpedo.x - self.ship.x) < 2):
                play_explosion_sound(); self.score = max(0, self.score // 2)
                self.ship.hit()
                if torpedo in self.torpedoes: self.torpedoes.remove(torpedo)
    def draw_destroyed_counter(self):
        level = self.destroyed_subs // 16
        current_count = self.destroyed_subs % 16
        color = COLOR_DESTROYED if level == 0 else (COLOR_DESTROYED2 if level == 1 else COLOR_DESTROYED3)
        if level > 0:
            for i in range(16): self.display.set_pixel(i, 15, COLOR_DESTROYED)
        if level > 1:
            for i in range(16): self.display.set_pixel(i, 15, COLOR_DESTROYED2)
        if level >= 2:
            for i in range(current_count): self.display.set_pixel(i, 15, COLOR_DESTROYED3)
        for i in range(current_count): self.display.set_pixel(i, 15, color)
    def draw(self, time_remaining_ms):
        self.display.clear()
        sea_color = COLOR_SEA
        if self.extended_time: sea_color = COLOR_SEA_EXTENDED
        elif time_remaining_ms < 10000: sea_color = COLOR_SEA_DANGER
        for i in range(16): self.display.set_pixel(i, 2, sea_color)
        self.ship.draw(self.display)
        for bomb in self.bombs: self.display.set_pixel(int(bomb.x), int(bomb.depth), bomb.color)
        for sub in self.submarines:
            x_pos = int(sub.x)
            color = COLOR_EXPLOSION if sub.hit_flash > 0 and sub.hit_flash % 4 < 2 else sub.color
            if 0 <= x_pos < MATRIX_WIDTH: self.display.set_pixel(x_pos, sub.y, color)
            if 0 <= (x_pos - (1 if sub.direction == 1 else -1)) < MATRIX_WIDTH:
                 self.display.set_pixel(x_pos - 1 if sub.direction == 1 else x_pos + 1, sub.y, color)
        for torpedo in self.torpedoes: self.display.set_pixel(int(torpedo.x), int(torpedo.y), torpedo.color)
        self.draw_destroyed_counter()
        self.display.update()
    def show_final_score(self):
        final_score = self.score + (self.destroyed_subs * 30)
        score_text = f"SCORE {final_score}"
        interrupted = self._run_scrolling_text(score_text)
        if interrupted: return
        time.sleep(1)
    def run(self):
        start_time = time.ticks_ms()
        total_duration = self.game_duration
        while True:
            current_time = time.ticks_ms()
            elapsed = time.ticks_diff(current_time, start_time)
            difficulty = min(1.0, elapsed / total_duration)
            if elapsed >= self.game_duration:
                if not self.extended_time and self.destroyed_subs * 30 > 500:
                    self.game_duration += 45 * 1000
                    total_duration = self.game_duration; self.extended_time = True
                else: break
            self.handle_input()
            self.spawn_submarine()
            self.update_game_objects(difficulty)
            self.check_collisions()
            self.draw(self.game_duration - elapsed)
            time.sleep(0.05); gc.collect()
        self.show_final_score()

# <<< MODIFICA: La sezione qui sotto sostituisce la vecchia funzione main() e l'if __name__ == "__main__"
# Questo codice viene eseguito automaticamente quando il file viene importato dal launcher.

# 1. Crea un'istanza del gioco
game = Game()

while True:
# 2. Mostra la schermata iniziale / demo del gioco e attende la pressione del tasto START
    game.show_start_screen()

# 3. Una volta premuto START, azzera lo stato del gioco e avvia la partita vera e propria
    game.reset()
    game.run()

# 4. Alla fine della partita (quando game.run() termina), mostra il punteggio finale
# (La funzione show_final_score è già chiamata alla fine di run())

# 5. Breve pausa per permettere al giocatore di leggere il punteggio
    time.sleep(1)

# 6. Riavvia il Pico per tornare al menù principale del launcher
#machine.reset()
# main.py - Il Launcher per la nostra mini-console

import machine
import neopixel
import time
import os
from icons import ICONS # Importiamo le icone dal nostro file separato

# --- IMPOSTAZIONI HARDWARE (le stesse del gioco) ---
NEOPIXEL_PIN = 2; MATRIX_WIDTH = 16; MATRIX_HEIGHT = 16; NUM_PIXELS = MATRIX_WIDTH * MATRIX_HEIGHT
BUTTON_LEFT_PIN = 16; BUTTON_RIGHT_PIN = 17; BUTTON_START_PIN = 20 # Usiamo il tasto "acceleratore" come START
BUZZER_PIN = 21
Stato = "INTRO"

# --- INIZIALIZZAZIONE HARDWARE ---
pixels = neopixel.NeoPixel(machine.Pin(NEOPIXEL_PIN), NUM_PIXELS)
btn_left = machine.Pin(BUTTON_LEFT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
btn_right = machine.Pin(BUTTON_RIGHT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
btn_start = machine.Pin(BUTTON_START_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
buzzer = machine.PWM(machine.Pin(BUZZER_PIN)); buzzer.duty_u16(0)

# --- LISTA DEI GIOCHI ---
# Aggiungi qui i tuoi giochi. Devono corrispondere ai nomi dei file .py
# L'icona viene presa dal dizionario ICONS
GAMES = [
    {'name': 'LOGO', 'file': '', 'icon': ICONS['logo']},
    {'name': 'SUB', 'file': 'depth4', 'icon': ICONS['sub']},
    {'name': 'SPACE', 'file': 'invaders', 'icon': ICONS['invaders']},
    {'name': 'BREAK', 'file': 'breakout', 'icon': ICONS['arkanoid']},
    {'name': 'RACE', 'file': 'cars', 'icon': ICONS['race']},
    {'name': 'PXMAN', 'file': 'pixelman', 'icon': ICONS['pacman']},
    {'name': 'PONG', 'file': 'pong', 'icon': ICONS['pong']},
    {'name': 'SHERIFF', 'file': 'sheriff', 'icon': ICONS['sheriff']}
]

# Variabili di stato del menù
selected_index = 1
BLACK = (0, 0, 0)
WHITE = (20, 20, 20)

# --- FUNZIONI DEL LAUNCHER ---
def play_tone(frequency, duration_ms):
    if frequency > 0: buzzer.freq(frequency); buzzer.duty_u16(32768)
    time.sleep_ms(duration_ms)
    buzzer.duty_u16(0)

def draw_icon(icon_data):
    """Disegna un'icona 16x16 sullo schermo."""
    pixels.fill(BLACK)
    for y, row_data in enumerate(icon_data):
        for x, color in enumerate(row_data):
            if color: # Se il colore non è None o (0,0,0)
                # La mappatura a serpentina viene gestita qui
                if y % 2 == 0: # Riga RTL
                    idx = y * MATRIX_WIDTH + (MATRIX_WIDTH - 1 - x)
                else: # Riga LTR
                    idx = y * MATRIX_WIDTH + x
                pixels[idx] = color
    pixels.write()

def launch_game(filename):
    """Lancia il gioco selezionato."""
    # Animazione di caricamento
    pixels.fill(BLACK)
    # Disegna una barra di caricamento
    for i in range(MATRIX_WIDTH):
        if i % 2 == 0: play_tone(800 + i * 50, 20)
        # La mappatura a serpentina viene gestita qui
        y = MATRIX_HEIGHT // 2
        if y % 2 == 0: idx = y * MATRIX_WIDTH + (MATRIX_WIDTH - 1 - i)
        else: idx = y * MATRIX_WIDTH + i
        pixels[idx] = WHITE
        pixels.write()
        time.sleep_ms(10)
        
    print(f"Avvio del gioco: {filename}.py...")
    
    try:
        # Questo è il comando magico che carica ed esegue il file del gioco
        __import__(filename)
    except ImportError:
        # Se il file non esiste, torna al menù dopo un errore
        print(f"Errore: file {filename}.py non trovato!")
        time.sleep(2)
        machine.reset() # Riavvia e torna al menù

# --- CICLO PRINCIPALE DEL MENÙ ---
while True:
    if Stato == "INTRO":
        draw_icon(GAMES[0]['icon'])
        time.sleep_ms(4000)
        Stato = "MENU"
        
    # 1. Disegna l'icona del gioco selezionato
    draw_icon(GAMES[selected_index]['icon'])
    #print(f"Gioco selezionato: {GAMES[selected_index]['name']}")
    
    # 2. Attendi un input dall'utente
    while True:
        # Naviga a destra
        if btn_right.value() == 0:
            play_tone(600, 50)
            selected_index = (selected_index + 1) % len(GAMES)
            if selected_index == 0:
                selected_index = 1
            time.sleep_ms(200) # Debounce per evitare pressioni multiple
            break # Esci dal ciclo di attesa per ridisegnare
        
        # Naviga a sinistra
        if btn_left.value() == 0:
            play_tone(500, 50)
            selected_index = (selected_index - 1 + len(GAMES)) % len(GAMES)
            if selected_index == 0:
                selected_index = len(GAMES)-1
            time.sleep_ms(200) # Debounce
            break # Esci per ridisegnare
            
        # Lancia il gioco
        if btn_start.value() == 0:
            play_tone(1200, 100)
            launch_game(GAMES[selected_index]['file'])
            # Il codice qui sotto non verrà mai raggiunto, perché launch_game
            # o lancia un gioco che prende il controllo, o riavvia.
        
        time.sleep_ms(10)
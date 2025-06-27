🎮 Pixel Arcade

Pixel Arcade è un mini cabinato arcade stampato in 3D, basato sulla struttura OraQuadra di Davide Gatti, pensato per portare il divertimento retro direttamente sul tuo tavolo!
È un progetto open-source che unisce elettronica, stampa 3D e programmazione in MicroPython su Raspberry Pi Pico 2040.

📦 Caratteristiche principali

    Mini struttura stampata in 3D (basata su OraQuadra)

    Display 16x16 LED RGB con tecnologia NeoPixel

    Controllato da una Raspberry Pi Pico 2040

    5 pulsanti fisici per il controllo dei giochi

    Software sviluppato in MicroPython

    7 giochi inclusi

    Un programma principale main.py che funge da launcher per i giochi

🕹️ Giochi inclusi

Attualmente nel sistema sono installati 7 giochi, ognuno progettato per sfruttare la semplicità e lo stile grafico retro del display 16x16.

Sub Hunt, Space, Block, Race, PxMan, Pong, Sheriff

Il programma principale main.py consente di selezionare e avviare ogni gioco direttamente dal mini cabinato.


🧰 Componenti

Struttura stampata in 3D : https://makerworld.com/it/models/1554656-bartop-pixel-arcade-game#profileId-1633266
	
**Materiale utilizzato - link Amazon/Aliexpress:**
	
Pulsante START: 7mm PBS-110

- https://amzn.eu/d/9DxOjs4
	
- https://it.aliexpress.com/item/1005008333401098.html
	
Pulsanti: Pulsante 16MM 3A 
	
- https://amzn.eu/d/bFmCU81
	
- https://it.aliexpress.com/item/1005001709481942.html
	
Pannello 16x16 WS2812B: 
	
- https://amzn.eu/d/deiAU8E
	
- https://it.aliexpress.com/item/4001298469994.html
	
Raspberry PI PICO RP20240 16M Black:
	
- https://amzn.eu/d/30erm6Y
	
- https://it.aliexpress.com/item/1005006128042609.html
	
Barrel jack connector 5.5-2.1:
	
- https://amzn.eu/d/fFGX126
	
- https://it.aliexpress.com/item/4000583899030.html
	
Alimentatore 5V 2A 5.5-2.1:
	
- https://amzn.eu/d/hgM6a9a
	
- https://it.aliexpress.com/item/32844702891.html

Alimentazione 5V per pannello LED e RP2040 (Vin)
	

🧑‍💻 Come caricare MicroPython e i giochi
1. Installare MicroPython sul Raspberry Pi Pico

    Tieni premuto il tasto BOOTSEL sul Raspberry Pi Pico e collegalo al PC via USB.

    Il Pico verrà montato come un’unità USB (es: RPI-RP2).

    Scarica l'ultima versione del firmware MicroPython per Pico da qui.

    Copia il file .uf2 nella memoria del Pico. Il Pico si riavvierà automaticamente con MicroPython installato.

2. Installare e configurare Thonny

    Scarica e installa Thonny da thonny.org.

    Avvia Thonny e vai su Strumenti → Opzioni → Interprete.

    Scegli:

        Interprete: MicroPython (Raspberry Pi Pico)

        Porta: lascia su Automatico o seleziona quella corretta

    Collega il Pico via USB: se tutto è corretto, Thonny mostrerà una console Python attiva.

3. Caricare i giochi nel Pico

    Dal menu di Thonny, apri ciascun file .py contenuto nella cartella del progetto.

    Per ogni file, fai clic su File → Salva con nome.

    Scegli Dispositivo MicroPython e salva il file con lo stesso nome (es: main.py, game1.py, ecc.).

    Assicurati che main.py sia presente: questo file viene eseguito automaticamente all’avvio del Pico.

📸 Immagini del progetto

![alt text](https://github.com/zeus074/Pixel-Arcade/blob/main/img/pixel_arcade2.jpg)

![alt text](https://github.com/zeus074/Pixel-Arcade/blob/main/img/pixel_arcade4.jpg)

![alt text](https://github.com/zeus074/Pixel-Arcade/blob/main/img/block.gif)

![alt text](https://github.com/zeus074/Pixel-Arcade/blob/main/img/pixel_arcade3.jpg)


📄 <a href="https://github.com/zeus074/Pixel-Arcade/blob/main/schematic/Schematic_Pixel_Arcade.pdf">Schema dei collegamenti</a>

Trovare il firmware da caricare su RP2040 nella cartella firmware.

📎 Ringraziamenti

A Davide Gatti (Survival Hacking) per la base OraQuadra su cui si basa la struttura del cabinato.

https://github.com/SurvivalHacking/OraQuadra
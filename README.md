# SenseHub

SenseHub è un progetto IoT che integra hardware Arduino con un'interfaccia web per monitorare in tempo reale dati ambientali attraverso vari sensori. 
Il gruppo è formato da:
-Didonè Matteo
-Battistutta Davide
-Vuaran Davide
-Mio Roberto 
-Burello Federico

## 📝 Descrizione

Il progetto è composto da tre componenti principali:
1. Un circuito Arduino che raccoglie dati da sensori ambientali
2. Un server Python che processa i dati e li memorizza in MongoDB
3. Un'interfaccia web che visualizza i dati in tempo reale

### Sensori utilizzati
- DHT11: Temperatura e umidità
- Fotoresistenza (LDR): Livello di luce
- Sensore PIR: Rilevamento movimento
- Sensore sonoro: Livello di rumore

## 🛠 Requisiti Hardware

- Arduino Uno/Nano
- Sensore DHT11
- Fotoresistenza (LDR)
- Sensore PIR
- Sensore sonoro
- Resistenze e cavi di collegamento

## 💻 Requisiti Software

- Python 3.x
- MongoDB
- Arduino IDE
- Librerie Python:
  - Flask
  - PyMongo
  - PySerial
  - Flask-CORS

## ⚡️ Configurazione

1. **Arduino**
   - Collega i sensori secondo lo schema:
     - DHT11 al pin 2
     - LDR al pin A0
     - Sensore sonoro al pin A1
     - PIR al pin 3
   - Carica il file `sensor_controller.ino` su Arduino

2. **MongoDB**
   - Installa MongoDB
   - Avvia il servizio MongoDB

3. **Python**
   ```bash
   # Crea un ambiente virtuale
   python -m venv .venv
   source .venv/bin/activate  # Per Unix
   # oppure
   .venv\Scripts\activate  # Per Windows

   # Installa le dipendenze
   pip install flask flask-cors pymongo pyserial
   ```

## 🚀 Avvio

1. Assicurati che Arduino sia collegato e che la porta seriale sia corretta nel file `main.py`
2. Avvia il server Python:
   ```bash
   python main.py
   ```
3. Apri il browser e visita `http://localhost:5000`

## 📊 Funzionalità

- Visualizzazione in tempo reale di:
  - Temperatura (°C)
  - Umidità (valore raw 0-1024)
  - Livello di luce (valore raw 0-1024)
  - Livello sonoro (valore raw 0-1024)
  - Stato del sensore di movimento
- Grafici storici per temperatura e umidità
- Interfaccia responsive e dark mode
- Aggiornamento automatico dei dati ogni 2 secondi

## 🔧 Struttura del Progetto

```
python-sensehub/
├── main.py                 # Server Python e logica backend
├── sensor_controller.ino   # Codice Arduino
└── templates/
    └── index.html         # Interfaccia web
```

## ⚙️ Configurazione Avanzata

- La porta seriale può essere modificata in `main.py`
- L'intervallo di aggiornamento può essere modificato sia nel codice Arduino che nel frontend
- La connessione MongoDB può essere configurata per un database remoto
- I grafici storici possono essere personalizzati modificando i parametri in index.html

## 🔍 Risoluzione Problemi

1. **Errore porta seriale**
   - Verifica che Arduino sia collegato
   - Controlla il nome della porta seriale corretta
   - Su Mac/Linux potrebbe richiedere permessi

2. **Errore MongoDB**
   - Verifica che MongoDB sia in esecuzione
   - Controlla i log per errori di connessione

3. **Dati non visualizzati**
   - Controlla la console del browser per errori
   - Verifica che il server Flask sia in esecuzione
   - Controlla la connessione seriale Arduino

## 📜 License

Questo progetto è distribuito con licenza MIT. Vedere il file `LICENSE` per maggiori dettagli.

- [Flask](https://flask.palletsprojects.com/)
- [MongoDB](https://www.mongodb.com/)
- [Chart.js](https://www.chartjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [DaisyUI](https://daisyui.com/)
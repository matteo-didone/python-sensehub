from flask import Flask, render_template, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import datetime
import serial
from threading import Thread

app = Flask(__name__)
CORS(app)

# Configurazione MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["arduino_serial_data"]
collection = db["serial_data"]

class Data:
    def __init__(self, temperature=0.0, humidity=0, light=0, movement=bool, sound=0):
        self.temperature = temperature
        self.humidity = humidity
        self.light = light
        self.movement = movement
        self.sound = sound

def parse_serial_data(message):
    try:
        parts = message.split()
        data = Data()

        for i in range(0, len(parts), 2):
            key = parts[i][0]  # Identificazione della lettera
            value_str = parts[i + 1].replace(',', '.')  # Converte le virgole in punti
            
            if key == 'T':
                data.temperature = float(value_str)  # Temperatura rimane in °C
            elif key == 'H':
                data.humidity = int(float(value_str))  # Valore raw 0-1024
            elif key == 'L':
                data.light = int(float(value_str))    # Valore raw 0-1024
            elif key == 'M':
                data.movement = bool(int(float(value_str)))  # Booleano
            elif key == 'S':
                data.sound = int(float(value_str))    # Valore raw 0-1024

        return data
    except (IndexError, ValueError) as e:
        print(f"Errore nel parsing dei dati! Errore: {e}")
        print(f"Messaggio ricevuto: {message}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data/current')
def get_current_data():
    # Prende i dati più recenti dal database
    latest_data = list(collection.find().sort([('_id', -1)]).limit(1))
    if latest_data:
        return jsonify({
            'temperature': float(latest_data[0].get('Temperature', 0)),
            'humidity': float(latest_data[0].get('Humidity', 0)),
            'light': float(latest_data[0].get('Light', 0)),
            'movement': bool(latest_data[0].get('Movement', False)),
            'sound': float(latest_data[0].get('Sound', 0))
        })
    return jsonify({
        'temperature': 0,
        'humidity': 0,
        'light': 0,
        'movement': False,
        'sound': 0
    })

@app.route('/api/data/history/<sensor>')
def get_sensor_history(sensor):
    # Ultimi 10 record per il sensore specificato
    history = list(collection.find().sort([('_id', -1)]).limit(10))
    
    if history:
        return jsonify([{
            'timestamp': record.get('timestamp'),
            'value': record.get(sensor, 0)
        } for record in history])
    return jsonify([])

def read_serial():
    try:
        arduino = serial.Serial(port='/dev/tty.usbmodem101', baudrate=9600)
        print("Seriale pronta a ricevere dati\n")
        
        while True:
            if arduino.in_waiting > 0:
                serial_msg = arduino.readline()
                serial_msg = serial_msg.decode('utf-8')
                
                serial_data = parse_serial_data(serial_msg)
                
                if serial_data:
                    record = {
                        "timestamp": datetime.datetime.now(),
                        "Temperature": serial_data.temperature,
                        "Humidity": serial_data.humidity,
                        "Light": serial_data.light,
                        "Movement": serial_data.movement,
                        "Sound": serial_data.sound
                    }
                    
                    try:
                        collection.insert_one(record)
                        print(f"Dati inseriti: {record}")
                    except Exception as e:
                        print(f"Errore nell'inserimento dei dati in Mongo! Errore: {e}")
                        
    except Exception as e:
        print(f"Errore nella lettura seriale: {e}")

if __name__ == '__main__':
    # Avvia la lettura seriale in un thread separato
    serial_thread = Thread(target=read_serial, daemon=True)
    serial_thread.start()
    
    # Avvia il server Flask
    app.run(debug=True, port=5000)
#include <DHT.h>
#include <String.h>

#define DHTPIN 2      // Pin a cui è collegato il DHT11
#define DHTTYPE DHT11 // Tipo di sensore
#define LDRPIN A0     // Pin a cui è collegata la fotoresistenza
#define SOUNDPIN A1   // Pin a cui è collegato il sensore di suono
#define PIRPIN 3      // Pin digitale a cui è collegato il sensore PIR

DHT dht(DHTPIN, DHTTYPE); // Inizializza il sensore DHT11

unsigned long lastPrintTime = 0;     // Tiene traccia dell'ultima volta che i dati sono stati stampati
const unsigned long interval = 2000; // Intervallo di stampa (2 secondi)

float umidita = 0;
float temperatura = 0;
int ldrValue = 0;
int soundValue = 0;
int pirValue = 0;

void setup()
{
    Serial.begin(9600);     // Avvia la comunicazione seriale
    dht.begin();            // Inizializza il sensore DHT11
    pinMode(PIRPIN, INPUT); // Imposta il pin del PIR come input
}

void loop()
{
    // Letture continue dei sensori
    umidita = dht.readHumidity();
    temperatura = dht.readTemperature();
    ldrValue = analogRead(LDRPIN);
    soundValue = analogRead(SOUNDPIN);
    pirValue = digitalRead(PIRPIN);

    // Controlla se è tempo di stampare i dati
    if (millis() - lastPrintTime >= interval)
    {
        lastPrintTime = millis(); // Aggiorna il tempo dell'ultima stampa

        // Controlla se ci sono errori durante la lettura del DHT11
        if (isnan(umidita) || isnan(temperatura))
        {
            Serial.println("Errore nella lettura del sensore DHT11");
        }
        else
        {
            // Crea una stringa con tutti i valori
            String output = "T: " + String(temperatura) + "    ";
            output += "H: " + String(umidita) + "    ";
            output += "L: " + String(ldrValue) + "    ";
            output += "S: " + String(soundValue) + "    ";
            output += "M: " + String(pirValue);

            // Stampa la stringa sulla seriale
            Serial.println(output);
        }
    }
}
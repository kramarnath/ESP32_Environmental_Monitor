# ESP32 Environmental Monitor

An IoT environmental monitoring system built on ESP32 and MicroPython that reads temperature and humidity using a DHT11 sensor, logs data to ThingSpeak for live graphing, and sends threshold-based alerts via a Telegram bot.

---

## Features

- **Real-time sensing** — reads temperature and humidity every 60 seconds via DHT11
- **Cloud logging** — pushes data to ThingSpeak (Field 1: Temp, Field 2: Humidity) over HTTP
- **Live dashboard** — visualise sensor data on ThingSpeak's built-in web graphs
- **Telegram alerts** — sends an instant message when temperature exceeds 35°C
- **LED feedback** — onboard LED (GPIO 12) blinks on every successful ThingSpeak upload
- **WiFi auto-connect** — reconnects automatically on startup

---

## Hardware Required

| Component | Quantity |
|-----------|----------|
| ESP32 DevKit | 1 |
| DHT11 Temperature & Humidity Sensor | 1 |
| Jumper wires | ~4 |
| Breadboard | 1 |

**Wiring:**

| DHT11 Pin | ESP32 Pin |
|-----------|-----------|
| VCC | 3.3V |
| GND | GND |
| DATA | GPIO 4 |

> LED blink feedback uses GPIO 12

## Cicuit 

<table>
  <tr>
    <td align="center"><img src="images/Weather-monitor_ckt.jpg" alt="Cicuit" height="200"/></td>
  </tr>
</table>


---

## Software & Libraries

- [MicroPython](https://micropython.org/) — firmware for ESP32
- `dht` — built-in MicroPython DHT11 driver
- `network` — built-in WiFi module
- `urequests` — lightweight HTTP client for MicroPython
- [Thonny IDE] — for flashing files

---

## Project Structure

```
ESP32-Environmental-Monitor/
├── firmware/                      # Entry point — runs on boot
│   ├── esp32_env_monitor.py       # Sensor read + ThingSpeak HTTP upload         
│   └── config.py                  # WiFi credentials, API keys, thresholds
├── docs/                          # Threshold alert via Telegram Bot API
│   ├── circuit_diagram.png
│   ├── thingspeak_screenshot.png
│   └── telegram_alert_screenshot.png
├── .gitignore
├── LICENSE
└── README.md
```

---

## Setup & Configuration

### 1. Flash MicroPython on ESP32
Download the latest MicroPython firmware to ESP32 using Thonny IDE:

### 2. Clone this repository

### 3. Configure credentials

### 4. Upload files to ESP32
Using Thonny: open each `.py` file and use **File → Save as → MicroPython device (as main.py)**.

### 5. Monitor output
Open Thonny's shell or any serial terminal at 115200 baud. You should see:

### 6. View the dashboard
Go to your ThingSpeak channel → **Private View** or **Public View** to see live graphs for temperature and humidity.

### 7. Monitor the bot after increasing the temperature above threshold:
You will get a message saying "Temperature_Exceeded_the_Limit: threshold_value C"

<table>
  <tr>
    <td align="center"><img src="images/tele_bot_msg.png" alt="telegram Message" height="200"/></td>
  </tr>
</table>

---

## How It Works

```
DHT11 Sensor
     │
     ▼
ESP32 (MicroPython)
     ├── Every 30s: HTTP GET → ThingSpeak API  →  Live Web Graph
     └── If temp > threshold_value°C: HTTP GET → Telegram Bot API  →  Phone Alert
```

1. On boot, ESP32 connects to WiFi
2. Every 30 seconds, `sensor.measure()` reads temperature and humidity
3. Both values are sent to ThingSpeak via an HTTP GET request (`field1=temp&field2=humidity`)
4. ThingSpeak response `1` = success; `0` or `-1` = rate limit or error
5. If temperature exceeds the threshold, a separate GET request fires the Telegram message
6. The onboard LED blinks once to confirm a successful upload

> **Note:** The 60-second interval respects ThingSpeak's free plan limit of one update per 15 seconds. Communication is via direct HTTP.

## Thingspeak Data

<table>
  <tr>
    <td align="center"><img src="images/field1_temp" alt="Temperature Plot" height="200"/></td>
    <td align="center"><img src="images/fiels2_humi.jpg" alt="Humidity plot" height="200"/></td>
  </tr>
</table>

---

## Telegram Bot Setup

1. Message @BotFather on Telegram
2. Send `/newbot` and follow the prompts to get your **Bot Token**
3. Start a chat with your new bot, then visit:
   `https://api.telegram.org/bot<TOKEN>/getUpdates`
4. Copy the `chat.id` value from the response — that is your **Chat ID**
5. Paste these in the appropriate section of the code
---

## Future Improvements

I am planning to do an Edge tinyml anomaly detector using the ESP32 

> So this project was basically built for  **data collection** for a TinyML ESP32 project.
> Instead of hardcoded thresholds (`if temp > 35`), a tiny ML model will learn what *normal* looks like
> and flag anomalies automatically — no cloud inference

---

## License

MIT License — see [LICENSE](LICENSE) for details.

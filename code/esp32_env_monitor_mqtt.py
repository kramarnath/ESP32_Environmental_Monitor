import machine
import dht
import network
import urequests
import time
from umqtt.simple import MQTTClient
import time
time.sleep(3)  # gives ESP32 time to stabilize before running

# ── WiFi ──────────────────────────────────────────────────────────────────────
SSID     = "your_ssid"
PASSWORD = "your_password"

# ── ThingSpeak via MQTT ───────────────────────────────────────────────────────
# These come from ThingSpeak → your channel → API Keys tab
THINGSPEAK_MQTT_CLIENT_ID = "your_client_id"
THINGSPEAK_MQTT_USER      = "your_thingspeak_username"
THINGSPEAK_MQTT_PASSWORD  = "your_thingspeak_mqtt_api_key"   # The MQTT API key
THINGSPEAK_CHANNEL_ID     = "your_channel_id"       # Numeric

MQTT_BROKER = "mqtt3.thingspeak.com"   # ThingSpeak's own MQTT broker
MQTT_PORT   = 1883

# The topic ThingSpeak expects
PUBLISH_TOPIC = "channels/" + THINGSPEAK_CHANNEL_ID + "/publish"

# ── Telegram ──────────────────────────────────────────────────────
TOKEN   = "your_bot_token"
CHAT_ID = "your_chat_id"

# ── Hardware ──────────────────────────────────────────────────────
sensor = dht.DHT11(machine.Pin(4))
led    = machine.Pin(12, machine.Pin.OUT)

TEMP_THRESHOLD = 35   # °C

# ── WiFi ──────────────────────────────────────────────────────────
def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)
    while not wifi.isconnected():
        time.sleep(0.5)
    print("WiFi connected:", wifi.ifconfig()[0])


# ── MQTT connect ──────────────────────────────────────────────────────────────
def connect_mqtt():
    client = MQTTClient(
        client_id = THINGSPEAK_MQTT_CLIENT_ID,
        server    = MQTT_BROKER,
        port      = 1883,
        user      = THINGSPEAK_MQTT_USER,
        password  = THINGSPEAK_MQTT_PASSWORD,
        keepalive = 60
    )
    client.connect()
    print("MQTT connected to", MQTT_BROKER)
    return client



# ── Telegram alert ──────────────────────────
def send_telegram_alert(temp):
    try:
        url = (
            "https://api.telegram.org/bot" + TOKEN +
            "/sendMessage?chat_id=" + CHAT_ID +
            "&text=Temperature_Exceeded_the_Limit:" + str(temp) + "C"
        )
        response = urequests.get(url)
        print("Telegram alert sent:", response.text)
        response.close()
    except Exception as e:
        print("Telegram error:", e)


# ── Main ──────────────────────────────────────────────────────────────────────
connect_wifi()
mqtt_client = connect_mqtt()

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        humidity = sensor.humidity()
        payload = "field1=" + str(temp) + "&field2=" + str(humidity)
        mqtt_client.publish(PUBLISH_TOPIC, payload)
        led.on()
        time.sleep(0.3)
        led.off()
    except OSError as e:
        print("MQTT lost, reconnecting...", e)
        try:
            mqtt_client = connect_mqtt()
        except Exception as re:
            print("Reconnect failed:", re)
    except Exception as e:
        print("Sensor error:", e)

    time.sleep(60)


while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        humidity = sensor.humidity()
        payload = "field1=" + str(temp) + "&field2=" + str(humidity)
        mqtt_client.publish(PUBLISH_TOPIC, payload)
        led.on()
        time.sleep(0.3)
        led.off()

        if temp > TEMP_THRESHOLD:
            send_telegram_alert(temp)

    except OSError as e:
        print("MQTT lost, reconnecting...", e)
        try:
            mqtt_client = connect_mqtt()
        except Exception as re:
            print("Reconnect failed:", re)
    except Exception as e:
        print("Sensor error:", e)

        if temp > TEMP_THRESHOLD:     
            send_telegram_alert(temp)

    time.sleep(60)

# main_mqtt.py  
# Publishes to ThingSpeak via MQTT

import machine
import dht
import network
import urequests
import time
from umqtt.simple import MQTTClient

time.sleep(3)  # gives ESP32 time to stabilize before running

# WiFi credentials
SSID     = "your_ssid"
PASSWORD = "your_password"

# ThingSpeak MQTT configuration
THINGSPEAK_MQTT_CLIENT_ID = "your_client_id"
THINGSPEAK_MQTT_USER      = "your_thingspeak_username"
THINGSPEAK_MQTT_PASSWORD  = "your_thingspeak_mqtt_api_key"
THINGSPEAK_CHANNEL_ID     = "your_channel_id"
MQTT_BROKER               = "mqtt3.thingspeak.com"
MQTT_PORT                 = 1883
PUBLISH_TOPIC             = "channels/" + THINGSPEAK_CHANNEL_ID + "/publish"

# Telegram configuration
TOKEN   = "your_bot_token"
CHAT_ID = "your_chat_id"

# Setup sensor
sensor = dht.DHT11(machine.Pin(4))

# LED at PIN 12
led = machine.Pin(12, machine.Pin.OUT)

# Temperature threshold
threshold_temp = 35  # in celsius

# Connect WiFi
def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)
    while not wifi.isconnected():
        time.sleep(0.5)
    print("WiFi connected:", wifi.ifconfig()[0])

# Connect MQTT
def connect_mqtt():
    client = MQTTClient(
        client_id = THINGSPEAK_MQTT_CLIENT_ID,
        server    = MQTT_BROKER,
        port      = MQTT_PORT,
        user      = THINGSPEAK_MQTT_USER,
        password  = THINGSPEAK_MQTT_PASSWORD,
        keepalive = 60
    )
    client.connect()
    print("MQTT connected to", MQTT_BROKER)
    return client

# Main loop
connect_wifi()
mqtt_client = connect_mqtt()

while True:
    try:
        sensor.measure()
        temp     = sensor.temperature()
        humidity = sensor.humidity()

        # Publish to ThingSpeak
        payload = "field1=" + str(temp) + "&field2=" + str(humidity)
        mqtt_client.publish(PUBLISH_TOPIC, payload)
        print("Sent - Temp:", temp, "Humidity:", humidity)

        # Blink LED after successful publish
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
        print("Error:", e)

    if temp > threshold_temp:
        try:
            url = "https://api.telegram.org/bot" + TOKEN + "/sendMessage?chat_id=" + CHAT_ID + "&text=Temperature_Exceeded_the_Limit:" + str(temp) + "C"
            response = urequests.get(url)
            print(response.text)
            response.close()
        except Exception as e:
            print("Error:", e)

    time.sleep(60)

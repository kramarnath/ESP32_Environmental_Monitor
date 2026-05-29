import machine
import dht
import network
import urequests
import time

# WiFi data
SSID = "your_ssid"
PASSWORD = "your_password"

# ThingSpeak configuration
API_KEY = "your_thingspeak_api_key"
URL = "https://api.thingspeak.com/update"

# Telegram configuration
TOKEN = "your_bot_token"
CHAT_ID = "chat_id"

# Setup sensor
sensor = dht.DHT11(machine.Pin(4))

# LED at PIN 12
led = machine.Pin(12, machine.Pin.OUT)

# Temperature threshold
threshold_temp = 35  # in celcius

# Connect WiFi
def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)
    while not wifi.isconnected():
        time.sleep(0.5)
    print("WiFi connected:", wifi.ifconfig()[0])


# Main loop
connect_wifi()

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        humidity = sensor.humidity()
        
        # Send to ThingSpeak
        full_url = URL + "?api_key=" + API_KEY
        full_url += "&field1=" + str(temp)
        full_url += "&field2=" + str(humidity)
        
        response = urequests.get(full_url)
        print("Sent - Temp:", temp, "Humidity:", humidity)
        print("ThingSpeak response:", response.text)
        response.close()
        
        # Blink LED after successful upload
        led.on()
        time.sleep(0.3)
        led.off()
        
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

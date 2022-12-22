from pydos_wifi import Pydos_wifi  
ssid = Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID')  
pswd = Pydos_wifi.getenv('CIRCUITPY_WIFI_PASSWORD')  
result = Pydos_wifi.connect(ssid, pswd) 
text_url = "http://wifitest.adafruit.com/testwifi/index.html"  
response = Pydos_wifi.get(text_url)  
# since not using ssl can read data without testing for end of stream  
print(Pydos_wifi.next(1000).decode('utf-8'))  
Pydos_wifi.close()

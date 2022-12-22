from pydos_wifi import Pydos_wifi  
ssid = Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID')  
pswd = Pydos_wifi.getenv('CIRCUITPY_WIFI_PASSWORD')  
result = Pydos_wifi.connect(ssid, pswd) 
text_url = "https://httpbin.org/get"  
response = Pydos_wifi.get(text_url,None,True)  
print(Pydos_wifi.json())  
Pydos_wifi.close()  

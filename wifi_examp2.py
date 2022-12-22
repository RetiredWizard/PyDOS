from pydos_wifi import Pydos_wifi  
# .5 second timeout, Pydos_wifi.next will wait this long before returning b''  
# if this is too short, could find false end of data on slow networks  
Pydos_wifi.timeout = 500 # default is 15000 (15 seconds)  
ssid = Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID')  
pswd = Pydos_wifi.getenv('CIRCUITPY_WIFI_PASSWORD')  
result = Pydos_wifi.connect(ssid, pswd) 
text_url = "https://httpbin.org/get"  
response = Pydos_wifi.get(text_url)  
# If running on CircuitPython this loop can be replaced with **getRes = Pydos_wifi.next(1000)**  
getRes = b''  
nxtByte = None  
while nxtByte != b'':  
    nxtByte = Pydos_wifi.next(1)  
    getRes += nxtByte  

print(getRes.decode('utf-8'))  
Pydos_wifi.close()  

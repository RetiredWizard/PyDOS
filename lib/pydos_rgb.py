from sys import implementation
from pydos_hw import Pydos_hw

if implementation.name.upper() == "CIRCUITPYTHON":
    import board

    if Pydos_hw.boardName == 'arduino_nano_rp2040_connect':
        from digitalio import DigitalInOut
        import busio
    else:
        pass

elif implementation.name.upper() == 'MICROPYTHON':
    import machine
    import time

class PyDOS_rgb:

    _rgblist = [[()]]
    _esp32_cs = [None]
    _esp32_ready = [None]
    _esp32_reset = [None]
    _spi = [None]
    _pixels = [None]
    _leds = [None,None,None]
    _neoName = [None]


    def __init__(self, neoName: str=None, pSize: int=0, autoWrite: bool=True, pOrder: str="RGB"):
        if pSize:
            self.size = pSize
        else:
            self.size = len(self._rgblist[0])
        self._firstWrite = 0
        self._esp = None
        self._nano_connect = False
        self._autoWrite = autoWrite

        if neoName != None:
            neoName = neoName.upper().replace("'","").replace('"','')
        if neoName != self._neoName[0]:
            print("Setting data pin",neoName if neoName != None else "Default")
            self.deinit()
        elif self._pixels[0] and len(self._pixels[0]) != self.size:
            print("Resetting pixels due to size change")
            self.deinit()
        self._neoName[0] = neoName

        if len(self._rgblist[0]) != self.size or self._rgblist[0] == [()]:
            self._rgblist[0] = [(0,0,0)]*self.size

        neoPin = Pydos_hw.neoPixel
        if implementation.name.upper() == 'CIRCUITPYTHON':
            if neoName:
                try:
                    neoPin = getattr(board,neoName)
                except:
                    print("neopixel pin specified but not found, ignoring...")

            if Pydos_hw.boardName == 'arduino_nano_rp2040_connect' and not neoPin:
                from adafruit_esp32spi import adafruit_esp32spi as _esp32spi
                self._nano_connect = True
                #  uses the secondary SPI connected through the ESP32
                if not self._spi[0]:
                    self._spi[0] = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)

                #  ESP32 pins
                if not self._esp32_cs[0]:
                    self._esp32_cs[0] = DigitalInOut(board.ESP_CS)
                if not self._esp32_ready[0]:
                    self._esp32_ready[0] = DigitalInOut(board.ESP_BUSY)
                if not self._esp32_reset[0]:
                    self._esp32_reset[0] = DigitalInOut(board.ESP_RESET)
            elif Pydos_hw.LED_RED and Pydos_hw.LED_GREEN and Pydos_hw.LED_BLUE and not neoPin:
                import pwmio
                if not self._leds[0]:
                    self._leds[0] = pwmio.PWMOut(Pydos_hw.LED_RED)
                if not self._leds[1]:
                    self._leds[1] = pwmio.PWMOut(Pydos_hw.LED_GREEN)
                if not self._leds[2]:
                    self._leds[2] = pwmio.PWMOut(Pydos_hw.LED_BLUE)
                self._pixels[0] = [True]
                self.size = 1

        elif implementation.name.upper() == 'MICROPYTHON':
            if neoName:
                try:
                    try:
                        neoPin = neoName
                        neoPin = int(neoName)
                    except:
                        pass
                    neoPin = machine.Pin(neoPin)
                except:
                    print("neopixel pin specified but not found, ignoring...")

            if Pydos_hw.neoPixel_Pow:
                Pydos_hw.neoPixel_Pow.on()

            if Pydos_hw.boardName == 'Arduino Nano RP2040 Connect with RP2040' and not neoPin:
                import mp_esp32spi as _esp32spi
                self._nano_connect = True

                #  uses the secondary SPI connected through the ESP32
                if not self._spi[0]:
                    self._spi[0] = machine.SPI(1)

                #  ESP32 pins
                self._esp32_cs[0] = machine.Pin(9,machine.Pin.OUT)
                self._esp32_ready[0] = machine.Pin(10,machine.Pin.IN)
                self._esp32_reset[0] = machine.Pin(3,machine.Pin.OUT)
            elif Pydos_hw.LED_RED and Pydos_hw.LED_GREEN and Pydos_hw.LED_BLUE and not neoPin:
                try:
                    self._leds[0] = machine.PWM(machine.Pin(Pydos_hw.LED_RED,machine.Pin.OUT))
                    self._leds[1] = machine.PWM(machine.Pin(Pydos_hw.LED_GREEN,machine.Pin.OUT))
                    self._leds[2] = machine.PWM(machine.Pin(Pydos_hw.LED_BLUE,machine.Pin.OUT))
                except:
                    try:
                        # See if old micropython PWM is available (i.e. nrf chips)
                        self._leds[0] = machine.PWM(0,pin=machine.Pin(Pydos_hw.LED_RED, \
                            machine.Pin.OUT),period=10000,freq=1000,duty=50)
                        self._leds[1] = machine.PWM(1,pin=machine.Pin(Pydos_hw.LED_GREEN, \
                            machine.Pin.OUT),period=10000,freq=1000,duty=50)
                        self._leds[2] = machine.PWM(2,pin=machine.Pin(Pydos_hw.LED_BLUE, \
                            machine.Pin.OUT),period=10000,freq=1000,duty=50)
                    except:
                        # if can't find a working PWM simple on/off logic is used
                        self._leds[0] = machine.Pin(Pydos_hw.LED_RED,machine.Pin.OUT)
                        self._leds[1] = machine.Pin(Pydos_hw.LED_GREEN,machine.Pin.OUT)
                        self._leds[2] = machine.Pin(Pydos_hw.LED_BLUE,machine.Pin.OUT)

                self._pixels[0] = [True]
                self.size = 1

        if self._nano_connect:
            self.size = 1
            self._pixels[0] = [True]
            if not self._esp:
                self._esp = _esp32spi.ESP_SPIcontrol(self._spi[0], self._esp32_cs[0], \
                    self._esp32_ready[0], self._esp32_reset[0])
        
        if not self._pixels[0]:
            if Pydos_hw.dotStar_Clock or neoPin:
                if neoPin:
#                    try:
#                        import ws2812
        # Could add new Pydos_hw.SPI_NeoPixel variable, but just setting to 1 for now
#                        self._pixels[0] = ws2812.WS2812(spi_bus=1, led_count=self.size, intensity=1)
#                    except:
                    import neopixel
                    try:
                        self._pixels[0] = neopixel.NeoPixel(neoPin, self.size, auto_write=self._autoWrite)
                    except:
                        self._pixels[0] = neopixel.NeoPixel(neoPin, self.size)
                elif Pydos_hw.dotStar_Clock:
                    if implementation.name.upper() == 'CIRCUITPYTHON':
                        import adafruit_dotstar
                        self._pixels[0] = adafruit_dotstar.DotStar(Pydos_hw.dotStar_Clock, \
                            Pydos_hw.dotStar_Data, self.size, auto_write=self._autoWrite)
                        if Pydos_hw.dotStar_Pow:
                            Pydos_hw.dotStar_Pow = 0
                    elif implementation.name.upper() == 'MICROPYTHON':
                        from dotstar import DotStar
                        if not self._spi[0]:
                            self._spi[0] = machine.SoftSPI(sck=machine.Pin(Pydos_hw.dotStar_Clock), \
                                mosi=machine.Pin(Pydos_hw.dotStar_Data), \
                                miso=machine.Pin(Pydos_hw.dotStar_Extra))
                        self._pixels[0] = DotStar(self._spi[0], self.size)
                        if Pydos_hw.dotStar_Pow:
                            machine.Pin(Pydos_hw.dotStar_Pow).value(0)
            else:
                print("Neopixel/Dotstar not found")
                self.size = 0

    def __len__(self):
        return self.size

    def __setitem__(self,indx,rgb):
        self._rgblist[0][indx] = rgb

        if self._nano_connect:
#            if rgb == (0,0,0) and implementation.name.upper() == 'CIRCUITPYTHON':
#                # Hack to completly turn off RGB LED
#                from adafruit_esp32spi import adafruit_esp32spi as _esp32spi
#                self._spi.deinit()
#                self._spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)
#                self._esp = _esp32spi.ESP_SPIcontrol(self._spi, self._esp32_cs, \
#                    self._esp32_ready, self._esp32_reset)
#
#                # Second possible Hack method to turn off RGB LED
#                try:
#                    self._esp32_reset.value(0)
#                except:
#                    self._esp32_reset.value = 0
#            else:
            if True:
                r, g, b = rgb
                self._esp.set_analog_write(27,(255-r)/255)
                self._esp.set_analog_write(25,(255-g)/255)
                self._esp.set_analog_write(26,(255-b)/255)
        elif implementation.name.upper() == 'CIRCUITPYTHON':
            if self._leds[0]:
                self._leds[0].duty_cycle = int(((255-rgb[0])/255)*65535)
                self._leds[1].duty_cycle = int(((255-rgb[1])/255)*65535)
                self._leds[2].duty_cycle = int(((255-rgb[2])/255)*65535)
            else:
                self._pixels[0][indx] = rgb
        elif implementation.name.upper() == 'MICROPYTHON':
            if self._leds[0]:
                if 'duty' in dir(self._leds[0]):
                    try:
                        self._leds[0] = machine.PWM(0,pin=machine.Pin(Pydos_hw.LED_RED), \
                            period=10000,freq=1000,duty=int(((255-rgb[0])/255)*100))
                        self._leds[0].init()
                        self._leds[1] = machine.PWM(1,pin=machine.Pin(Pydos_hw.LED_GREEN), \
                            period=10000,freq=1000,duty=int(((255-rgb[1])/255)*100))
                        self._leds[1].init()
                        self._leds[2] = machine.PWM(2,pin=machine.Pin(Pydos_hw.LED_BLUE), \
                            period=10000,freq=1000,duty=int(((255-rgb[2])/255)*100))
                        self._leds[2].init()
                    except:
                        self._leds[0].duty(int(((255-rgb[0])/255)*1023))
                        self._leds[1].duty(int(((255-rgb[1])/255)*1023))
                        self._leds[2].duty(int(((255-rgb[2])/255)*1023))
                elif 'duty_u16' in dir(self._leds[0]):
                    self._leds[0].duty_u16(int(((255-rgb[0])/255)*1023))
                    self._leds[1].duty_u16(int(((255-rgb[1])/255)*1023))
                    self._leds[2].duty_u16(int(((255-rgb[2])/255)*1023))
                else:
                    self._leds[0].value(rgb[0]==0)
                    self._leds[1].value(rgb[1]==0)
                    self._leds[2].value(rgb[2]==0)
            else:
                self._pixels[0][indx] = rgb
                # Hack for esp32c3 chips hanging after multiples writes without sleep
                if "C3" in Pydos_hw.boardName.upper():
                    if self._firstWrite % 25 == 0:
                        time.sleep(.02)
                    self._firstWrite += 1
                if self._autoWrite:
                    if 'write' in dir(self._pixels[0]):
                        self._pixels[0].write()
                    elif 'show' in dir(self._pixels[0]):
                        self._pixels[0].show()


    def __getitem__(self,indx):
        return self._rgblist[0][indx]

    def fill(self,rgb):
        for i in range(self.size):
            self.__setitem__(i,rgb)

    def write(self):
        for i in range(self.size):
            self.__setitem__(i,self._rgblist[0][i])
        try:
            self._pixels[0].write()
        except:
            self._pixels[0].show()

    def show(self):
        self.write()

    def deinit(self):
        if self._nano_connect:
            try:
                self._esp32_reset[0].value = 0
            except:
                self._esp32_reset[0].value(0)
            if implementation.name.upper() == 'CIRCUITPYTHON':
                self._esp32_cs[0].deinit()
                self._esp32_ready[0].deinit()
                self._esp32_reset[0].deinit()
            self._esp32_cs[0] = None
            self._esp32_ready[0] = None
            self._esp32_reset[0] = None
            self._spi[0].deinit()
            self._spi[0] = None
            self._nano_connect = False

        if Pydos_hw.neoPixel_Pow:
            try:
                Pydos_hw.neoPixel_Pow.off()
            except:
                pass

        if implementation.name.upper() == 'CIRCUITPYTHON':
            if self._leds[0]:
                self._leds[0].deinit()
                self._leds[0] = None
            if self._leds[1]:
                self._leds[1].deinit()
                self._leds[1] = None
            if self._leds[2]:
                self._leds[2].deinit()
                self._leds[2] = None

        try:
            self._pixels[0].deinit()
        except:
            pass
        self._pixels[0] = None
        self._rgblist[0] = [()]
        self._neoName[0] = None

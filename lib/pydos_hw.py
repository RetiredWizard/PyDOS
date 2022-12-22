"""
    GPIO abstraction layer

"""
from sys import implementation
from pydos_bcfg import Pydos_pins
if implementation.name.upper() == "MICROPYTHON":
    from machine import Pin
    from machine import SoftI2C as s_I2C
    from machine import I2C as m_I2C
    from machine import SoftSPI as s_SPI
    from machine import SPI as m_SPI

elif implementation.name.upper() == "CIRCUITPYTHON":
    try:
        from adafruit_bus_device.i2c_device import I2CDevice
    except:
        pass
    import digitalio
    import busio
    import board

    try:
        import adafruit_sdcard
        del adafruit_sdcard
        csAsPin = False
    except:
        csAsPin = True

    if board.board_id == "unexpectedmaker_feathers2":
        try:
            import kfw_s2_board as board
        except ImportError:
            pass
    elif board.board_id == "raspberry_pi_pico":
        try:
            import kfw_pico_board as board
            foundBoard = True
        except ImportError:
            foundBoard = False

        if not foundBoard:
            try:
                import cyt_mpp_board as board
            except ImportError:
                pass

class PyDOS_HW:

    _I2C = None
    _I2C_power = None
    _SPI = []
    sndPin = None
    sndGPIO = None
    neoPixel = None
    neoPixel_Pow = None
    dotStar_Clock = None
    dotStar_Data = None
    dotStar_Extra = None
    dotStar_Pow = None
    led = None
    I2C_NUM = None
    SCL = None
    SDA = None
    SPI_NUM = []
    SCK = []
    MOSI = []
    MISO = []
    CS = []
    I2CbbqDevice = None
    KFW = False
    SD = []
    SDdrive = []
    
    def __init__(self):

        self.sndPin = Pydos_pins.get('sndPin',(None,None))[0]
        self.neoPixel = Pydos_pins.get('neoPixel',(None,None))[0]
        self.neoPixel_Pow = Pydos_pins.get('neoPixel_Pow',(None,None))[0]
        self.dotStar_Clock = Pydos_pins.get('dotStar_Clock',(None,None))[0]
        self.dotStar_Data = Pydos_pins.get('dotStar_Data',(None,None))[0]
        self.dotStar_Pow = Pydos_pins.get('dotStar_Pow',(None,None))[0]
        self.dotStar_Extra = Pydos_pins.get('dotStar_Extra',(None,None))[0]
        self.led = Pydos_pins.get('led',(None,None))[0]

        if implementation.name.upper() == 'MICROPYTHON':
            if self.sndPin:
                self.sndPin = Pin(self.sndPin)

            if self.neoPixel:
                self.neoPixel = Pin(self.neoPixel)

            if self.neoPixel_Pow:
                self.neoPixel_Pow = Pin(self.neoPixel_Pow,Pin.OUT)

        self.I2C_NUM=Pydos_pins.get('I2C_NUM',(None,None))[0]
        self.SCL=Pydos_pins.get('SCL',(None,None))[0]
        self.SDA=Pydos_pins.get('SDA',(None,None))[0]
        for i in range(len(Pydos_pins.get('SCK',[]))):
            self.SCK.append((Pydos_pins['SCK'][i])[0])
            self.MOSI.append((Pydos_pins['MOSI'][i])[0])
            self.MISO.append((Pydos_pins['MISO'][i])[0])
            self.CS.append((Pydos_pins['CS'][i])[0])
            if len(Pydos_pins.get('SPI_NUM',[])) > i:
                self.SPI_NUM.append((Pydos_pins['SPI_NUM'][i])[0])
            else:
                self.SPI_NUM.append(None)
            self.SDdrive.append(None)
            self.SD.append(None)
            self._SPI.append(None)

            if implementation.name.upper() == 'CIRCUITPYTHON':
                if not csAsPin:
                    if self.CS[i]:
                        self.CS[i] = digitalio.DigitalInOut(self.CS[i])

        if implementation.name.upper() == 'CIRCUITPYTHON':
            if not self.led:
                if 'LED1' in dir(board):
                    self.led = board.LED1
                elif 'LED' in dir(board):
                    self.led = board.LED

            if self.dotStar_Pow:
                self.dotStar_Pow = digitalio.DigitalInOut(self.dotStar_Pow)
                self.dotStar_Pow.direction = digitalio.Direction.OUTPUT

            if self.sndPin:
                self.sndGPIO = digitalio.DigitalInOut(self.sndPin)
                self.sndGPIO.direction = digitalio.Direction.OUTPUT
                self.sndGPIO.value = False

            try:
                chkForFile = open('/lib/kfw_pico_board.py','r')
                chkForFile.close()
                self.KFW = True
            except:
                pass
            if not self.KFW:
                try:
                    chkForFile = open('/lib/kfw_s2_board.py','r')
                    chkForFile.close()
                    self.KFW = True
                except:
                    pass

            if self.KFW:
                self.neoPixel = board.D11
            elif self.neoPixel is None and 'NEOPIXEL' in dir(board):
                self.neoPixel = board.NEOPIXEL

    def I2C(self):

        if not self._I2C:
            if implementation.name.upper() == "CIRCUITPYTHON":

                if 'I2C_POWER_INVERTED' in dir(board) and not self._I2C_power:
                    self._I2C_power = digitalio.DigitalInOut(board.I2C_POWER_INVERTED)
                    self._I2C_power.direction = digitalio.Direction.OUTPUT
                    self._I2C_power.value = False

                if 'STEMMA_I2C' in dir(board):
                    self._I2C = board.STEMMA_I2C()
                elif 'I2C' in dir(board):
                    self._I2C = board.I2C()
                else:
                    self._I2C = busio.I2C(self.SCL, self.SDA)

                if self.KFW and not self.I2CbbqDevice:
                    self.I2CbbqDevice = I2CDevice(self._I2C, 0x1F)
            elif implementation.name.upper() == "MICROPYTHON":
                if self.I2C_NUM:
                    #self._I2C = m_I2C(self.I2C_NUM,scl=Pin(self.SCL),sda=Pin(self.SDA))
                    self._I2C = m_I2C(self.I2C_NUM)
                else:
                    self._I2C = s_I2C(scl=Pin(self.SCL),sda=Pin(self.SDA))

        return self._I2C

    def I2C_deinit(self):
        if implementation.name.upper() == "CIRCUITPYTHON":
            if self._I2C_power:
                self._I2C_power.deinit()
                self._I2C_power = None

            if self._I2C:
                self._I2C.deinit()
            self._I2C = None
            self.I2CbbqDevice = None

    def SPI_deinit(self,spiNo=0):
        if self._SPI[spiNo]:

            self._SPI[spiNo].deinit()
            self._SPI[spiNo] = None

    def SPI(self,spiNo=0):
        if not self._SPI[spiNo]:
            if implementation.name.upper() == "CIRCUITPYTHON":
                if spiNo == len(self._SPI)-1 and 'SPI' in dir(board):
                    self._SPI[spiNo] = board.SPI()
                elif spiNo == 0 and 'SD_SPI' in dir(board):
                    self._SPI[spiNo] = board.SD_SPI()
                else:
                    if spiNo+1 <= len(Pydos_hw.SCK):
                        trybitbangio = False
                        try:
                            self._SPI[spiNo] = busio.SPI(self.SCK[spiNo], self.MOSI[spiNo], self.MISO[spiNo])
                        except ValueError:
                            trybitbangio = True

                        if trybitbangio:
                            try:
                                import bitbangio
                            except ImportError:
                                trybitbangio = False
                                print('SPI Create Fail')

                        if trybitbangio:
                            self._SPI[spiNo] = bitbangio.SPI(self.SCK[spiNo], self.MOSI[spiNo], self.MISO[spiNo])
                    else:
                        print("SPI pins not defined for requested SPI interface #",spiNo)

            elif implementation.name.upper() == "MICROPYTHON":
                if self.SPI_NUM[spiNo] != None:
                    self._SPI[spiNo] = m_SPI(self.SPI_NUM[spiNo])
                else:
                    if self.SCK[spiNo]:
                        self._SPI[spiNo] = s_SPI(sck=Pin(self.SCK[spiNo]), \
                            mosi=Pin(self.MOSI[spiNo]),miso=Pin(self.MISO[spiNo]))
        return self._SPI[spiNo]

Pydos_hw = PyDOS_HW()
sndPin = Pydos_hw.sndPin
sndGPIO = Pydos_hw.sndGPIO

def quietSnd():

    if implementation.name.upper() == "CIRCUITPYTHON":
        if sndPin:
            Pydos_hw.sndGPIO = digitalio.DigitalInOut(sndPin)
            #self.sndGPIO.direction = digitalio.Direction.OUTPUT
    return


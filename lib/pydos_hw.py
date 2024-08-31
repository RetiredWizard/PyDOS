"""
    GPIO abstraction layer

"""
from sys import implementation
from pydos_bcfg import Pydos_pins
if implementation.name.upper() == "MICROPYTHON":
    from machine import Pin
    from machine import SoftI2C as s_I2C
    from machine import I2C as m_I2C
    try:
        from machine import SoftSPI as s_SPI
    except:
        pass
    from machine import SPI as m_SPI
    try:
        from os import uname
    except:
        pass

elif implementation.name.upper() == "CIRCUITPYTHON":
    try:
        from adafruit_bus_device.i2c_device import I2CDevice
    except:
        pass
    import digitalio
    import busio
    import board

    if board.board_id == "unexpectedmaker_feathers2":
        try:
            import kfw_s2_board as board
        except ImportError:
            pass
    elif board.board_id == "raspberry_pi_pico":
        try:
            import kfw_pico_board as board
        except ImportError:
            pass

        if 'kfw' not in dir(board):
            try:
                import cyt_mpp_board as board
            except ImportError:
                pass

class PyDOS_HW:

    I2CbbqDevice = None
    
    def __init__(self):

        self._I2C = [None,None,None,None]
        self._SPI = []
        self.SPI_NUM = []
        self.SCK = []
        self.MOSI = []
        self.MISO = []
        self.CS = []
        self.SD = []
        self.SDdrive = []
        self.sndGPIO = None
        self.KFW = False
#       self._I2C_power = None
        self.boardName = None
        if implementation.name.upper() == 'CIRCUITPYTHON':
            self.boardName = board.board_id
        elif implementation.name.upper() == 'MICROPYTHON':
            try:
                self.boardName = uname().machine
            except:
                pass
            try:
                self.boardName = implementation._machine
            except:
                pass

        self.sndPin = Pydos_pins.get('sndPin',(None,None))[0]
        self.i2sSCK = Pydos_pins.get('i2s_BitClock',(None,None))[0]
        self.i2sWS = Pydos_pins.get('i2s_WordSelect',(None,None))[0]
        self.i2sDATA = Pydos_pins.get('i2s_Data',(None,None))[0]
        self.neoPixel = Pydos_pins.get('neoPixel',(None,None))[0]
        self.neoPixel_Pow = Pydos_pins.get('neoPixel_Pow',(None,None))[0]
        self.dotStar_Clock = Pydos_pins.get('dotStar_Clock',(None,None))[0]
        self.dotStar_Data = Pydos_pins.get('dotStar_Data',(None,None))[0]
        self.dotStar_Pow = Pydos_pins.get('dotStar_Pow',(None,None))[0]
        self.dotStar_Extra = Pydos_pins.get('dotStar_Extra',(None,None))[0]
        self.led = Pydos_pins.get('led',Pydos_pins.get('LED_RED',(None,None)))[0]
        self.LED_RED = Pydos_pins.get('LED_RED',(None,None))[0]
        self.LED_GREEN = Pydos_pins.get('LED_GREEN',(None,None))[0]
        self.LED_BLUE = Pydos_pins.get('LED_BLUE',(None,None))[0]

        if implementation.name.upper() == 'MICROPYTHON':
            if self.sndPin != None:
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

        self.SDIO_CLK=Pydos_pins.get('SDIO_CLK',(None,None))[0]
        self.SDIO_CMD=Pydos_pins.get('SDIO_CMD',(None,None))[0]
        self.SDIO_DPINS=Pydos_pins.get('SDIO_DPINS',([None],None))[0]
        if self.SDIO_CLK:
            self.SDdrive.append(None)
            self.SD.append(None)        

            if implementation.name.upper() == 'CIRCUITPYTHON':
                try:
                    if i == 0:
                        import adafruit_sdcard
                        del adafruit_sdcard
                    if i == 0 or type(self.CS[i-1]) == digitalio.DigitalInOut:
                        if self.CS[i]:
                            self.CS[i] = digitalio.DigitalInOut(self.CS[i])
                except:
                    pass

        if implementation.name.upper() == 'CIRCUITPYTHON':
            if not self.i2sSCK:
                if 'I2S_BIT_CLOCK' in dir(board):
                    try:
                        self.i2sWS = board.I2S_WORD_SELECT
                        self.i2sDATA = board.I2S_DATA
                        self.i2sSCK = board.I2S_BIT_CLOCK
                    except:
                        self.i2sWS = None
                elif 'SPEAKER_SCK' in dir(board):
                    try:
                        self.i2sWS = board.SPEAKER_WS
                        self.i2sDATA = board.SPEAKER_DOUT
                        self.i2sSCK = board.SPEAKER_SCK
                    except:
                        self.i2sWS = None
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

    def I2C(self,i2cNo=0):
    # i2cNo = 0 returns first available I2C device in this order of availablity:
    #       CircuitPython: board.STEMMA_I2C, board.I2C, busio.I2C(SCL,SDA)
    #       MicroPython: machine.I2C(I2C_NUM if defined), else machine.SoftI2C(SCL,SDA)
    #         If default I2C is SoftI2C do not configure I2C_NUM or set it to None
    # i2cNo = 1 returns first available I2C device in the following order:
    #       CircuitPython: board.I2C, busio.I2C(SCL,SDA)
    #       MicroPython: machine.I2C((I2C_NUM+1)%2 if defined), else machine.SoftI2C(SCL,SDA)
    # i2cNo = 2 returns busio.I2C(SCL,SDA) for CircuitPython, SoftI2c(SCL,SDA) for MicroPython

        if not self._I2C[i2cNo]:
            if implementation.name.upper() == "CIRCUITPYTHON":

                #if 'I2C_POWER_INVERTED' in dir(board) and not self._I2C_power:
                #    self._I2C_power = digitalio.DigitalInOut(board.I2C_POWER_INVERTED)
                #    self._I2C_power.direction = digitalio.Direction.OUTPUT
                #    self._I2C_power.value = False

                if 'STEMMA_I2C' in dir(board) and i2cNo == 0:
                    self._I2C[i2cNo] = board.STEMMA_I2C()
                elif 'I2C' in dir(board) and i2cNo in [0,1]:
                    self._I2C[i2cNo] = board.I2C()
                elif self.SCL and i2cNo in [0,1,2]:
                    # dangerous bus as 0 or 1 may use these pins. reserve 0 and 1 first
                    for i in [0,1]:
                        if i2cNo == i:
                            break
                        self.I2C(i)
                    self._I2C[i2cNo] = busio.I2C(self.SCL, self.SDA)
                elif 'SCL1' in dir(board) and i2cNo in [0,1,2,3]:
                    # dangerous bus as 0,1 or 2 may use these pins. reserve 0,1 and 2 first
                    for i in [0,1,2]:
                        if i2cNo == i:
                            break
                        self.I2C(i)
                    self._I2C[i2cNo] = busio.I2C(board.SCL1, board.SDA1)

                if self.KFW and not self.I2CbbqDevice and i2cNo == 0:
                    self.I2CbbqDevice = I2CDevice(self._I2C[i2cNo], 0x1F)
            elif implementation.name.upper() == "MICROPYTHON":
                if self.I2C_NUM != None:
                    if i2cNo == 0:
                        #self._I2C = m_I2C(self.I2C_NUM,scl=Pin(self.SCL),sda=Pin(self.SDA))
                        try:
                            self._I2C[i2cNo] = m_I2C(self.I2C_NUM)
                        except:
                            self._I2C[i2cNo] = m_I2C(self.I2C_NUM,scl=Pin(self.SCL),sda=Pin(self.SDA))
                    elif i2cNo == 1:
                        try:
                            self._I2C[i2cNo] = m_I2C((self.I2C_NUM+1)%2)
                        except:
                            self._I2C[i2cNo] = m_I2C((self.I2C_NUM+1)%2,scl=Pin(self.SCL),sda=Pin(self.SDA))

                if not self._I2C[i2cNo]:
                    try:
                        self._I2C[i2cNo] = s_I2C(scl=Pin(self.SCL),sda=Pin(self.SDA))
                    except:
                        pass

        return self._I2C[i2cNo]

    def I2C_deinit(self,i2cNo=0):
        if implementation.name.upper() == "CIRCUITPYTHON":
            if self._I2C[i2cNo]:
                self._I2C[i2cNo].deinit()
            self._I2C[i2cNo] = None

            if i2cNo == 0:
                self.I2CbbqDevice = None
                #if self._I2C_power:
                #    self._I2C_power.deinit()
                #    self._I2C_power = None

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
                        reuseSPI = -1
                        for i in range(len(self._SPI)):
                            if i != spiNo and self._SPI[i]:
                                if self.SCK[i] == self.SCK[spiNo]:
                                    reuseSPI = i
                        try:
                            if reuseSPI == -1:
                                self._SPI[spiNo] = busio.SPI(self.SCK[spiNo], self.MOSI[spiNo], self.MISO[spiNo])
                            else:
                                self._SPI[spiNo] = self._SPI[reuseSPI]
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
                    try:
                        self._SPI[spiNo] = m_SPI(self.SPI_NUM[spiNo],sck=Pin(self.SCK[spiNo]), \
                            mosi=Pin(self.MOSI[spiNo]),miso=Pin(self.MISO[spiNo]))
                    except:
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


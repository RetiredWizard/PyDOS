from time import sleep_ms
from sys import path as syspath
from uos import mount as uosmount
from uos import umount as uosumount
from machine import Pin, SPI

_BAUD = const(0x500000) #5 Mb ~ can be overwritten in SDCard constructor

class SDCard(object):
    @property
    def drive(self)->int:
        return self.__drive

    @property
    def sectors(self) -> int:
        return self.__sectors

    @property
    def type(self) -> int:
        return self.__type

    def __init__(self, spi:int, sck:int, mosi:int, miso:int, cs:int, baudrate:int=_BAUD, mount:bool=True, drive:str="/sd") -> None:
        self.__sd = SDObject(SPI(spi, sck=Pin(sck, Pin.OUT), mosi=Pin(mosi, Pin.OUT), miso=Pin(miso, Pin.OUT)), Pin(cs, Pin.OUT), baudrate)

        self.__drive   = drive
        self.__type    = self.__sd.type
        self.__sectors = self.__sd.sectors

        if mount:
            self.mount()

    def mount(self) -> None:
        print('{} Mounted'.format(self.__drive))
        uosmount(self.__sd, self.__drive)
        syspath.append(self.__drive)

    def eject(self) -> None:
        print('{} Ejected'.format(self.__drive))
        uosumount(self.__drive)
        syspath.remove(self.__drive)


_IOCTL_INIT         = const(1)
_IOCTL_DEINIT       = const(2)
_IOCTL_SYNC         = const(3)
_IOCTL_BLK_COUNT    = const(4)
_IOCTL_BLK_SIZE     = const(5)
_IOCTL_BLK_ERASE    = const(6)

_CMD0               = const(0x40)    # CMD0 : init card; should return _IDLE_STATE
_CMD8               = const(0x48)    # CMD8 : determine card version
_CMD9               = const(0x49)    # CMD9 : response R2 (R1 byte + 16-byte block read)
_CMD12              = const(0x4C)    # CMD12: forces card to stop transmission in Multiple Block Read Operation
_CMD16              = const(0x50)    # CMD16: set block length to 512 bytes
_CMD17              = const(0x51)    # CMD17: set read address for single block
_CMD18              = const(0x52)    # CMD18: set read address for multiple blocks
_CMD24              = const(0x58)    # CMD24: set write address for single block
_CMD25              = const(0x59)    # CMD25: set write address for first block
_CMD41              = const(0x69)    # CMD41: host capacity support information / activates card's initialization process.
_CMD55              = const(0x77)    # CMD55: next command is app command
_CMD58              = const(0x7a)    # CMD58: read OCR register. CCS bit is assigned to OCR[30]

_FF                 = b'\xFF'
_BLOCK              = const(0x200)

_CMD_TIMEOUT        = const(100)

_IDLE_STATE         = const(0x01)
_ILLEGAL_CMD        = const(0x04)

_TOKEN_CMD25        = const(0xFC)
_TOKEN_STOP_TRAN    = const(0xFD)
_TOKEN_DATA         = const(0xFE)


class SDObject(object):
    def __init__(self, spi, cs:int, baudrate:int=_BAUD) -> None:
        self.spi, self.cs = spi, cs
        self.cs.init(self.cs.OUT, value=1)
        self.spi.init(baudrate=100000, phase=0, polarity=0)

        self.tokenbuf = bytearray(1)
        self.buf_mv   = memoryview(bytearray([0xFF]*_BLOCK))

        self.type     = None

        for _ in range(16):
            self.spi.write(_FF)

        # init card ~ 5 attempts
        for _ in range(5):
            if self.cmd(_CMD0, 0, 0x95) == _IDLE_STATE:
                break
        else:
            raise OSError("No Card")

        r = self.cmd(_CMD8, 0x01AA << 8, 0x87, 4)

        if r == _IDLE_STATE:
            self.init_card_v2()
        elif r == (_IDLE_STATE | _ILLEGAL_CMD):
            self.init_card_v1()
        else:
            raise OSError("Unknown Version")

        if self.cmd(_CMD9, release=False):
            raise OSError("No Response")

        csd = bytearray(16)
        self.readinto(csd)

        if csd[0] & 0xC0 == 0x40:       # CSD version 2.0
            self.sectors = ((csd[8] << 8 | csd[9]) + 1) * 1024
        elif csd[0] & 0xC0 == 0x00:     # CSD version 1.0 (old, <=2GB)
            c_size       = csd[6] & 0x3 | csd[7] << 2 | (csd[8] & 0xC0) << 4
            c_size_mult  = (csd[9] & 0x3) << 1 | csd[10] >> 7
            self.sectors = (c_size + 1) * (2 ** (c_size_mult + 2))
        else:
            raise OSError("CSD Format Unsupported")

        csd = None

        if self.cmd(_CMD16, _BLOCK << 8):
            raise OSError("Can't Set Block Size")

        self.spi.init(baudrate=baudrate, phase=0, polarity=0)

    def init_card_v1(self) -> None:
        for _ in range(_CMD_TIMEOUT):
            self.cmd(_CMD55)
            if not self.cmd(_CMD41):
                self.cdv  = _BLOCK
                self.type = '[SDCard v1]'
                return
        raise OSError("Timeout")

    def init_card_v2(self) -> None:
        for i in range(_CMD_TIMEOUT):
            sleep_ms(50)
            self.cmd(_CMD58, final=4)
            self.cmd(_CMD55)
            if not self.cmd(_CMD41, 0x40 << 32):
                self.cmd(_CMD58, final=4)
                self.cdv = 1
                self.type = '[SDCard v2]'
                return
        raise OSError("Timeout")

    def cmd(self, cmd:int, arg:int=0, crc:int=0, final:int=0, release:bool=True, skip1:bool=False) -> int:
        self.cs(0)

        self.spi.write((cmd << 40 | arg | crc).to_bytes(6, 'big'))

        if skip1:
            self.spi.readinto(self.tokenbuf, 0xFF)

        # wait for the response (response[7] == 0)
        for i in range(_CMD_TIMEOUT):
            self.spi.readinto(self.tokenbuf, 0xFF)
            if not (self.tokenbuf[0] & 0x80):
                # this could be a big-endian integer that we are getting here
                for j in range(final):
                    self.spi.write(_FF)
                if release:
                    self.cs(1)
                    self.spi.write(_FF)
                return self.tokenbuf[0]

        # timeout
        self.cs(1)
        self.spi.write(_FF)
        return -1

    def readinto(self, buf:bytearray) -> None:
        self.cs(0)

        # read until start byte (0xff)
        for _ in range(_CMD_TIMEOUT):
            self.spi.readinto(self.tokenbuf, 0xFF)
            if self.tokenbuf[0] == _TOKEN_DATA:
                break
            sleep_ms(1)
        else:
            self.cs(1)
            raise OSError("Response Timeout")

        # read data
        self.spi.write_readinto(self.buf_mv[: len(buf)], buf)

        # read checksum
        self.spi.write(_FF)
        self.spi.write(_FF)

        self.cs(1)
        self.spi.write(_FF)

    def write(self, token:int, buf:bytearray) -> None:
        self.cs(0)

        # send: start of block, data, checksum
        self.spi.read(1, token)
        self.spi.write(buf)
        self.spi.write(_FF)
        self.spi.write(_FF)

        # check the response
        if (self.spi.read(1, 0xFF)[0] & 0x1F) != 0x05:
            self.cs(1)
            self.spi.write(_FF)
            return

        # wait for write to finish
        while not self.spi.read(1, 0xFF)[0]:
            pass

        self.cs(1)
        self.spi.write(_FF)

    def write_token(self, token:int) -> None:
        self.cs(0)

        self.spi.read(1, token)
        self.spi.write(_FF)

        # wait for write to finish
        while not self.spi.read(1, 0xFF)[0]:
            pass

        self.cs(1)
        self.spi.write(_FF)

    def readblocks(self, block_num:int, buf:bytearray) -> None:
        nblocks, err = divmod(len(buf), _BLOCK)
        assert nblocks and not err, "Invalid Buffer Length"
        if nblocks == 1:
            if self.cmd(_CMD17, int(block_num * self.cdv) << 8, release=False):
                self.cs(1)
                raise OSError(5)  # EIO

            self.readinto(buf)
        else:
            if self.cmd(_CMD18, int(block_num * self.cdv) << 8, release=False):
                self.cs(1)
                raise OSError(5)  # EIO

            mv = memoryview(buf)
            for i in range(nblocks):
                self.readinto(mv[_BLOCK+int(_BLOCK*(i-1)) : _BLOCK+int(_BLOCK*i)])

            if self.cmd(_CMD12, 0, 0xFF, skip1=True):
                raise OSError(5)  # EIO

    def writeblocks(self, block_num:int, buf:bytearray) -> None:
        nblocks, err = divmod(len(buf), _BLOCK)
        assert nblocks and not err, "Invalid Buffer Length"
        if nblocks == 1:
            if self.cmd(_CMD24, int(block_num * self.cdv) << 8):
                raise OSError(5)  # EIO

            self.write(_TOKEN_DATA, buf)
        else:
            if self.cmd(_CMD25, int(block_num * self.cdv) << 8):
                raise OSError(5)  # EIO

            mv = memoryview(buf)
            for i in range(nblocks):
                self.write(_TOKEN_CMD25, mv[_BLOCK+int(_BLOCK*(i-1)) : _BLOCK+int(_BLOCK*i)])

            self.write_token(_TOKEN_STOP_TRAN)

    def ioctl(self, cmd:int, arg:int=0) -> int:
        if cmd in (_IOCTL_INIT, _IOCTL_DEINIT, _IOCTL_SYNC):
            return 0
        elif cmd == _IOCTL_BLK_COUNT:
            return self.sectors
        elif cmd == _IOCTL_BLK_SIZE:
            return _BLOCK
        else:
            return -1
# The MIT License (MIT)
#
# Copyright (c) 2015 Christopher Arndt
# Copyright (c) 2019 Peter Hich
# Copyright (c) 2022 Robert Hammelrath
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# flashbdev.py
#
# A combination of spiflash.py by Christopher Arndt, the
# esp8266 flashbdev.py driver and the EEPROM library of Peter Hinch
#
# https://github.com/SpotlightKid/micropython-stm-lib/tree/master/spiflash
# https://github.com/peterhinch/micropython_eeprom.git
#

# 3 and 4 byte address commands
_READ_INDEX = const(0)
_PROGRAM_PAGE_INDEX = const(1)
_SECTOR_ERASE_INDEX = const(2)
_CMDS3BA = b'\x03\x02\x20'
_CMDS4BA = b'\x13\x12\x21'

CMD_JEDEC_ID = const(0x9F)
CMD_READ_STATUS = const(0x05)    # Read status register
CMD_WRITE_ENABLE = const(0x06)   # Write enable
# The commands below are placed into the _CMDS3BA and _CMDS4BA arrays.
# CMD_READ = const(0x03)           # Read @ low speed
# CMD_PROGRAM_PAGE = const(0x02)   # Write page
# CMD_ERASE_4K = const(0x20)
CMD_READ_UID = const(0x4B)
PAGE_SIZE = const(256)
SECTOR_SIZE = const(4096)

class SPIFlash:
    def __init__(self, spi, cs, addr4b=False):
        self._spi = spi
        self._cs = cs
        self._cs.high()
        self._buf = bytearray(1)
        self._addr4b = addr4b
        if addr4b:
            self._cmds = _CMDS4BA
            self._addrbuf = bytearray(5)
        else:
            self._cmds = _CMDS3BA
            self._addrbuf = bytearray(4)

        self.wait()
        id = self.getid()
        if id[2] == 1:
            self._size = 512 * 1024
        else:
            self._size = 1 << id[2]

    def getsize(self):
        return self._size

    def _write(self, val):
        if isinstance(val, int):
            self._buf[0] = val
            self._spi.write(self._buf)
        else:
            self._spi.write(val)

    def _addr_write(self, cmd, addr):
        self._addrbuf[0] = cmd
        if self._addr4b:
            self._addrbuf[-4] = addr >> 24
        self._addrbuf[-3] = addr >> 16
        self._addrbuf[-2] = addr >> 8
        self._addrbuf[-1] = addr
        self._cs.low()
        self._spi.write(self._addrbuf)

    def getid(self):
        self._cs.low()
        self._write(CMD_JEDEC_ID)  # id
        res = self._spi.read(3)
        self._cs.high()
        return res

    def wait(self):
        while True:
            self._cs.low()
            self._write(CMD_READ_STATUS)
            r = self._spi.read(1)[0]
            self._cs.high()
            if r == 0:
                return

    def read_block(self, addr, buf):
        self._addr_write(self._cmds[_READ_INDEX], addr)
        self._spi.readinto(buf)
        self._cs.high()

    def write_block(self, addr, buf):
        # Write in 256-byte chunks
        length = len(buf)
        pos = 0
        mv = memoryview(buf)
        while pos < length:
            size = min(length - pos, PAGE_SIZE)
            self._cs.low()
            self._write(CMD_WRITE_ENABLE)
            self._cs.high()
            # _addr_write() sets _cs low
            self._addr_write(self._cmds[_PROGRAM_PAGE_INDEX], addr)
            self._write(mv[pos:pos + size])
            self._cs.high()
            self.wait()

            addr += size
            pos += size

    def erase(self, addr):
        self._cs.low()
        self._write(CMD_WRITE_ENABLE)
        self._cs.high()
        # _addr_write() sets _cs low
        self._addr_write(self._cmds[_SECTOR_ERASE_INDEX], addr)
        self._cs.high()
        self.wait()

class FlashBdev(SPIFlash):

    def __init__(self, spi, cs, addr4b=False):
        super().__init__(spi, cs, addr4b)

    def readblocks(self, n, buf, offset=0):
        self.read_block(n * SECTOR_SIZE + offset, buf)

    def writeblocks(self, n, buf, offset=None):
        if offset is None:
            self.erase(n * SECTOR_SIZE)
            offset = 0
        self.write_block(n * SECTOR_SIZE + offset, buf)

    def ioctl(self, op, arg):
        if op == 4:  # MP_BLOCKDEV_IOCTL_BLOCK_COUNT
            return self.getsize() // SECTOR_SIZE
        if op == 5:  # MP_BLOCKDEV_IOCTL_BLOCK_SIZE
            return SECTOR_SIZE
        if op == 6:  # MP_BLOCKDEV_IOCTL_BLOCK_ERASE
            self.erase(arg * SECTOR_SIZE)
            return 0
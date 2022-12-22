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
_CMDS3BA = b'\x03\x02\x20'  # CMD_READ CMD_PROGRAM_PAGE CMD_ERASE_4K
_CMDS4BA = b'\x13\x12\x21'  # CMD_READ CMD_PROGRAM_PAGE CMD_ERASE_4K

CMD_JEDEC_ID = const(0x9F)
CMD_READ_STATUS = const(0x05)    # Read status register
CMD_WRITE_ENABLE = const(0x06)   # Write enable
CMD_READ_UID = const(0x4B)
CMD_READ_SFDP = const(0x5A)
PAGE_SIZE = const(256)
SECTOR_SIZE = const(4096)

class SPIflash:
    def __init__(self, spi, cs, addr4b=False, size=None, pagesize=PAGE_SIZE, sectorsize=SECTOR_SIZE):
        self._spi = spi
        self._cs = cs
        self._cs(1)
        self._buf = bytearray(1)
        self.pagesize = pagesize
        self._addr4b = 0
        self._cmds = _CMDS3BA
        self._addrbuf = bytearray(4)

        self.wait()
        if size is None:
            id = self.getid()
            if id[2] == 1:
                self._size = 512 * 1024
            else:
                self._size = 1 << id[2]
        else:
            self._size = size

        header = self.get_sfdp(0, 16)
        len = header[11] * 4;
        if len >= 29:
            addr = header[12] + (header[13] << 8) + (header[14] << 16)
            table = self.get_sfdp(addr, len)
            self._addr4b = ((table[2] >> 1) & 0x03) != 0
            self.sectorsize = 1 << table[28]
        else:
            self._addr4b = addr4b
            self.sectorsize = sectorsize

        if self._addr4b:
            self._cmds = _CMDS4BA
            self._addrbuf = bytearray(5)

    def flash_size(self):
        return self._size

    def flash_sectorsize(self):
        return self.sectorsize

    def _write_cmd(self, val):
        self._buf[0] = val
        self._spi.write(self._buf)

    def _write_addr(self, cmd, addr):
        self._addrbuf[0] = cmd
        if self._addr4b:
            self._addrbuf[-4] = addr >> 24
        self._addrbuf[-3] = addr >> 16
        self._addrbuf[-2] = addr >> 8
        self._addrbuf[-1] = addr
        self._cs(0)
        self._spi.write(self._addrbuf)

    def getid(self):
        self._cs(0)
        self._write_cmd(CMD_JEDEC_ID)  # id
        res = self._spi.read(3)
        self._cs(1)
        return res

    def get_sfdp(self, addr, len):
        self._write_addr(CMD_READ_SFDP, addr)
        self._spi.write(bytearray(1))
        res = self._spi.read(len)
        self._cs(1)
        return res

    def wait(self):
        self._buf[0] = 1
        while self._buf[0]:
            self._cs(0)
            self._write_cmd(CMD_READ_STATUS)
            self._spi.readinto(self._buf)
            self._cs(1)

    def flash_read(self, addr, buf):
        self._write_addr(self._cmds[_READ_INDEX], addr)
        self._spi.readinto(buf)
        self._cs(1)

    def flash_write(self, addr, buf):
        # Write in 256-byte chunks
        length = len(buf)
        pos = 0
        mv = memoryview(buf)
        while pos < length:
            size = min(length - pos, self.pagesize - pos % self.pagesize)
            self._cs(0)
            self._write_cmd(CMD_WRITE_ENABLE)
            self._cs(1)
            # _write_addr() sets _cs low
            self._write_addr(self._cmds[_PROGRAM_PAGE_INDEX], addr)
            self._spi.write(mv[pos:pos + size])
            self._cs(1)
            self.wait()

            addr += size
            pos += size

    def flash_erase(self, addr):
        self._cs(0)
        self._write_cmd(CMD_WRITE_ENABLE)
        self._cs(1)
        # _write_addr() sets _cs low
        self._write_addr(self._cmds[_SECTOR_ERASE_INDEX], addr)
        self._cs(1)
        self.wait()
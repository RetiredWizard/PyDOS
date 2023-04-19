import os, sys

sys.path.append('/flash/lib')

from flashbdev import FlashBdev
from spiflash import SPIflash
from machine import SPI, Pin

spi=SPI(0, sck=21, mosi=20,miso=24,baudrate=24_000_000)
cs = Pin(25, Pin.OUT, value=1)
flash=FlashBdev(SPIflash(spi, cs))
if 'format_secondary_flash.___' in os.listdir('/flash'):
    os.VfsLfs2.mkfs(flash, progsize=256)
    os.remove('/flash/format_secondary_flash.___')
try:
    vfs = os.VfsLfs2(flash, progsize=256)
except OSError as e:
    os.VfsLfs2.mkfs(flash, progsize=256)
    vfs = os.VfsLfs2(flash, progsize=256)

os.mount(vfs, "/")
os.chdir('/')

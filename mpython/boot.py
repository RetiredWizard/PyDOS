from sys import implementation

spcBoards = ['Teensy 4.1 with MIMXRT1062DVJ6A', \
    'Sparkfun SAMD51 Thing Plus with SAMD51J20A', 
    'XIAO nRF52840 Sense with NRF52840']

if implementation._machine in spcBoards:
    boardNo = spcBoards.index(implementation._machine)
else:
    import os
    os.remove('/boot.py')
    boardNo = -1

if boardNo == 0:
    import uos, sys
    uos.umount("/flash")
    uos.mount(vfs,"/")
    uos.chdir("/")
    sys.path.pop(-1)
    sys.path.pop(-1)
    sys.path.append("/")
    sys.path.append("/lib")
elif boardNo == 1 or boardNo == 2:
    import sys
    sys.path.append("/lib")
    sys.path.append("/mpython/extFlash/lib")
    sys.path.append("/flash/mpython/extFlash/lib")
    if boardNo == 1:
        import ThngPls_SAMD51
    else:
        import XIAO_nRF52840
    sys.path.pop(-1)
    sys.path.pop(-1)

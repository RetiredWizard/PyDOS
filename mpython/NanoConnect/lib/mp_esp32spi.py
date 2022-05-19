from spidevice import SPIDevice
from machine import Pin
import time

_SET_PIN_MODE_CMD = const(0x50)
_SET_DIGITAL_WRITE_CMD = const(0x51)
_SET_ANALOG_WRITE_CMD = const(0x52)
_SET_DIGITAL_READ_CMD = const(0x53)
_SET_ANALOG_READ_CMD = const(0x54)

_START_CMD = const(0xE0)
_END_CMD = const(0xEE)
_ERR_CMD = const(0xEF)
_REPLY_FLAG = const(1 << 7)
_CMD_FLAG = const(0)

class ESP_SPIcontrol:

    def __init__(self, spi, cs_dio, ready_dio, reset_dio, gpio0_dio=None, *, debug=False):
        self._debug = debug
        self.set_psk = False
        self.set_crt = False
        self._buffer = bytearray(10)
        self._pbuf = bytearray(1)  # buffer for param read
        self._sendbuf = bytearray(256)  # buffer for command sending
        self._socknum_ll = [[0]]  # pre-made list of list of socket #

        self._spi_device = SPIDevice(spi, cs_dio, baudrate=8000000)
        self._cs = cs_dio
        self._ready = ready_dio
        self._reset = reset_dio
        self._gpio0 = gpio0_dio
        #self._cs.direction = Pin.OUT
        #self._ready.direction = Pin.IN
        #self._reset.direction = Pin.OUT
        # Only one TLS socket at a time is supported so track when we already have one.
        self._tls_socket = None
        #if self._gpio0:
            #self._gpio0.direction = Pin.IN
        self.reset()

    def _send_command(self, cmd, params=None, *, param_len_16=False):
        """Send over a command with a list of parameters"""
        if not params:
            params = ()

        packet_len = 4  # header + end byte
        for i, param in enumerate(params):
            packet_len += len(param)  # parameter
            packet_len += 1  # size byte
            if param_len_16:
                packet_len += 1  # 2 of em here!
        while packet_len % 4 != 0:
            packet_len += 1
        # we may need more space
        if packet_len > len(self._sendbuf):
            self._sendbuf = bytearray(packet_len)

        self._sendbuf[0] = _START_CMD
        self._sendbuf[1] = cmd & ~_REPLY_FLAG
        self._sendbuf[2] = len(params)

        # handle parameters here
        ptr = 3
        for i, param in enumerate(params):
            if self._debug >= 2:
                print("\tSending param #%d is %d bytes long" % (i, len(param)))
            if param_len_16:
                self._sendbuf[ptr] = (len(param) >> 8) & 0xFF
                ptr += 1
            self._sendbuf[ptr] = len(param) & 0xFF
            ptr += 1
            for j, par in enumerate(param):
                self._sendbuf[ptr + j] = par
            ptr += len(param)
        self._sendbuf[ptr] = _END_CMD

        self._wait_for_ready()
        with self._spi_device as spi:
            times = time.ticks_ms()
            while (time.ticks_ms() - times) < 1000:  # wait up to 1000ms
                if self._ready.value():  # ok ready to send!
                    break
            else:
                raise RuntimeError("ESP32 timed out on SPI select")
            spi.write(self._sendbuf)
            # , start=0, end=packet_len)  # pylint: disable=no-member
            if self._debug >= 3:
                print("Wrote: ", [hex(b) for b in self._sendbuf[0:packet_len]])

    def _send_command_get_response(
        self,
        cmd,
        params=None,
        *,
        reply_params=1,
        sent_param_len_16=False,
        recv_param_len_16=False
    ):
        """Send a high level SPI command, wait and return the response"""
        self._send_command(cmd, params, param_len_16=sent_param_len_16)
        return self._wait_response_cmd(cmd, reply_params, param_len_16=recv_param_len_16)

    def _wait_response_cmd(self, cmd, num_responses=None, *, param_len_16=False):
        """Wait for ready, then parse the response"""
        self._wait_for_ready()

        responses = []
        with self._spi_device as spi:
            times = time.ticks_ms()
            while (time.ticks_ms() - times) < 1000:  # wait up to 1000ms
                if self._ready.value():  # ok ready to send!
                    break
            else:
                raise RuntimeError("ESP32 timed out on SPI select")

            self._wait_spi_char(spi, _START_CMD)
            self._check_data(spi, cmd | _REPLY_FLAG)
            if num_responses is not None:
                self._check_data(spi, num_responses)
            else:
                num_responses = self._read_byte(spi)
            for num in range(num_responses):
                param_len = self._read_byte(spi)
                if param_len_16:
                    param_len <<= 8
                    param_len |= self._read_byte(spi)
                if self._debug >= 2:
                    print("\tParameter #%d length is %d" % (num, param_len))
                response = bytearray(param_len)
                self._read_bytes(spi, response)
                responses.append(response)
            self._check_data(spi, _END_CMD)

        if self._debug >= 2:
            print("Read %d: " % len(responses[0]), responses)
        return responses

    def _wait_spi_char(self, spi, desired):
        """Read a byte with a retry loop, and if we get it, check that its what we expect"""
        for _ in range(10):
            r = self._read_byte(spi)
            if r == _ERR_CMD:
                raise RuntimeError("Error response to command")
            if r == desired:
                return True
            time.sleep(0.01)
        raise RuntimeError("Timed out waiting for SPI char")

    def _read_byte(self, spi):
        """Read one byte from SPI"""
        spi.readinto(self._pbuf)
        if self._debug >= 3:
            print("\t\tRead:", hex(self._pbuf[0]))
        return self._pbuf[0]

    def _read_bytes(self, spi, buffer, start=0, end=None):
        """Read many bytes from SPI"""
        if not end:
            end = len(buffer)
        #spi.readinto(buffer, start=start, end=end)
        spi.readinto(buffer)
        if self._debug >= 3:
            print("\t\tRead:", [hex(i) for i in buffer])

    def _check_data(self, spi, desired):
        """Read a byte and verify its the value we want"""
        r = self._read_byte(spi)
        if r != desired:
            raise RuntimeError("Expected %02X but got %02X" % (desired, r))

    def set_pin_mode(self, pin, mode):
        """Set the io mode for a GPIO pin.
        :param int pin: ESP32 GPIO pin to set.
        :param value: direction for pin, digitalio.Direction or integer (0=input, 1=output).
        """
        #if mode == Direction.OUTPUT:
            #pin_mode = 1
        #elif mode == Direction.INPUT:
            #pin_mode = 0
        #else:
            #pin_mode = mode
        pin_mode = mode
        resp = self._send_command_get_response(_SET_PIN_MODE_CMD, ((pin,), (pin_mode,)))
        if resp[0][0] != 1:
            raise RuntimeError("Failed to set pin mode")

    def set_analog_write(self, pin, analog_value):
        """Set the analog output value of pin, using PWM.
        :param int pin: ESP32 GPIO pin to write to.
        :param float value: 0=off 1.0=full on
        """
        value = int(255 * analog_value)
        resp = self._send_command_get_response(
            _SET_ANALOG_WRITE_CMD, ((pin,), (value,))
        )
        if resp[0][0] != 1:
            raise RuntimeError("Failed to write to pin")

    def reset(self):
        """Hard reset the ESP32 using the reset pin"""
        if self._debug:
            print("Reset ESP32")
        if self._gpio0:
            self._gpio0.direction = Direction.OUTPUT
            self._gpio0.value(True)  # not bootload mode
        self._cs.value(True)
        self._reset.value(False)
        time.sleep(0.01)  # reset
        self._reset.value(True)
        time.sleep(0.75)  # wait for it to boot up
        #if self._gpio0:
            #self._gpio0.direction = Direction.INPUT


    def _wait_for_ready(self):
        """Wait until the ready pin goes low"""
        if self._debug >= 3:
            print("Wait for ESP32 ready", end="")
        times = time.ticks_ms()
        while (time.ticks_ms() - times) < 10000:  # wait up to 10 seconds
            if not self._ready.value():  # we're ready!
                break
            if self._debug >= 3:
                print(".", end="")
                time.sleep(0.05)
        #else:
            #raise RuntimeError("ESP32 not responding")
        if self._debug >= 3:
            print()

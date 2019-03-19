from ov2640_constants import *
from ov2640_lores_constants import *
from ov2640_hires_constants import *
import machine
import time
import ubinascii
import uos
import gc

class ov2640(object):
    def __init__(self, sclpin=22, sdapin=21, cspin=15, sckpin=14, mosipin=13, misopin=12, resolution=OV2640_320x240_JPEG, IMAGEDECODE=OV2640_YUV422):

        gc.enable()

        #I2C pins
        self.sclpin=sclpin
        self.sdapin=sdapin
        self.cspin=cspin

        #SPI pins
        self.sckpin=sckpin
        self.mosipin=mosipin
        self.misopin=misopin

        self.standby=False #variable para control de estado de camara

        #iniciacion de buses para la comunicacion    
        self.hspi = machine.SPI(1, baudrate=80000000, polarity=0, phase=0, sck=machine.Pin(self.sckpin), mosi=machine.Pin(self.mosipin), miso=machine.Pin(self.misopin))
        self.i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=1000000)
        self.hspi.init(baudrate=2000000)

        #cs pin para la comunicacion spi, tener en cuenta que este puede ser cualquier gpio
        self.cspin = machine.Pin(self.cspin, machine.Pin.OUT)
        self.cspin.value(1)

        #deteccion de la camara
        addrs = self.i2c.scan()
        print('ov2640_init: devices detected on on i2c:')
        for a in addrs:
            print('0x%x' % a)
            time.sleep(1)


        self.i2c.writeto_mem(SENSORADDR, 0xff, b'\x01')
        # initiate system reset
        self.i2c.writeto_mem(SENSORADDR, 0x12, b'\x80')

        # let it come up
        time.sleep_ms(100)

        # jpg init registers
        cam_write_register_set(self.i2c, SENSORADDR, OV2640_JPEG_INIT)
        cam_write_register_set(self.i2c, SENSORADDR, IMAGEDECODE)
        cam_write_register_set(self.i2c, SENSORADDR, OV2640_JPEG)

        self.i2c.writeto_mem(SENSORADDR, 0xff, b'\x01')
        self.i2c.writeto_mem(SENSORADDR, 0x15, b'\x00')
		   
        cam_write_register_set(self.i2c, SENSORADDR, OV2640_1600x1200_JPEG)

        cam_spi_write(b'\x00', b'\x55', self.hspi, self.cspin)
        res = cam_spi_read(b'\x00', self.hspi, self.cspin)
        print(res)
        print("ov2640 init:  register test return bytes %s" % ubinascii.hexlify(res))
        if (res == b'\x55'):
            print("ov2640_init: register test successful")
        else:
            print("ov2640_init: register test failed!")
        time.sleep_us(10)

        self.i2c.writeto_mem(SENSORADDR, 0xff, b'\x01')
        # check the camera type
        time.sleep_us(50)
        parta = self.i2c.readfrom_mem(SENSORADDR, 0x0a, 1)
        time.sleep_us(50)
        partb = self.i2c.readfrom_mem(SENSORADDR, 0x0b, 1)
        if ((parta != b'\x26') or (partb != b'\x42')):
            print("ov2640_init: device type does not appear to be ov2640, bytes: %s/%s" % \
                    (ubinascii.hexlify(parta), ubinascii.hexlify(partb)))
        else:
            print("ov2640_init: device type looks correct, bytes: %s/%s" % \
                    (ubinascii.hexlify(parta), ubinascii.hexlify(partb)))
        time.sleep_us(50)


    def capture_to_file(self, fn, overwrite):
        # bit 0 - clear FIFO write done flag
        cam_spi_write(b'\x04', b'\x01', self.hspi, self.cspin)

        # bit 1 - start capture then read status
        cam_spi_write(b'\x04', b'\x02', self.hspi, self.cspin)
        time.sleep_ms(10)

        # read status
        res = cam_spi_read(b'\x41', self.hspi, self.cspin)
        cnt = 0
        #if (res == b'\x00'):
        #    print("initiate capture may have failed, return byte: %s" % ubinascii.hexlify(res))

        # read the image from the camera fifo
        while True:
            res = cam_spi_read(b'\x41', self.hspi, self.cspin)
            mask = b'\x08'
            if (res[0] & mask[0]):
                break
            #print("continuing, res register %s" % ubinascii.hexlify(res))
            time.sleep_ms(10)
            cnt += 1
        #print("slept in loop %d times" % cnt)

        # read the fifo size
        b1 = cam_spi_read(b'\x44', self.hspi, self.cspin)
        b2 = cam_spi_read(b'\x43', self.hspi, self.cspin)
        b3 = cam_spi_read(b'\x42', self.hspi, self.cspin)
        val = b1[0] << 16 | b2[0] << 8 | b3[0] 
        print("ov2640_capture: %d bytes in fifo" % val)
        gc.collect()

        bytebuf = [ 0, 0 ]
        picbuf = [ b'\x00' ] * PICBUFSIZE
        l = 0
        bp = 0
        if (overwrite == True):
            #print("deleting old file %s" % fn)
            try:
                uos.remove(fn)
            except OSError:
                pass
        while ((bytebuf[0] != b'\xd9') or (bytebuf[1] != b'\xff')):
            bytebuf[1] = bytebuf[0]
            if (bp > (len(picbuf) - 1)):
                #print("appending buffer to %s" % fn)
                appendbuf(fn, picbuf, bp)
                bp = 0

            bytebuf[0] = cam_spi_read(b'\x3d', self.hspi, self.cspin)
            l += 1
            #print("read so far: %d, next byte: %s" % (l, ubinascii.hexlify(bytebuf[0])))
            picbuf[bp] = bytebuf[0]
            bp += 1
        if (bp > 0):
            #print("appending final buffer to %s" % fn)
            appendbuf(fn, picbuf, bp)
        print("read %d bytes from fifo, camera said %d were available" % (l, val))
        return (l)

    def standby(self):
        # register set select
        self.i2c.writeto_mem(SENSORADDR, 0xff, b'\x01')
        # standby mode
        self.i2c.writeto_mem(SENSORADDR, 0x09, b'\x10')
        self.standby = True

    def wake(self):
        # register set select
        self.i2c.writeto_mem(SENSORADDR, 0xff, b'\x01')
        # standby mode
        self.i2c.writeto_mem(SENSORADDR, 0x09, b'\x00')
        self.standby = False

def cam_write_register_set(i, addr, set):
    for el in set:
        raddr = el[0]
        val = el[1]
        if (raddr == 0xff and val == b'\xff'):
            return
        i.writeto_mem(SENSORADDR, raddr, val)

def cam_spi_write(address, value, hspi, cspin):
    cspin.value(0)
    modebit = b'\x80'
    d = bytes([address[0] | modebit[0], value[0]])
    hspi.write(d)
    cspin.value(1)

def appendbuf(fn, picbuf, howmany):
    try:
        f = open(fn, 'ab')
        c = 1
        for by in picbuf:
            if (c > howmany):
                break
            c += 1
            f.write(bytes([by[0]]))
        f.close()
    except OSError:
        print("error writing file")
    print("write %d bytes from buffer" % howmany)

def cam_spi_read(address, hspi, cspin):
    cspin.value(0)
    maskbits = b'\x7f'
    wbuf = bytes([address[0] & maskbits[0]])
    hspi.write(wbuf)
    buf = hspi.read(1)
    cspin.value(1)
    return (buf)
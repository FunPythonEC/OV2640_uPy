#brillo 2
time.sleep_us(50)
i2c.writeto_mem(0x60, 0xff, b'x00')
i2c.writeto_mem(0x60, 0x7c, b'x00')
i2c.writeto_mem(0x60, 0x7d, b'x04')
i2c.writeto_mem(0x60, 0x7c, b'x09')
i2c.writeto_mem(0x60, 0x7d, b'x40')
i2c.writeto_mem(0x60, 0x7d, b'x00')
time.sleep_us(50)

#negativo
i2c.writeto_mem(0x60, 0xff, b'x00')
i2c.writeto_mem(0x60, 0x7c, b'x00')
i2c.writeto_mem(0x60, 0x7d, b'x58')
i2c.writeto_mem(0x60, 0x7c, b'x05')
i2c.writeto_mem(0x60, 0x7d, b'x80')
i2c.writeto_mem(0x60, 0x7d, b'x80')
time.sleep_us(50)

#normal
i2c.writeto_mem(0xff, 0x00);
i2c.writeto_mem(0x7c 0x00);
i2c.writeto_mem(0x7d, 0x00);
i2c.writeto_mem(0x7c 0x05);
i2c.writeto_mem(0x7d, 0x80);
i2c.writeto_mem(0x7d, 0x80;

#brillo 0
write_SCCB(0xff, 0x00);
write_SCCB(0x7c, 0x00);
write_SCCB(0x7d, 0x04);
write_SCCB(0x7c, 0x09);
write_SCCB(0x7d, 0x20);
write_SCCB(0x7d, 0x00);



i2c.writeto_mem(SENSORADDR, 0xff, b'x00')
i2c.writeto_mem(SENSORADDR, 0x7c, b'x00')
i2c.writeto_mem(SENSORADDR, 0x7d, b'x04')
i2c.writeto_mem(SENSORADDR, 0x7c, b'x09')
i2c.writeto_mem(SENSORADDR, 0x7d, b'x20')
i2c.writeto_mem(SENSORADDR, 0x7d, b'x00')
time.sleep_us(50)
i2c.writeto_mem(SENSORADDR, 0xff, b'\x00')
i2c.writeto_mem(SENSORADDR, 0x7c, b'\x00')
i2c.writeto_mem(SENSORADDR, 0x7d, b'\x00')
i2c.writeto_mem(SENSORADDR, 0x7c, b'\x05')
i2c.writeto_mem(SENSORADDR, 0x7d, b'\x80')
i2c.writeto_mem(SENSORADDR, 0x7d, b'\x80')

i2c.writeto_mem(SENSORADDR, 0xff, b'\x00')
i2c.writeto_mem(SENSORADDR, 0x7c, b'\x00')
i2c.writeto_mem(SENSORADDR, 0x7d, b'\x18')
i2c.writeto_mem(SENSORADDR, 0x7c, b'\x05')
i2c.writeto_mem(SENSORADDR, 0x7d, b'\x80')
i2c.writeto_mem(SENSORADDR, 0x7d, b'\x80')
time.sleep_us(50)

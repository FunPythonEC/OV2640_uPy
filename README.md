# OV2640_uPy
Libreria para camara OV2640 con MicroPython, especificamente para el ESP32 el cual tiene una mayor capacidad de procesamiento.
Ha sido creada a partir de la de namato encontrada en el siguiente link: https://github.com/namato/micropython-ov2640

## Conexiones para la comunicación
Para la comunicacion en la librería ya se ha escecificado que pines se usan, los cuales agrego a continucacion, sin embargo puede ser cambiado en el constructor:
~~~~ cam = ov2640(sclpin=22, sdapin=21, cspin=15, sckpin=14, mosipin=13, misopin=12 resolution=OV2640_320x240_JPEG, IMAGEDECODE=OV2640_YUV422) ~~~~

### I²C
SCL -> GPIO22
SDA -> GPIO21

### SPI
CS -> GPIO15
SCK -> GPIO14
MOSI -> GPIO13
MISO -> GPIO12


## Proximas actualizaciones
Proximamente se agregaran ciertas configuraciones posibles para la camara y ademas el ejemplo de un web server para video streaming

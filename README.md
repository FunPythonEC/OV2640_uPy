# OV2640_uPy - MicroPython class to use OV2640
Libreria para camara OV2640 con MicroPython, especificamente para el ESP32 el cual tiene una mayor capacidad de procesamiento.
Ha sido creada a partir de la de namato encontrada en el siguiente link: https://github.com/namato/micropython-ov2640

## Conexiones para la comunicación
Para la comunicacion en la librería ya se ha escecificado que pines se usan, los cuales agrego a continucacion, sin embargo puede ser cambiado en el constructor:
~~~~ python
import ov2640
from ov2640_config import *
from ov2640_constants import *
from ov2640_hires_constants import *
from ov2640_lores_constants import *
#todos los imports anteriores son para poder usar las constantes de encoding de las imagenes
cam = ov2640.ov2640(sclpin=22, sdapin=21, cspin=15, sckpin=14, mosipin=13, misopin=12 resolution=OV2640_320x240_JPEG, IMAGEDECODE=OV2640_YUV422)
nbytes = cam.capture_to_file("/image.jpg")
~~~~

### I²C

| Pin Camara (OV2640) | Pin ESP |
| ------------------- | ------- |
| SCL                 | GPIO22  |
| SDA                 | GPIO21  |

Tener en cuenta los siguiente:
	La comunicación I²C permite la configuración de la camara.

Además que los pines especificados en la tabla anterior es para una de las configuraciones de I²C que se pueden hacer, sin embargo, si se quieren usar otro pines, estos pueden ser especificados en el constructor.

### SPI

| Pin Camara (OV2640) | Pin ESP |
| ------------------- | ------- |
| CS               | GPIO15 |
| SCK              | GPIO14 |
| MOSI | GPIO13 |
| MISO | GPIO12 |
Tener presente que asi como para la comunicación anterior, SPI esta dedicado para la transmisión de la imagen al microcontrolador y que además se permiten otros pines para SPI que deben ser especificados en el constructor del objeto.


## Proximas actualizaciones
* Proximamente se agregaran ciertas configuraciones posibles para la camara y ademas el ejemplo de un web server para video streaming.
* Una programación más sencilla para los imports y su uso.
* Metodos para la configuración de la camara por I²C.
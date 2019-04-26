# OV2640_uPy - MicroPython class to use OV2640
Libreria para camara OV2640 con MicroPython, especificamente para el ESP32 el cual tiene una mayor capacidad de procesamiento.
Ha sido creada a partir de la de namato encontrada en el siguiente link: https://github.com/namato/micropython-ov2640

## Conexiones para la comunicación
La camara OV2640 con fifo permite comunicación I²C y SPI. Por lo que a continuación se muestran los pines predeterminados que son usados para ello. La comunicación I²C es dedicada para las configuraciones de la cámara, mientras que la SPI es para la transmisión de la imagen captada.

### I²C
Los pines especificados en la siguiente tabla son los usados por default en el constructor de la clase.
| Pin Camara (OV2640) | Pin ESP |
| ------------------- | ------- |
| SCL                 | GPIO22  |
| SDA                 | GPIO21  |

### SPI
Los pines especificados en la siguiente tabla son los usados por default en el constructor de la clase.
| Pin Camara (OV2640) | Pin ESP |
| ------------------- | ------- |
| CS   | GPIO15 |
| SCK  | GPIO14 |
| MOSI | GPIO13 |
| MISO | GPIO12 |

## Ejemplos de uso
### Pines predeterminados

~~~~ python
import ov2640
from ov2640_config import *
from ov2640_constants import *
from ov2640_hires_constants import *
from ov2640_lores_constants import *
cam = ov2640.ov2640()
nbytes = cam.capture_to_file("/image.jpg")
~~~~

### Pines especificos

~~~~ python
import ov2640
from ov2640_config import *
from ov2640_constants import *
from ov2640_hires_constants import *
from ov2640_lores_constants import *
#todos los imports anteriores son para poder usar las constantes de encoding de las imagenes y configuraciones
cam = ov2640.ov2640(sclpin=22, sdapin=21, cspin=15, sckpin=14, mosipin=13, misopin=12, resolution=ov2640_hires_constants.OV2640_320x240_JPEG, imagedecode=ov2640_constants.OV2640_YUV422)
nbytes = cam.capture_to_file("/image.jpg")
~~~~

## Proximas actualizaciones
* Proximamente se agregaran ciertas configuraciones posibles para la camara y ademas el ejemplo de un web server para video streaming.
* Una programación más sencilla para los imports y su uso.
* Metodos para la configuración de la camara por I²C.
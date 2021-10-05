#import LoRaDuplexCallback
#import LoRaPingPong
#import LoRaSender

import network
import LoRaReceiver
import config_lora
from sx127x import SX127x

from machine  import Pin, I2C
from ssd1306 import SSD1306_I2C

from controller_esp32 import ESP32Controller
print("QUESTA VOLTA L UPDATE LO METTO QUI!!!!")
print("QUI FACCIAMO ADESSO UN BEL CAMBIO")
#initialize OLED
i2c = I2C(-1, Pin(22), Pin(21))
oled = SSD1306_I2C(128, 32, i2c)
oled.fill(0)

oled.text(">>>COLLECTOR<<<", 0, 0)
oled.text("LORA INIT...", 0, 10)
oled.show()

#initialize controller and LoRa network
controller = ESP32Controller()
lora = controller.add_transceiver(SX127x(name = 'LoRa'),
                                  pin_id_ss = ESP32Controller.PIN_ID_FOR_LORA_SS,
                                  pin_id_RxDone = ESP32Controller.PIN_ID_FOR_LORA_DIO0)


#LoRaDuplexCallback.duplexCallback(lora)

#LoRaPingPong.ping_pong(lora)

#LoRaSender.send(lora)

LoRaReceiver.receive(lora)



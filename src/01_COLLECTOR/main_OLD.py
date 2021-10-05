import network
import LoRaReceiver
import config_lora
from sx127x import SX127x
from machine  import Pin, I2C
from ssd1306 import SSD1306_I2C
from controller_esp32 import ESP32Controller
import wifi_connect as wifi
import uos 
from time import sleep_ms

#initialize OLED
i2c = I2C(-1, Pin(22), Pin(21))
oled = SSD1306_I2C(128, 32, i2c)
oled.fill(0)

oled.text(">>>NEW MAIN!<<<", 0, 0)

oled.text("NETWORK INIT...", 0, 10)
wifi.wifi_connect()

oled.text("FTP INIT...", 0, 20)
import uftpd

uftpd.restart(verbose=1)

oled.show()
sleep_ms(15000)
oled.fill(0)
uftpd.stop()

oled.text("CODE UPDATE SLOT", 0 , 0)

if "main_NEW.py" in uos.listdir():
    uos.rename("main.py", "main_OLD.py")
    uos.rename("main_NEW.py", "main.py")
    oled.text("UPDATED CODE!", 0, 10)
else:
    oled.text("NO UPDATE", 0, 10) 

sleep_ms(2500)

oled.text("LORA INIT...", 0, 20)
oled.show()


#initialize controller and LoRa network
controller = ESP32Controller()
lora = controller.add_transceiver(SX127x(name = 'LoRa'),
                                  pin_id_ss = ESP32Controller.PIN_ID_FOR_LORA_SS,
                                  pin_id_RxDone = ESP32Controller.PIN_ID_FOR_LORA_DIO0)

LoRaReceiver.receive(lora)




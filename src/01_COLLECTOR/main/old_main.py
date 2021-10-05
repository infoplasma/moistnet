import config_lora
from sx127x import SX127x
from controller_esp32 import ESP32Controller
from time import sleep
from machine import Pin, ADC, I2C, PWM, deepsleep
from ssd1306 import SSD1306_I2C
from gfx import GFX


#initialize controller and LoRa network
controller = ESP32Controller()
lora = controller.add_transceiver(SX127x(name = 'LoRa'),
                                  pin_id_ss = ESP32Controller.PIN_ID_FOR_LORA_SS,
                                  pin_id_RxDone = ESP32Controller.PIN_ID_FOR_LORA_DIO0)

#initialize RGB LED pins
red = PWM(Pin(2))
green = PWM(Pin(4))
blue = PWM(Pin(15))
red.duty(0)
green.duty(0)
blue.duty(0)

#initialize I2C bus comms
i2c = I2C(-1, Pin(22), Pin(21))

#initialize OLED display
dsp = SSD1306_I2C(128, 64, i2c)

#initliaze graphics
graphics = GFX(128, 64, dsp.pixel)

# setup of analog pin, for moisture sensor reaadings
sens_32 = ADC(Pin(32))

# setup analog pin attenuation to 11DB, to allow readings
# of 3.1V maximum
sens_32.atten(ADC.ATTN_11DB)

# 100%DRY: 2.7V 4095
# 100%WET: 1.2V 0

def pulse(led=red, dty=0, slp=0.001):
    for j in range(dty):
        led.duty(j)
        sleep(slp)
    for k in range(dty):
        led.duty(dty-k)
        sleep(slp)

def classify_reading(value):
    very_wet = range(0,682)
    wet = range(683,1365)
    little_wet = range(1366,2048)
    little_dry = range(2049,2730)
    dry = range(2731,3412)
    very_dry = range(3413,4096)
    if value in very_wet:
        return '6'
    elif value in wet:
        return '5'
    elif value in little_wet:
        return '4'
    elif value in little_dry:
        return '3'
    elif value in dry:
        return '2'
    elif value in very_dry:
        return '1'
    else:
        return '0'

for _ in range(4):
    red.duty(0)
    blue.duty(0)
    green.duty(0)
    val = 0
    for i in range(10):
        reading = sens_32.read()
        val += reading        
        print("ACTUAL READING ==> {}".format(reading))
        pulse(red, 1000, slp=0.0009)
        sleep(0.001)
    avg_reading = val / 10
    cls_reading = classify_reading(avg_reading)
 
    payload = "{}".format(cls_reading)
    print("AVERAGE VALUE ==> {}, SIGNAL RSSI ==> {}, ACTUAL CLASSIFIED PAYLOAD ==> {}".format(avg_reading, lora.packetRssi(), cls_reading))
 
    dsp.fill(0)
    dsp.text("avg_val= {}".format(avg_reading), 0, 0)
    dsp.text("pckt_RSSI= {}".format(lora.packetRssi()), 0, 10)
    dsp.text("payload= {}".format(payload), 0, 20)
    dsp.show()
    #send payload
    lora.println(payload)
    for _ in range(5):
        pulse(led=green, dty=50, slp=0.02)    

red.duty(0)
green.duty(0)
blue.duty(0)
dsp.fill(0)
dsp.show()
deepsleep(10000)

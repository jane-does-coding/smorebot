from machine import Pin, PWM, SPI, ADC
import time
#import neopixel
from st7735 import TFT
from st7735 import sysfont
from machine import SPI,Pin
import math

# MICROWAVE SPINNER
pwm = PWM(Pin(26))
pwm.freq(20)
pwm.duty_u16(1800) #4000 is the minimum to overcome motor inductance

print("Enabled Rotator")


# HOT AIR GUN
relay = Pin(27, Pin.OUT)
relay.high() #ensure relay OFF initially

# SCREEN
spi = SPI(0, baudrate=20000000, polarity=0, phase=0,
              sck=Pin(2), mosi=Pin(3), miso=None)
tft=TFT(spi,0,7,1)
tft.initr()
tft.rgb(True)

font = sysfont.sysfont
v = 45
tft.rotation(1)
tft.fill(TFT.BLACK)
tft.text((32, 3), "SMOREBOT", TFT.YELLOW, font, 2, nowrap=True)


# TEMPERATURE
#therm = ADC(Pin(28))

adc = ADC(Pin(28))

for i in range(1, 14):   
    tft.fillrect((0, tft.size()[1]//2 - 26), (160, 50), TFT.WHITE)

    
    read = adc.read_u16()
    temp = math.log(10000.0 / (65335 / read - 1))
    temp = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * temp * temp))* temp);
    temp = temp - 263.15
    trunc_temp = f"{temp:.1f}"
    text_str = f"{trunc_temp} F"
    print(text_str)
    tft.text((2, v), text_str, TFT.BLUE, font, 5, nowrap=True)

    #tft.text((2, 100), "[            ]", TFT.YELLOW, font, 2, nowrap=True)
    
    
    load_str = "#############"
    new_str = load_str[0:i-1]
    tft.text((2, 100), f"[{new_str: ^12}]", TFT.YELLOW, font, 2, nowrap=True)
    time.sleep(4)

# turn off blower
relay.low()
tft.fillrect((0, tft.size()[1]//2 - 26), (160, 50), TFT.WHITE)
tft.text((2, v), "YIPPEE", TFT.BLUE, font, 5, nowrap=True)
pwm.duty_u16(0000)

buzzer = PWM(Pin(6))
buzzer.freq(500)
buzzer.duty_u16(1000) #beep
time.sleep(1)
buzzer.duty_u16(0)
time.sleep(1)
buzzer.duty_u16(1000) #beep
time.sleep(1)
buzzer.duty_u16(0)
time.sleep(1)
buzzer.duty_u16(1000) #beep
time.sleep(1)
buzzer.duty_u16(0)




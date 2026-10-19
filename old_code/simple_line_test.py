from machine import Pin
from time import sleep
from config import track_1, track_2, track_3, track_4
from path import *


while True:
    track_1_value = Pin(track_1, Pin.IN).value()
    track_2_value = Pin(track_2, Pin.IN).value()
    track_3_value = Pin(track_3, Pin.IN).value()
    track_4_value = Pin(track_4, Pin.IN).value()

    value_list = [track_1_value, track_2_value, track_3_value, track_4_value]
    line_following(value_list)
    line_correction(value_list)






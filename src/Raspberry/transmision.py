import sys
import sx126x
import threading
import time
import select
import busio, board
import adafruit_bmp280 as bmp280
import adafruit_ltr390 as ltr390


node = sx126x.sx126x(serial_num="/dev/ttyS0", freq=433, addr=0, power=22, rssi=False)

i2c = busio.I2C(board.SCL, board.SDA)
ltr = ltr390.LTR390(i2c)
bmp = bmp280.Adafruit_BMP280_I2C(i2c, 0x76)


def send_deal():
    get_rec = "0," + "AAA" + " " + str(bmp.temperature)[:5] + " " + str(bmp.pressure)[:7] + " " + str(ltr.uvs)[:4] + " " + str(ltr.light) + " "

    get_t = get_rec.split(",")

    node.addr_temp = node.addr
    node.set(node.freq, int(get_t[0]), node.power, node.rssi)
    node.send(get_t[1])
    time.sleep(0.2)
    node.set(node.freq, node.addr_temp, node.power, node.rssi)


try:
    time.sleep(1)

    while True:

        send_deal()

except:
    print("Sa matao")

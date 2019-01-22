#! /usr/bin/python3

import wiringpi as wpi
import datetime, logging, time

ECHO_PIN = 27
TRIG_PIN = 28
LED_PIN = 29
DIV_CM = 58.0
MAX_DIST = 23200
CM_MARGIN = 20.0
LOOP_DELAY = 60E-3
D_TOL = 3
    
# ProximitySensor requires one of the three wiringPi setup functions to be called before use
# WARNING: Make sure no other proximity processes are running, or setup() will definitely be corrupted!
class ProximitySensor():
    def __init__(self):
        self.det_count = 0
        self.detected = False
        self.range_o = -1

    def setup(self):
        # set up wiringPi
        wpi.wiringPiSetup()
        wpi.pinMode(TRIG_PIN, 1)
        wpi.pinMode(ECHO_PIN, 0)
        wpi.pinMode(LED_PIN, 1)
        wpi.digitalWrite(LED_PIN, 0)
        # set up logger
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%H:%M:%S', filename='debug-{0:%m}-{0:%d}-{0:%y}.log'.format(datetime.datetime.now()), filemode='w')
        logging.info('Starting Sensor')
        # get initial range
        self.range_o = self.getInitialRange()
        logging.info('Initial Range: {:.2f}'.format(self.range_o))

    def triggerEcho(self):
        wpi.digitalWrite(TRIG_PIN, 1)
        wpi.delayMicroseconds(10) # hold high for 10us
        wpi.digitalWrite(TRIG_PIN, 0)

    def readEcho(self):
        time_out = wpi.micros() + 3E6 # timeout at current time plus 3 seconds
        while time_out > wpi.micros() and wpi.digitalRead(ECHO_PIN) == 0:
            pass
        to = wpi.micros()
        while wpi.digitalRead(ECHO_PIN) == 1:
            pass
        tf = wpi.micros()
        return to, tf

    def calcRange(self, to, tf, cm=True):
        pwidth = tf - to
        return pwidth / DIV_CM

    def getInitialRange(self):
        self.triggerEcho()
        to, tf = self.readEcho()
        return self.calcRange(to, tf)

    def getRange(self):
        self.triggerEcho()
        to, tf = self.readEcho()
        return self.calcRange(to, tf)

    def scan(self):
        # maintain count of contiguous detections

        range = self.getRange()
        if range > self.range_o + CM_MARGIN:
            wpi.digitalWrite(LED_PIN, 0)
            self.det_count = 0
            self.detected = False
            # logging.info('-- measure out of range --')
        elif range <= self.range_o - CM_MARGIN:
            self.det_count = min(self.det_count + 1, D_TOL) # increment count of detections, max D_TOL
            if self.det_count == D_TOL and not self.detected: # per detection, only log ONCE
                wpi.digitalWrite(LED_PIN, 1)
                self.detected = True
                logging.info('Detected: {:.2f}'.format(range))
        else:
            self.det_count = max(self.det_count - 1, 0)
            if self.det_count == 0:
                self.detected = False
                wpi.digitalWrite(LED_PIN, 0)
        time.sleep(LOOP_DELAY)

if __name__ == "__main__":
    sensor = ProximitySensor()
    sensor.setup()

    while 1:
        sensor.scan()
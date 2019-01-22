# simple sonic sensor code app
<i> i.e. Just for fun, don't use this for any serious applications
</i>
## Prerequisites
1. HCSR04 sonic proximity sensor (two pin interface)
2. Raspberry Pi with updated Python3/pip3

## Install
1. Clone the repo onto your local machine and transfer to your Pi's filesystem, or just clone it to your Pi directly
2. Navigate to the project root:
```
pip3 install -r requirements.txt
```

## Usage
1. Change the pin constants (TRIG_PIN, ECHO _PIN, optional LED_PIN) to match your circuit
2. Be sure to call the setup method before calling other functions:
```
s = ProximitySensor()
s.setup()
...
```
3. Call `sensor.scan()` in a loop for simple logging of detection and ranging data

Note that only one sensor is supported per Pi! Do not try to use multiple sensors on the same circuit, as they will interfere with each other.


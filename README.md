# TankBot
Remote controlled tank-robot. Supports keyboard, PS3 controller and XBOX 360 controller. Can be used via SSH/putty or VNC-connection.

How it works: Establish a remote connection to Pi, and move the robot using your keyboard (or a game controller). WASD moves the tank and arrow keys turn the camera. Use [UV4L](https://www.linux-projects.org/uv4l/) to watch a video stream from the robot at http://[raspi-IP]:9090/stream

Programmed with Python.


## Hardware
**Computer:** [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)

**Operating system:** Raspbian 9.3 (Stretch)

**Chassis:** DFRobot's Devastator Tank Mobile Robot Platform with 2x 6V Metal DC Gear Motors [(product ID ROB0128)](https://www.dfrobot.com/product-1477.html)

**Camera:** [ZeroCam FishEye](https://thepihut.com/products/zerocam-fisheye-camera-for-raspberry-pi-zero)

**Camera mount:** Adafruit Mini Pan-Tilt kit with 2x Tower Pro SG90 Micro Servos. [(product ID 1967)](https://www.adafruit.com/product/1967)

**Servo controller:** Adafruit 16-Channel PWM / Servo HAT [(product ID 2327)](https://www.adafruit.com/product/2327)


**DC motor controller:** Adafruit DC & Stepper Motor HAT [(product ID 2348)](https://www.adafruit.com/product/2348)

## Media links
[Prototype, under development](https://youtu.be/k5S5gY3hc3g)
[Pan/tilt-kit working](https://www.youtube.com/watch?v=GreMILf87uk)

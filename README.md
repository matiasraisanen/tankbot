# TankBot

**PLEASE NOTE: If you are looking for the exact code used in my [bachelor's thesis](https://www.theseus.fi/handle/10024/155917), see release [v1.0.0](https://github.com/matiasraisanen/tankbot/releases/tag/v1.0.0).  
Code in the master branch is subject to changes over time, and may not reflect the thesis build.**

---

Remote controlled tank-robot. Supports keyboard, PS3 controller and XBOX 360 controller. Can be used via SSH/putty or VNC-connection.

How it works: Establish a remote connection to Pi, and move the robot using your keyboard (or a game controller). WASD moves the tank and arrow keys turn the camera. Use [UV4L](https://www.linux-projects.org/uv4l/) to watch a video stream from the robot at http://[raspi-IP]:9090/stream

Programmed with Python.

## Main programs

**sonarBot.py** ->
Autonomous robot. Detects and avoids obstacles using a sonar sensor. Once an object is close (20cm), stops and scans for a new direction.

**tankbot_KEYBOARD_X.X.py** ->
User-controlled tankbot. Use keyboard to move.

**tankbot_PS3_X.X.py** ->
User-controlled tankbot. Use PS3 controller to move.

Other programs are mainly tests, or programs for the HATs provided by Adafruit.

## Hardware

**Computer:** [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)

**Operating system:** Raspbian 9.3 (Stretch)

**Chassis:** DFRobot's Devastator Tank Mobile Robot Platform with 2x 6V Metal DC Gear Motors [(product ID ROB0128)](https://www.dfrobot.com/product-1477.html)

**Camera:** [Raspberry Pi Camera Module V2](https://thepihut.com/products/raspberry-pi-camera-module)

**Camera mount:** Adafruit Mini Pan-Tilt kit with 2x Tower Pro SG90 Micro Servos. [(product ID 1967)](https://www.adafruit.com/product/1967)

**Ultrasonic distance sensor:** [HC-SR04](https://thepihut.com/products/ultrasonic-distance-sensor-hcsr04)

**Servo controller:** Adafruit 16-Channel PWM / Servo HAT [(product ID 2327)](https://www.adafruit.com/product/2327)

**DC motor controller:** Adafruit DC & Stepper Motor HAT [(product ID 2348)](https://www.adafruit.com/product/2348)

## Media

<a href="http://www.youtube.com/watch?feature=player_embedded&v=k5S5gY3hc3g" target="_blank"><img src="http://img.youtube.com/vi/k5S5gY3hc3g/0.jpg" alt="KBControl" width="240" height="180" border="10" /></a><br> [Early version, keyboard control](https://youtu.be/k5S5gY3hc3g)

<a href="http://www.youtube.com/watch?feature=player_embedded&v=GreMILf87uk" target="_blank"><img src="http://img.youtube.com/vi/GreMILf87uk/0.jpg" alt="PanTil KBControl" width="240" height="180" border="10" /></a><br>[Pan/tilt-kit, keyboard control](https://www.youtube.com/watch?v=GreMILf87uk)

<a href="http://www.youtube.com/watch?feature=player_embedded&v=lVK4EL7_Mjs" target="_blank"><img src="http://img.youtube.com/vi/lVK4EL7_Mjs/0.jpg" alt="Relay Laser Pointer" width="240" height="180" border="10" /></a><br>[Relay controlled laser pointer](https://www.youtube.com/watch?v=lVK4EL7_Mjs)

<a href="http://www.youtube.com/watch?feature=player_embedded&v=kYUl4-z5d7g" target="_blank"><img src="http://img.youtube.com/vi/kYUl4-z5d7g/0.jpg" alt="SonarBot" width="240" height="180" border="10" /></a><br> [SonarBot 2.0 in action](https://youtu.be/kYUl4-z5d7g)

<a href="http://www.youtube.com/watch?feature=player_embedded&v=aily3uSGdJE" target="_blank"><img src="http://img.youtube.com/vi/aily3uSGdJE/0.jpg" alt="SonarBot avoiding obstacles" width="240" height="180" border="10" /></a><br> [Sonarbot avoiding more obstacles](https://youtu.be/aily3uSGdJE)

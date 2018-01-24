# tankbot
Remote controlled tank-robot. Supports keyboard, PS3 controller and XBOX 360 controller. Can be used via SSH/putty or VNC-connection.

How it works: Establish a remote connection to Pi, and move the robot using your keyboard (or a game controller). WASD moves the tank and arrow keys turn the camera. Use uv4l to watch a video stream from the robot at http://[raspi-IP]:9090/stream

Programmed with Python.


## Hardware
Chassis: DFRobot's Devastator Tank Mobile Robot Platform with 2x 6V Metal DC Gear Motors
Controlled by a Raspberry Pi 3, running Raspbian 9.3 Stretch.

Camera: ZeroCam FishEye, sitting on Adafruit Mini Pan-Tilt kit with 2x Tower Pro SG90 Micro Servos.

Micro Servos will be controlled via Adafruit 16-Channel PWM / Servo HAT (product ID 2327)

DC motors controlled via Adafruit DC & Stepper Motor HAT (product ID 2348)

Prototype, under development: https://youtu.be/k5S5gY3hc3g


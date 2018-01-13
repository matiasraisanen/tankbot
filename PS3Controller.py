#Class for reading PS3-controller.
#Based heavily on Martin O'Hanlon's class for an Xbox controller: http://www.stuffaboutcode.com/2014/10/raspberry-pi-xbox-360-controller-python.html

import pygame
from pygame.locals import *
import os, sys
import threading
import time

"""
NOTES - pygame events and values

JOYAXISMOTION
event.axis              event.value
0 - x axis left thumb   (+1 is right, -1 is left)
1 - y axis left thumb   (+1 is down, -1 is up)
2 - x axis right thumb  (+1 is right, -1 is left)
3 - y axis right thumb  (+1 is down, -1 is up)
4 - right trigger
5 - left trigger

JOYBUTTONDOWN | JOYBUTTONUP
event.button
A = 0
B = 1
X = 2
Y = 3
LB = 4
RB = 5
BACK = 6
START = 7
XBOX = 8
LEFTTHUMB = 9
RIGHTTHUMB = 10

JOYHATMOTION
event.value
[0] - horizontal
[1] - vertival
[0].0 - middle
[0].-1 - left
[0].+1 - right
[1].0 - middle
[1].-1 - bottom
[1].+1 - top

"""
#Main class for reading the PS3 controller values
class PS3Controller(threading.Thread):

    #internal ids for the PS3 controls
    class PS3Controls():
        LTHUMBX = 0
        LTHUMBY = 1
        RTHUMBX = 2
        RTHUMBY = 3
        RTRIGGER = 9
        LTRIGGER = 8
        CROSS = 14
        SPHERE = 13
        SQUARE = 15
        TRIANGLE = 12
        L1 = 10
        R1 = 11
        SELECT = 0
        START = 3
        XBOX = 16
        LEFTTHUMB = 1
        RIGHTTHUMB = 2
        DPADUP = 4
        DPADDOWN = 6
        DPADLEFT = 7
        DPADRIGHT = 5
    #pygame axis constants for the analogue controls of the PS3 controller
    class PyGameAxis():
        LTHUMBX = 0
        LTHUMBY = 1
        RTHUMBX = 2
        RTHUMBY = 3
        RTRIGGER = 13
        LTRIGGER = 12

    #pygame constants for the buttons of the PS3 controller
    class PyGameButtons():
	A = 14
        B = 13
        X = 15
        Y = 12
        LB = 10
        RB = 11
        BACK = 0
        START = 3
        XBOX = 16
        LEFTTHUMB = 1
        RIGHTTHUMB = 2
        RTRIGGER = 9
        LTRIGGER = 8
        DPADUP = 4
        DPADDOWN = 6
        DPADLEFT = 7
        DPADRIGHT = 5


    #map between pygame axis (analogue stick) ids and PS3 control ids
    AXISCONTROLMAP = {PyGameAxis.LTHUMBX: PS3Controls.LTHUMBX,
                      PyGameAxis.LTHUMBY: PS3Controls.LTHUMBY,
                      PyGameAxis.RTHUMBX: PS3Controls.RTHUMBX,
                      PyGameAxis.RTHUMBY: PS3Controls.RTHUMBY}
    
    #map between pygame axis (trigger) ids and PS3 control ids
    TRIGGERCONTROLMAP = {PyGameAxis.RTRIGGER: PS3Controls.RTRIGGER,
                         PyGameAxis.LTRIGGER: PS3Controls.LTRIGGER}

    #map between pygame buttons ids and PS3 control ids
    BUTTONCONTROLMAP = {PyGameButtons.A: PS3Controls.CROSS,
                        PyGameButtons.B: PS3Controls.SPHERE,
                        PyGameButtons.X: PS3Controls.SQUARE,
                        PyGameButtons.Y: PS3Controls.TRIANGLE,
                        PyGameButtons.LB: PS3Controls.L1,
                        PyGameButtons.RB: PS3Controls.R1,
                        PyGameButtons.BACK: PS3Controls.SELECT,
                        PyGameButtons.START: PS3Controls.START,
                        PyGameButtons.XBOX: PS3Controls.XBOX,
                        PyGameButtons.LEFTTHUMB: PS3Controls.LEFTTHUMB,
                        PyGameButtons.RIGHTTHUMB: PS3Controls.RIGHTTHUMB,
                        PyGameButtons.DPADUP: PS3Controls.DPADUP,
                        PyGameButtons.DPADDOWN: PS3Controls.DPADDOWN,
                        PyGameButtons.DPADLEFT: PS3Controls.DPADLEFT,
                        PyGameButtons.DPADRIGHT: PS3Controls.DPADRIGHT}
                        
    #setup xbox controller class
    def __init__(self,
                 controllerCallBack = None,
                 joystickNo = 0,
                 deadzone = 0.1,
                 scale = 1,
                 invertYAxis = False):

        #setup threading
        threading.Thread.__init__(self)
        
        #persist values
        self.running = False
        self.controllerCallBack = controllerCallBack
        self.joystickNo = joystickNo
        self.lowerDeadzone = deadzone * -1
        self.upperDeadzone = deadzone
        self.scale = scale
        self.invertYAxis = invertYAxis
        self.controlCallbacks = {}

        #setup controller properties
        self.controlValues = {self.PS3Controls.LTHUMBX:0,
                              self.PS3Controls.LTHUMBY:0,
                              self.PS3Controls.RTHUMBX:0,
                              self.PS3Controls.RTHUMBY:0,
                              self.PS3Controls.RTRIGGER:0,
                              self.PS3Controls.LTRIGGER:0,
                              self.PS3Controls.CROSS:0,
                              self.PS3Controls.SPHERE:0,
                              self.PS3Controls.SQUARE:0,
                              self.PS3Controls.TRIANGLE:0,
                              self.PS3Controls.L1:0,
                              self.PS3Controls.R1:0,
                              self.PS3Controls.SELECT:0,
                              self.PS3Controls.START:0,
                              self.PS3Controls.XBOX:0,
                              self.PS3Controls.LEFTTHUMB:0,
                              self.PS3Controls.RIGHTTHUMB:0,
                              self.PS3Controls.DPADUP:0,
                              self.PS3Controls.DPADDOWN:0,
                              self.PS3Controls.DPADLEFT:0,
                              self.PS3Controls.DPADRIGHT:0,
                              }

        #setup pygame
        self._setupPygame(joystickNo)

    #Create controller properties
    @property
    def LTHUMBX(self):
        return self.controlValues[self.PS3Controls.LTHUMBX]

    @property
    def LTHUMBY(self):
        return self.controlValues[self.PS3Controls.LTHUMBY]

    @property
    def RTHUMBX(self):
        return self.controlValues[self.PS3Controls.RTHUMBX]

    @property
    def RTHUMBY(self):
        return self.controlValues[self.PS3Controls.RTHUMBY]

    @property
    def RTRIGGER(self):
        return self.controlValues[self.PS3Controls.RTRIGGER]

    @property
    def LTRIGGER(self):
        return self.controlValues[self.PS3Controls.LTRIGGER]

    @property
    def CROSS(self):
        return self.controlValues[self.PS3Controls.CROSS]

    @property
    def SPHERE(self):
        return self.controlValues[self.PS3Controls.SPHERE]

    @property
    def SQUARE(self):
        return self.controlValues[self.PS3Controls.SQUARE]

    @property
    def TRIANGLE(self):
        return self.controlValues[self.PS3Controls.TRIANGLE]

    @property
    def L1(self):
        return self.controlValues[self.PS3Controls.L1]

    @property
    def R1(self):
        return self.controlValues[self.PS3Controls.R1]

    @property
    def SELECT(self):
        return self.controlValues[self.PS3Controls.SELECT]

    @property
    def START(self):
        return self.controlValues[self.PS3Controls.START]

    @property
    def XBOX(self):
        return self.controlValues[self.PS3Controls.XBOX]

    @property
    def LEFTTHUMB(self):
        return self.controlValues[self.PS3Controls.LEFTTHUMB]

    @property
    def RIGHTTHUMB(self):
        return self.controlValues[self.PS3Controls.RIGHTTHUMB]

    @property
    def DPADUP(self):
        return self.controlValues[self.PS3Controls.DPADUP]

    @property
    def DPADDOWN(self):
        return self.controlValues[self.PS3Controls.DPADDOWN]

    @property
    def DPADLEFT(self):
        return self.controlValues[self.PS3Controls.DPADLEFT]

    @property
    def DPADRIGHT(self):
        return self.controlValues[self.PS3Controls.DPADRIGHT]

    #setup pygame
    def _setupPygame(self, joystickNo):
        # set SDL to use the dummy NULL video driver, so it doesn't need a windowing system.
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        # init pygame
        pygame.init()
        # create a 1x1 pixel screen, its not used so it doesnt matter
        screen = pygame.display.set_mode((1, 1))
        # init the joystick control
        pygame.joystick.init()
        # how many joysticks are there
        #print pygame.joystick.get_count()
        # get the first joystick
        joy = pygame.joystick.Joystick(joystickNo)
        # init that joystick
        joy.init()

    #called by the thread
    def run(self):
        self._start()

    #start the controller
    def _start(self):
        
        self.running = True
        
        #run until the controller is stopped
        while(self.running):
            #react to the pygame events that come from the xbox controller
            for event in pygame.event.get():

                #thumb sticks, trigger buttons                    
                if event.type == JOYAXISMOTION:
                    #is this axis on our xbox controller
                    if event.axis in self.AXISCONTROLMAP:
                        #is this a y axis
                        yAxis = True if (event.axis == self.PyGameAxis.LTHUMBY or event.axis == self.PyGameAxis.RTHUMBY) else False
                        #update the control value
                        self.updateControlValue(self.AXISCONTROLMAP[event.axis],
                                                self._sortOutAxisValue(event.value, yAxis))
                    #is this axis a trigger
                    if event.axis in self.TRIGGERCONTROLMAP:
                        #update the control value
                        self.updateControlValue(self.TRIGGERCONTROLMAP[event.axis],
                                                self._sortOutTriggerValue(event.value))
                        
                #d pad
                elif event.type == JOYHATMOTION:
                    #update control value
                    
                    self.updateControlValue(self.PS3Controls.DPAD, event.value)

                #button pressed and unpressed
                elif event.type == JOYBUTTONUP or event.type == JOYBUTTONDOWN:
                    #is this button on our xbox controller
                    if event.button in self.BUTTONCONTROLMAP:
                        #update control value
                        self.updateControlValue(self.BUTTONCONTROLMAP[event.button],
                                                self._sortOutButtonValue(event.type))
        
    #stops the controller
    def stop(self):
        self.running = False

    #updates a specific value in the control dictionary
    def updateControlValue(self, control, value):
        #if the value has changed update it and call the callbacks
        if self.controlValues[control] != value:
            self.controlValues[control] = value
            self.doCallBacks(control, value)
    
    #calls the call backs if necessary
    def doCallBacks(self, control, value):
        #call the general callback
        if self.controllerCallBack != None: self.controllerCallBack(control, value)

        #has a specific callback been setup?
        if control in self.controlCallbacks:
            self.controlCallbacks[control](value)
            
    #used to add a specific callback to a control
    def setupControlCallback(self, control, callbackFunction):
        # add callback to the dictionary
        self.controlCallbacks[control] = callbackFunction
                
    #scales the axis values, applies the deadzone
    def _sortOutAxisValue(self, value, yAxis = False):
        #invert yAxis
        if yAxis and self.invertYAxis: value = value * -1
        #scale the value
        value = value * self.scale
        #apply the deadzone
        if value < self.upperDeadzone and value > self.lowerDeadzone: value = 0
        return value

    #turns the trigger value into something sensible and scales it
    def _sortOutTriggerValue(self, value):
        #trigger goes -1 to 1 (-1 is off, 1 is full on, half is 0) - I want this to be 0 - 1
        value = max(0,(value + 1) / 2)
        #scale the value
        value = value * self.scale
        return value

    #turns the event type (up/down) into a value
    def _sortOutButtonValue(self, eventType):
        #if the button is down its 1, if the button is up its 0
        value = 1 if eventType == JOYBUTTONDOWN else 0
        return value
    
#tests
if __name__ == '__main__':

    #generic call back
    def controlCallBack(xboxControlId, value):
        print "Control Id = {}, Value = {}".format(xboxControlId, value)


    #specific callbacks for the left thumb (X & Y)
    #def leftThumbX(xValue):
    #    print "LX {}".format(xValue)
    #def leftThumbY(yValue):
    #    print "LY {}".format(yValue)

    #setup xbox controller, set out the deadzone and scale, also invert the Y Axis (for some reason in Pygame negative is up - wierd! 
    PS3Cont = PS3Controller(controlCallBack, deadzone = 30, scale = 100, invertYAxis = True)

    #setup the left thumb (X & Y) callbacks
    #PS3Cont.setupControlCallback(PS3Cont.PS3Controls.LTHUMBX, leftThumbX)
    #PS3Cont.setupControlCallback(PS3Cont.PS3Controls.LTHUMBY, leftThumbY)

    try:
        #start the controller
        PS3Cont.start()
        print "PS3 controller running"
        while True:
            time.sleep(1)

    #Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"
    
    #error        
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
        
    finally:
        #stop the controller
        PS3Cont.stop()

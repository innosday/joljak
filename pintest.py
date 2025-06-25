from limitswitch import LimitSwitch
from stepmoter import StepMoter
from servo import Servo

grap = Servo(1)

xleft = LimitSwitch(20)
xright = LimitSwitch(16)
yleft = LimitSwitch(21)
yright = LimitSwitch(12)


xmoter = StepMoter(14,15)
ymoter = StepMoter(25,8)
zmoter = StepMoter(23,24)

xmoter.TurnRotation()
xmoter.Action(40,0.001)
ymoter.TurnRotation()
ymoter.Action(40,0.001)
zmoter.TurnRotation()
zmoter.Action(40,0.001)
try:
    while True:
        print(f"xleft:{xleft.digitalRead()} | xright:{xright.digitalRead()}\nyleft:{yleft.digitalRead()} | yright:{yright.digitalRead()}\n-----------------")
        grap.servoPos(180)
        grap.servoPos(0)
except KeyboardInterrupt:
    pass

xleft.cleanup()
xright.cleanup()
yleft.cleanup()
yright.cleanup()
grape.cleanup()

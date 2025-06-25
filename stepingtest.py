from stepmoter import StepMoter
from limitswitch import LimitSwitch

x = StepMoter(14,15)
y= StepMoter(23,24)
grap = StepMoter(25,8)

#s = LimitSwitch(14)
#$ss = LimitSwitch(15)

move = False
    
def smapleStep(entity:StepMoter,steps,delay,rotation=False):
    entity.TurnRotation(rotation)
    entity.Action(steps,delay)

try:
    while True:
            smapleStep(x,5,0.001)
            smapleStep(y,5,0.001)
            smapleStep(grap,5,0.001)
    #if not s.digitalRead() and not move:
        #    x.TurnRotation()
         #   x.Action(5,0.001)
        #else:
         #   move=True
        #if not ss.digitalRead() and move:
         #   x.TurnRotation(True)
         #   x.Action(5,0.001)
        #else:
         #   move=False
except KeyboardInterrupt:
    pass

s.cleanup()
x.cleanup()

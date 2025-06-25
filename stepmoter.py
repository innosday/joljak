import gpiozero,time

class StepMoter:
    def __init__(self,step,direction):
        self.step_pin = gpiozero.OutputDevice(step)
        self.direction_pin = gpiozero.OutputDevice(direction)
        self.step_pin.off()
        self.direction_pin.off()

    def TurnRotation(self,rotation=False):
        if rotation:
            self.direction_pin.on()
        else:
            self.direction_pin.off()
    def Action(self,steps,delay):
        for _ in range(steps):
            self.step_pin.on()
            time.sleep(delay)
            self.step_pin.off()
            time.sleep(delay)

    def cleanup(self):
        self.step_pin.off()
        self.direction_pin.off()

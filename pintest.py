from limitswitch import LimitSwitch

xleft = LimitSwitch(20)
xright = LimitSwitch(16)
yleft = LimitSwitch(21)
yright = LimitSwitch(12)

try:
    while True:
        print(f"xleft:{xleft.digitalRead()} | xright:{xright.digitalRead()}\nyleft:{yleft.digitalRead()} | yright:{yright.digitalRead()}\n-----------------")
except KeyboardInterrupt:
    pass

xleft.cleanup()
xright.cleanup()
yleft.cleanup()
yright.cleanup()

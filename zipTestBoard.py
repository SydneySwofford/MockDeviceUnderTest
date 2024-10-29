import time
from customExceptions import ActuatorError

class zipTestBoard:
    def __init__(self):
        self.deviceStatus="ON"
        self.powerSupply="0V"

    def getDeviceStatus(self):
        return self.deviceStatus


    def turnOnPs(self,supply):
        self.powerSupply=supply

    def turnOffPs(self, supply):
        if supply not in "0.0":
            raise ValueError("Input Voltage does not turn Power Supply off")
        self.powerSupply=supply

    def i2cSetup(self, sda,scl,freq):
        #for now dont implement
        print("i2c is setup")

    def i2cCmd(self, addr, data,resp_len=0):
        #for now dont implement
        print("Written to Device")

    def actuatorMove(self,config):
        match config:
            case "slow_climb":
                print("Doing Slow Climb")
                time.sleep(10)

            case "sharp_turn":
                print("Doing Sharp Turn")
                time.sleep(10)
            
            case "quick_drop":
                print("Doing Quick Drop")
                time.sleep(10)

            case "fail":
                #make actuator fail
                raise ActuatorError("Actuator has Failed")
            case _:
                raise ValueError("Invalid Actuator Input")
            



    
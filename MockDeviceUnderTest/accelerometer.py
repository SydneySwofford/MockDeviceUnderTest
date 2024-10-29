import random

class MockAccelerometer:
    def __init__(self, rangeG=2):
        self.rangeG=rangeG
        self.x=0.0
        self.y=0.0
        self.z=0.0

    def randomAcceleration(self):
        self.x=random.uniform(-self.rangeG,self.rangeG)
        self.y=random.uniform(-self.rangeG,self.rangeG)
        self.z=random.uniform(-self.rangeG,self.rangeG)
    
    def setRange(self, newRange):
        if newRange not in [2,4,8,16]:
            raise ValueError("Invalid Range Choose Between [2,4,8,16]")
        self.rangeG=newRange

    def mockAccelerationValues(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z

    def readAcceleration(self):
        return self.x, self.y, self.z



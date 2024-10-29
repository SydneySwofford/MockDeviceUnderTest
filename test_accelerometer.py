import pytest
import time
import logging
from accelerometer import MockAccelerometer
from zipTestBoard import zipTestBoard

logging.basicConfig(filename="newfile.txt",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger=logging.getLogger()

logger.setLevel(logging.DEBUG)

@pytest.fixture(scope="session", autouse=True)
def zipBoard():
    zB=zipTestBoard()
    zB.turnOnPs("3V3")
    print("ZipBoard is Powered")
    yield zB
    zB.turnOffPs("0.0")

#using Mock and not real Hardware, bring up new accelerometer for each test
@pytest.fixture()
def newMockAccelerometer():
    return MockAccelerometer(rangeG=16)

def logTestResult(testName, startTime, passed, exception=None):
    elapsedTime = time.time() - startTime
    if passed:
        logger.info(f"{testName}: TEST PASSED in {elapsedTime:.3f} sec")
    else:
        logger.error(f"{testName}: TEST FAILED in {elapsedTime:.3f} sec due to {str(exception)}")



def test_zipStatus(zipBoard):

    startTime=time.time()
    try:
        assert zipBoard.getDeviceStatus()=="ON"
        logTestResult("test_zipStatus", startTime,True)
    except Exception as e:
        logTestResult("test_zipStatus", startTime,False,e)


def test_configureAccelerometerForMaxRange(newMockAccelerometer):
    startTime=time.time()
    maxRange=16

    try:
        newMockAccelerometer.setRange(maxRange)
        newMockAccelerometer.randomAcceleration()
        accelX,accelY,accelZ=newMockAccelerometer.readAcceleration()
        assert -16.00 <= accelX <= 16.00
        assert -16.00 <= accelY <= 16.00
        assert -16.00 <= accelZ <= 16.00
        logTestResult("test_configureAccelerometerForMaxRange", startTime, True)

    except Exception as e:
        logTestResult("test_configureAccelerometerForMaxRange", startTime, False,e)


def test_accelerometerSelfTest(newMockAccelerometer):
    startTime = time.time()
    try:
        for rangeG in [2, 4, 8, 16]:
            newMockAccelerometer.setRange(rangeG)
            newMockAccelerometer.randomAcceleration()
            accelX, accelY, accelZ = newMockAccelerometer.readAcceleration()

            assert -rangeG <= accelX <= rangeG
            assert -rangeG <= accelY <= rangeG
            assert -rangeG <= accelZ <= rangeG
        logTestResult("test_accelerometerSelfTest", startTime, True)
    except Exception as e:
        logTestResult("test_accelerometerSelfTest", startTime, False, e)


def test_slowClimbMotionRandom(zipBoard, newMockAccelerometer):    
    duration = 10
    samplingRate = 0.00125
    samples = int(duration / samplingRate)
    action = "slow_climb"

    startTime = time.time()
    try:
        zipBoard.actuatorMove(action)

        for i in range(samples):
            newMockAccelerometer.randomAcceleration()
            accelX, accelY, accelZ = newMockAccelerometer.readAcceleration()

            assert -1.00 <= accelY <= 1.00
            assert 6.00 <= accelZ <= 8.00

            time.sleep(samplingRate)

        logTestResult("test_slowClimbMotionRandom", startTime, True)

    except AssertionError as e:
        logTestResult("test_slowClimbMotionRandom", startTime, False, e)

    except Exception as e:
        logTestResult("test_slowClimbMotionRandom", startTime, False, e)


def test_slowClimbMotionSetValues(zipBoard,newMockAccelerometer):
    # ODR=800Hz--> sampling every 1.25ms
    startTime = time.time()
    try:
        duration = 10
        samplingRate = 0.00125
        samples = int(duration / samplingRate)
        zipBoard.actuatorMove("slow_climb")

        for _ in range(samples):
            newMockAccelerometer.mockAccelerationValues(16, 0.5, 7)
            accelX, accelY, accelZ = newMockAccelerometer.readAcceleration()

            assert -1.00 <= accelY <= 1.00
            assert 6.00 <= accelZ <= 8.00
            time.sleep(samplingRate)
        logTestResult("test_slowClimbMotionSetValues", startTime, True)
    except Exception as e:
        logTestResult("test_slowClimbMotionSetValues", startTime, False, e)

def test_sharpTurnMotionRandom(zipBoard, newMockAccelerometer):
    # ODR=800Hz --> sampling every 1.25ms
    duration = 10
    samplingRate = 0.00125
    samples = int(duration / samplingRate)
    action = "sharp_turn"

    startTime = time.time()
    try:
        zipBoard.actuatorMove(action)
        for i in range(samples):
            maxRange = 16
            newMockAccelerometer.randomAcceleration()
            accelX, accelY, accelZ = newMockAccelerometer.readAcceleration()

            assert 5.00 <= accelX <= maxRange
            assert 5.00 <= accelY <= maxRange

            time.sleep(samplingRate)

        logTestResult("test_sharpTurnMotionRandom", startTime, True)

    except AssertionError as e:
        logTestResult("test_sharpTurnMotionRandom", startTime, False, e)

    except Exception as e:
        logTestResult("test_sharpTurnMotionRandom", startTime, False, e)

def test_sharpTurnMotionSetValues(zipBoard,newMockAccelerometer):
    # ODR=800Hz--> sampling every 1.25ms
    startTime = time.time()
    try:
        duration = 10
        samplingRate = 0.00125
        samples = int(duration / samplingRate)
        zipBoard.actuatorMove("sharp_turn")

        for _ in range(samples):
            newMockAccelerometer.mockAccelerationValues(6, 6.25, 7)
            accelX, accelY, _ = newMockAccelerometer.readAcceleration()

            assert 5.00 <= accelX <= 16.00
            assert 5.00 <= accelY <= 16.00
            time.sleep(samplingRate)
        logTestResult("test_sharpTurnMotionSetValues", startTime, True)
    except Exception as e:
        logTestResult("test_sharpTurnMotionSetValues", startTime, False, e)


def test_quickDropMotionRandom(zipBoard, newMockAccelerometer):
    # ODR=800Hz --> sampling every 1.25ms
    duration = 10
    samplingRate = 0.00125
    samples = int(duration / samplingRate)
    minRange = -16
    action = "quick_drop"

    startTime = time.time()
    try:
        zipBoard.actuatorMove(action)

        for i in range(samples):
            newMockAccelerometer.randomAcceleration()
            accelX, accelY, accelZ = newMockAccelerometer.readAcceleration()

            assert accelZ >= minRange
            assert accelZ <= -8.00
            time.sleep(samplingRate)

        logTestResult("test_quickDropMotionRandom", startTime, True)

    except AssertionError as e:
        logTestResult("test_quickDropMotionRandom", startTime, False, e)

    except Exception as e:
        logTestResult("test_quickDropMotionRandom", startTime, False, e)

def test_quickDropMotionSetValues(zipBoard,newMockAccelerometer):
    # ODR=800Hz--> sampling every 1.25ms
    startTime = time.time()
    try:
        duration = 10
        samplingRate = 0.00125
        samples = int(duration / samplingRate)
        zipBoard.actuatorMove("quick_drop")

        for _ in range(samples):
            newMockAccelerometer.mockAccelerationValues(16, 0.5, -16)
            _, _, accelZ = newMockAccelerometer.readAcceleration()

            assert -16.00 <= accelZ <= -8.00
            time.sleep(samplingRate)
        logTestResult("test_quickDropMotionSetValues", startTime, True)
    except Exception as e:
        logTestResult("test_quickDropMotionSetValues", startTime, False, e)





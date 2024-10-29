# Accelerometer Testing Project

## 1. Project Overview
To test the accelerometer ADXL345 under different scenarios. Approx 160 coding minutes were used in the creation of this project. Additional minutes were used for planning, understanding the accelerometer, and reviewing the project.

## 2. Assumptions
- Using mock objects as there is no real hardware.
- Accelerometer ranges vary from 2, 4, 8, 16 ± g; for test cases, 16g was used.
- Accelerometer has different ranges for changes in precision, i.e., better track small changes or large jolts.
- Accelerometer ODR is 100Hz, which indicates proper sampling time.
- Assumed certain functions didn't need to actually be fleshed out but were written as placeholders, such as zipBoard functions.
- Assumed the zipBoard would only be powered on and off once in the given test session.
- 3v3 power is sufficient to power the accelerometer

## 3. Testing Approach
Implemented tests to show PASS and FAIL results by injecting fake data into the mock accelerometer class.

### Fixtures
`zipBoard` and `newMockAccelerometer` fixtures were used to have structured bring-up and tear-down of the zipBoard as well as the newMockAccelerometer, so as not to interfere with other tests.

### Test Methods
- `test_zipStatus`: Confirm the status of the zipBoard.
- `test_configureAccelerometerForMaxRange`: Confirm accelerometer is working properly to output data for max range.
- `test_accelerometerSelfTest`: Test the accelerometer outputs proper ranges for each g precision.
- `test_slowClimbMotionRandom`: Designed to FAIL, passes in random accel values that may or may not be within range during "slow_climb".
- `test_slowClimbSetValues`: Designed to PASS, passes in acceptable accel values during "slow_climb".
- `test_sharpTurnMotionRandom`: Designed to FAIL, passes in random accel values that may or may not be within range during "sharp_turn".
- `test_sharpTurnSetValues`: Designed to PASS, passes in acceptable accel values during "sharp_turn".
- `test_quickDropMotionRandom`: Designed to FAIL, passes in random accel values that may or may not be within range during "quick_drop".
- `test_quickDropMotionSetValues`: Designed to PASS, passes in acceptable accel values during "quick_drop".

## 4. Test Implementation
Assertions were used to validate the tests, whether they pass or fail, and logging was used to relay test information.

## 5. Improvements and Future Work
Many other test methods could be added, such as:
- Boundary condition checks.
- More robust exception handling.
- Power supply checks.
- Multiple actuator movements one after another.

Additionally, the zipBoard class could be built out more, and more functions could be added to better interact with the newMockAccelerometer.

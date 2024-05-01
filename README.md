# LIDAR 3D Mapping
Final Project - Georgia Tech - Embedded Systems Design - ECE 4180 - Spring 2024<br>
Create 3D point models with the mBed microcontroller, basic hardware peripherals, and a 3D rendering desktop application
<br><br><br>

## Author
Connor Sempf - [connortsempf](https://github.com/connortsempf)
<br><br><br>

## Description
This project combines a bluetooth breakout board and two-servo, two-axis controlled LIDAR ToF scanner. It transmits polar coordinate data via USB virtual COM Port to a PC for mapping to 3D space coordinates in a pygame 3D rendering desktop application. This allows the user to visualize their scanned object and use the data for any 3D modelling application. Data is mapped and rendered in real-time so watching the LIDAR acquisition is possible. Manual servo control is enabled to calibrate a relative zero position for LIDAR alignment, and set new vertical and horizontal scanning range boundaries. 
<br><br><br>

## Features
- **LIDAR Distance Scanning**: The main component of this device setup is to retrieve distance scanning data from the LIDAR ToF sensor. The breakout board will return a millimeter distance value when called upon.
- **Bluetooth Control**: With the bluetooth chip, the user can communicate with the servos and LIDAR sensor to initialize a scanning period for rendering, set relative zero positions for the servos to create a repeatable starting point, and maneuver the actuators manually for determining a scanning range.
- **2-Axis Servo Maneuvering**: The user can instruct the servos to independently move vertically and horizontally by a variable degree interval. This gives an editable 2D area of scanning.
- **3D Rendering and Visualization**: The desktop python pygame application plots coordinate points in 3D space received from the mBED and LIDAR sensor to provide the user with a view of any scanned object. The software has full capability of rotating, scaling, and translating views to see the model from any angle.
- **3D Printed Supports**: Contained in this repository are 3D models and STL files for printing. These components are used to hold together the pivoting mechanism for the LIDAR sensor and servo motors.
<br><br><br>

## Devices and Components
**Hardware Components:**
- mBed LPC1768 Microcontroller - [Reference Site](https://os.mbed.com/platforms/mbed-LPC1768/)
- Adafruit Bluefruit LE Uart Bluetooth Board - [Reference Site](https://os.mbed.com/users/4180_1/notebook/adafruit-bluefruit-le-uart-friend---bluetooth-low-/)
- Adafruit VL53L0X LIDAR ToF Distance Sensor Board - [Reference Site](https://os.mbed.com/users/4180_1/code/HelloWorld_VL53L0X_LPC1768/)
- HiTEC HS-422 Deluxe Servo Motor (2) - [Reference Site](https://os.mbed.com/users/4180_1/notebook/an-introduction-to-servos/)<br><br>

**Miscellaneous Components:**
- 3D Printed Parts
- 30 Row Solderless Breadboard
- 63 Row Solderless Breadboard
- Mini-USB to USB-A Cable
- Smartphone with "Bluefruit Connect" App
- PC or Laptop
- 5V Supply
- Jumper Wires<br><br>

**Hardware Wiring Diagram:**<br><br>
<img src="Demo-Resources/Images/HardwareWiringDiagram.png" alt="Hardware Wiring Diagram" style="height: 500px;"><br><br>

**3D Printed Part Models:**<br><br>
<img src="3D-Models/Images/DeviceAssembly_Front.png" alt="Device Assembly Front" style="height: 300px;">
<img src="3D-Models/Images/DeviceAssembly_Rear.png" alt="Device Assembly Rear" style="height: 300px;"><br>
<img src="3D-Models/Images/BreadboardHolder3DModelImage.png" alt="Breadboard Holder 3D Model Image" style="height: 300px;">
<img src="3D-Models/Images/BreadboardHolder3DModelImage_Transparent.png" alt="Breadboard Holder 3D Model Image Transparent" style="height: 300px;"><br>
<img src="3D-Models/Images/HorizontalServoHolder3DModelImage.png" alt="Horizontal Servo Holder 3D Model Image" style="height: 300px;">
<img src="3D-Models/Images/HorizontalServoHolder3DModelImage_Transparent.png" alt="Horizontal Servo Holder 3D Model Image Transparent" style="height: 300px;"><br>
<img src="3D-Models/Images/VerticalServoHolder3DModelImage.png" alt="Vertical Servo Holder 3D Model Image" style="height: 300px;">
<img src="3D-Models/Images/VerticalServoHolder3DModelImage_Transparent.png" alt="Vertical Servo Holder 3D Model Image Transparent" style="height: 300px;">
<br><br><br>

## Images and Demos
**Component Images:**<br><br>
<img src="Demo-Resources/Images/LIDAR-FrontView.png" alt="Front View" style="height: 400px;">
<img src="Demo-Resources/Images/Setup-RearView.png" alt="Rear View" style="height: 400px;"><br>
<img src="Demo-Resources/Images/Servos-RearView.png" alt="Angled Rear View" style="height: 400px;">
<img src="Demo-Resources/Images/Breadboard-TopView.png" alt="Breadboard Top View" style="height: 400px;"><br>
<img src="Demo-Resources/Images/Setup-TopView.png" alt="Top View" style="height: 400px;"><br><br>
**Device Demos**:<br>
- [Servo Reset and Relative Zero Positioning](https://youtu.be/zzRhkBZBalc)
- [LIDAR Scanning Rear View](https://youtu.be/IgyYRwqueXU)
- [LIDAR Scanning Timelapse](https://youtu.be/QPMSIuET8sY)
- [Real Time Coordinate Mapping](https://youtu.be/MMdZRRT5r-Q)
- [Coordinate Rendering Visualization](https://youtu.be/nc9mq8p97Q0)<br><br>
<br><br><br>

## 3D Rendering Source Code
Files for the desktop application are found in the *LIDAR-Mapping-3D-Rendering-Source-Code* directory above.<br>
Make sure to run the *main.py* file and adjust the COM port if needed before starting the scanning sequence so the LIDAR data is actually mapped.
<br><br><br>

## Hardware Source Code
```c
#include "mbed.h"
#include "XNucleo53L0A1.h"
#include <cstdint>
#include <stdio.h>
#include "Servo.h"




// Servo //
#define absZeroPos              0.0
#define relativeZeroUDPos     -18.5
#define relativeZeroLRPos      -8.0
#define lidarMapUDStartPos    -10.0
#define lidarMapUDEndPos      -32.0
#define lidarMapLRStartPos    -20.0
#define lidarMapLREndPos        4.0
#define lidarPointsStep         1
#define variableRotate          0.5
#define autoRotate              0.25
Servo   udServo(p21);
Servo   lrServo(p22);
float   currentUDPos = 0;
float   currentLRPos = 0;
int     verticalLIDARPoints = (lidarMapUDStartPos - lidarMapUDEndPos) / lidarPointsStep;
int     horizontalLIDARPoints = (lidarMapLREndPos - lidarMapLRStartPos) / lidarPointsStep;

// LIDAR and I2C //
DigitalOut  shdn(p26);
#define     VL53L0_I2C_SDA   p28
#define     VL53L0_I2C_SCL   p27
static      XNucleo53L0A1 *board = NULL;
int         status;
uint32_t    lidarDistance;
uint32_t    lidarDistanceOffset = 34;
uint32_t    currentDistance;
DevI2C*     device_i2c = new DevI2C(VL53L0_I2C_SDA, VL53L0_I2C_SCL);

// Controller //
Serial controller(p13, p14);

// Serial Console //
Serial console(USBTX, USBRX);

// MBED LED's //
DigitalOut mbedLED1(LED1);
DigitalOut mbedLED2(LED2);
DigitalOut mbedLED3(LED3);
DigitalOut mbedLED4(LED4);




// Initialization Functions //
void initializeLIDARSensor() {
    board = XNucleo53L0A1::instance(device_i2c, A2, D8, D2);
    shdn = 0;
    wait(0.1);
    shdn = 1;
    wait(0.1);
    status = board->init_board();
    while (status) {
        console.printf("Failed to init board!\r\n");
        status = board->init_board();
    }
}




// General Functions //
void printServoPositions() {
    console.printf("Up/Down: %4.2f Left/Right: %4.2f\r\n", currentUDPos, currentLRPos);
}

void zeroPosUDServo() {
    if (currentUDPos > absZeroPos) {
        while (currentUDPos > absZeroPos) {
            currentUDPos = currentUDPos - autoRotate;
            udServo.position(currentUDPos);
            wait(0.01);
        }
    }   else if (currentUDPos < absZeroPos) {
        while (currentUDPos < absZeroPos) {
            currentUDPos = currentUDPos + autoRotate;
            udServo.position(currentUDPos);
            wait(0.01);
        }
    }
    currentUDPos = absZeroPos;
    udServo.position(absZeroPos);
}

void zeroPosLRServo() {
    if (currentLRPos > absZeroPos) {
        while (currentLRPos > absZeroPos) {
            currentLRPos = currentLRPos - autoRotate;
            lrServo.position(currentLRPos);
            wait(0.01);
        }
    }   else if (currentLRPos < absZeroPos) {
        while (currentLRPos < absZeroPos) {
            currentLRPos = currentLRPos + autoRotate;
            lrServo.position(currentLRPos);
            wait(0.01);
        }
    }
    currentLRPos = absZeroPos;
    lrServo.position(absZeroPos);
}

void zeroPosAllServos() {
    zeroPosUDServo();
    zeroPosLRServo();
    for (int i = 0; i < 4; i++) {
        mbedLED1 = !mbedLED1;
        mbedLED2 = !mbedLED2;
        mbedLED3 = !mbedLED3;
        mbedLED4 = !mbedLED4;
        wait(0.1);
    }
}

void relativeZeroPosUDServo() {
    if (currentUDPos > relativeZeroUDPos) {
        while (currentUDPos > relativeZeroUDPos) {
            currentUDPos = currentUDPos - autoRotate;
            udServo.position(currentUDPos);
            wait(0.01);
        }
    }   else if (currentUDPos < relativeZeroUDPos) {
        while (currentUDPos < relativeZeroUDPos) {
            currentUDPos = currentUDPos + autoRotate;
            udServo.position(currentUDPos);
            wait(0.01);
        }
    }
    currentUDPos = relativeZeroUDPos;
    udServo.position(relativeZeroUDPos);
}

void relativeZeroPosLRServo() {
    if (currentLRPos > relativeZeroLRPos) {
        while (currentLRPos > relativeZeroLRPos) {
            currentLRPos = currentLRPos - autoRotate;
            lrServo.position(currentLRPos);
            wait(0.01);
        }
    }   else if (currentLRPos < relativeZeroLRPos) {
        while (currentLRPos < relativeZeroLRPos) {
            currentLRPos = currentLRPos + autoRotate;
            lrServo.position(currentLRPos);
            wait(0.01);
        }
    }
    currentLRPos = relativeZeroLRPos;
    lrServo.position(relativeZeroLRPos);
}

void relativeZeroPosAllServos() {
    relativeZeroPosUDServo();
    relativeZeroPosLRServo();

    mbedLED1 = mbedLED2 = mbedLED3 = mbedLED4 = 0;
    for (int i = 0; i < 2; i++) {
        mbedLED1 = !mbedLED1;
        mbedLED2 = !mbedLED2;
        mbedLED3 = !mbedLED3;
        mbedLED4 = !mbedLED4;
        wait(0.1);
    }
}

void lidarMapStartingPosAllServos() {
    mbedLED1 = mbedLED2 = mbedLED3 = mbedLED4 = 0;
    for (int i = 0; i < 2; i++) {
        mbedLED1 = !mbedLED1;
        wait(0.1);
        mbedLED1 = !mbedLED1;
        mbedLED2 = !mbedLED2;
        wait(0.1);
        mbedLED2 = !mbedLED2;
        mbedLED3 = !mbedLED3;
        wait(0.1);
        mbedLED3 = !mbedLED3;
        mbedLED4 = !mbedLED4;
        wait(0.1);
        mbedLED4 = !mbedLED4;
    }

    while (currentUDPos < lidarMapUDStartPos) {
        currentUDPos = currentUDPos + autoRotate;
        udServo.position(currentUDPos);
        wait(0.01);
    }
    while (currentLRPos > lidarMapLRStartPos) {
        currentLRPos = currentLRPos - autoRotate;
        lrServo.position(currentLRPos);
        wait(0.01);
    }
    currentUDPos = lidarMapUDStartPos;
    udServo.position(currentUDPos);
    currentLRPos = lidarMapLRStartPos;
    lrServo.position(currentLRPos);
}

void rotateUpVariable(float rotationDegrees) {
    currentUDPos = currentUDPos + rotationDegrees;
    udServo.position(currentUDPos);
    printServoPositions();
}

void rotateDownVariable(float rotationDegrees) {
    currentUDPos = currentUDPos - rotationDegrees;
    udServo.position(currentUDPos);
    printServoPositions();
}

void rotateLeftVariable(float rotationDegrees) {
    currentLRPos = currentLRPos - rotationDegrees;
    lrServo.position(currentLRPos);
    printServoPositions();
}

void rotateRightVariable(float rotationDegrees) {
    currentLRPos = currentLRPos + rotationDegrees;
    lrServo.position(currentLRPos);
    printServoPositions();
}

uint32_t getLIDARDistance() {
    status = board->sensor_centre->get_distance(&lidarDistance);
    if (status == VL53L0X_ERROR_NONE) {
        return lidarDistance - lidarDistanceOffset;
    }
    return -1;
}

void reportDistance() {
    status = board->sensor_centre->get_distance(&lidarDistance);
    if (status == VL53L0X_ERROR_NONE) {
        currentDistance = getLIDARDistance();
        float LRPos = currentLRPos - relativeZeroLRPos;
        float UDPos = currentUDPos - relativeZeroUDPos;
        // X, Y, Z (distance) //
        console.printf("A %.2f\n", LRPos);
        console.printf("B %.2f\n", UDPos);
        console.printf("C %u\n", currentDistance);
    }
}

void mapLIDARPoints() {
    // Clear the Console for Easy Data Reading on 3D Rendering Side //
    console.printf("CLEAR\n");

    // Sweep Top to Bottom //
    for (int i = 0; i < verticalLIDARPoints; i = i + lidarPointsStep) {
        if (i % 2 == 0) {
            // Sweep Left to Right //
            for (int j = 0; j < horizontalLIDARPoints; j = j + lidarPointsStep) {
                currentLRPos = currentLRPos + lidarPointsStep;
                lrServo.position(currentLRPos);
                reportDistance();
            }
        }   else {
            // Sweep Right to Left //
            for (int j = 0; j < horizontalLIDARPoints; j = j + lidarPointsStep) {
                currentLRPos = currentLRPos - lidarPointsStep;
                lrServo.position(currentLRPos);
                reportDistance();
            }
        }
        currentUDPos = currentUDPos - lidarPointsStep;
        udServo.position(currentUDPos);
        reportDistance();
    }
}




int main() {

    // Initialization Processes //
    zeroPosAllServos();
    relativeZeroPosAllServos();
    initializeLIDARSensor();
    
    // Bluetooth Controller Variables //
    char controllerChar = 0;
    char controllerHit = 0;
    
    // Main Bluetooth Controller Thread //
    while (true) {
        if (controller.getc() == '!') {
            if (controller.getc() == 'B') {
                controllerChar = controller.getc();
                controllerHit = controller.getc();
                switch (controllerChar) {
                    // 1 Button //
                    case '1':
                        if (controllerHit == '1') {
                            relativeZeroPosAllServos();
                            lidarMapStartingPosAllServos();
                            mapLIDARPoints();
                        }
                        break;
                    // 3 Button //
                    case '3':
                        relativeZeroPosAllServos();
                        break;
                    // 4 Button //
                    case '4':
                        zeroPosAllServos();
                        break;
                    // Up Arrow Button //
                    case '5':
                        if (controllerHit == '1') {
                            rotateUpVariable(variableRotate);
                            mbedLED1 = 1;
                        }
                        break;
                    // Down Arrow Button //
                    case '6':
                        if (controllerHit == '1') {
                            rotateDownVariable(variableRotate);
                            mbedLED2 = 1;
                        }
                        break;
                    // Left Arrow Button //
                    case '7':
                        if (controllerHit == '1') {
                            rotateLeftVariable(variableRotate);
                            mbedLED3 = 1;
                        }
                        break;
                    // Right Arrow Button //
                    case '8':
                        if (controllerHit == '1') {
                            rotateRightVariable(variableRotate);
                            mbedLED4 = 1;
                        }
                        break;
                }
            }
        }
    }
}

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

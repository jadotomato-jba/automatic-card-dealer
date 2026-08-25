# Automated Robotic Card Dealer
## Description
Simple robotic card dealer built off of a Raspberry Pi Zero 2 W and Arduino Nano. To deal cards, the stepper motor spins to move to different players, and a servo is used to flick a card from the bottom of the deck. Users select the number of cards and number of players on a display on the Pi.

## System Architecture
**Two Controllers:** Both a Raspberry Pi and Arduino Nano are used to divide labor between the two controllers. The Raspberry Pi handles higher level operations, including recieving user input and updating the live display. The Nano controls the actual movement of the two motors precisely and accurately.\
\
**Power Distribution:** All components are powered by a set of two battery backs in series that each hold 4 AA batteries for a total of 12V. One rail of the breadboard is used to supply 12V to the stepper motor, and a second rail supplies 5V to the Pi and Servo. A buck converter is used to step down from 12V to 5V. Finally, the Nano recieves power from the Pi via a Micro USB to USB-C data cable.\
\
**Communication Protocol:** Data is exchanged between the two controllers using UART protocol over the data cable. Each controller recieves confirmation that data was correctly recieved, and then that information is displayed on the Pi for the user to see.

## Tech Stack and Hardware Components
**Electronics**
+ Rasberry Pi Zero 2 W
+ Waveshare 1.44inch LCD HAT
+ Arduino Nano
+ LM2596 Step Down Module
+ Adafruit TMC2209 Stepper Motor Driver

**Motors**
+ NEMA 14 Bipolar Stepper Motor
+ SG90 Microservo

## Setup Guide
### Microcontroller Firmware
To flash the Arduino sketch, first clone the repository to your local machine. Then open the sketch in the Arduino IDE and plug in your Nano. In the tool menu, set the board and proccessor  to "Arduino Nano" and "ATmega328p (Old Bootloader)", respectively. Required libraries include the standard Arduino and Servo library, and the AccelStepper library by Michael McCauley. Download the AccelStepper library by opening the library menu, searching for AccelStepper, and downloading it. Finally, click the upload button to compile and upload the code to the Nano.

### Single-board Computer Software
Clone the repository to the Pi by opening the Raspberry pi terminal. Navigate to your home directory, and then clone the repositroy using `git clone https://github.com/jadotomato-jba/automatic-card-dealer.git` To set up the virtual environment for the Raspberry Pi, navigate to the software directory using `cd ~/automatic-card-dealer/software`. Create the virtual environment using `python3 -m venv venv`. Activate the environment by using `source venv/bin/activate`, and install dependencies by running `pip install -r requirements.txt`. Deactivate the environment using `deactivate`. 

### Service/Daemon Configuration
Copy `dealer_startup.service` to the system folder using `sudo cp ~/software/dealer_startup.service /etc/systemd/system/`. Reload the Systemd daemon with `sudo systemctl daemon-reload`. Enable the service on boot with `sudo systemctl1 enable dealer_startup.service`, and finally start the service imedietly using `sudo systemctl start dealer_startup.service`.

## Engineering Challenges

## Future Implementations
+ Custom PCB to upgrade from the breadboard
+ 3D printed housing to encase the entire device
+ Rechargeable batteries
+ Custom-built ejector arm for servo 
# Imports for screen
from luma.core.interface.serial import spi
from luma.lcd.device import st7735
from luma.core.render import canvas
from PIL import ImageFont

# Setting up GPIO
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

JOYSTICK_UP = 26
JOYSTICK_DOWN = 5
JOYSTICK_RIGHT = 19
JOYSTICK_LEFT = 6
JOYSTICK_CENTER = 13

GPIO.setup(JOYSTICK_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(JOYSTICK_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(JOYSTICK_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(JOYSTICK_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(JOYSTICK_CENTER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

import time

import serial


#States for selected items
DEAL_SELECTED = 0
PLAYERS_SELECTED = 1
CARDS_SELECTED = 2
MINIMUM_PLAYERS = 0
MAXIMUM_PLAYERS = 12
MINIMUM_CARDS = 0

#Color defintions
UNSELECTED_TEXT_COLOR = "black"
UNSELECTED_BACKGROUND = "white"
SELECTED_TEXT_COLOR = "white"
SELECTED_BACKGROUND = "#2626AB"


# Font sizes
TITLE_FONT_SIZE = 14
SUBTITLE_SIZE = 10
PRESS_TO_DEAL_SIZE = 12
UP_DOWN_SIZE = 30
NUMBER_FONT_SIZE = 20
MESSAGE_TEXT_SIZE = 12


def draw_menu(selected: int, players: int, cards: int):    
    with canvas(device) as draw:
        draw.rectangle([0,0,128,128], UNSELECTED_BACKGROUND)

        draw.text((64,10), "Card Dealer 3000", fill=UNSELECTED_TEXT_COLOR, anchor="mm", font_size=TITLE_FONT_SIZE)

        if players == 0:
            players = "OFF"
        
        if cards == 0:
            cards = "OFF"

        if selected == PLAYERS_SELECTED:
            draw.rectangle([5,18,59,110], fill=SELECTED_BACKGROUND)
            draw.text((32,25), "Players", fill=SELECTED_TEXT_COLOR, anchor="mm", font_size=SUBTITLE_SIZE)
            draw.text((32,40), "+", fill=SELECTED_TEXT_COLOR, anchor="mm", font_size=UP_DOWN_SIZE)
            draw.text((32,100), "-", fill=SELECTED_TEXT_COLOR, anchor="mm", font_size=UP_DOWN_SIZE)
            draw.text((32,70), str(players), fill=SELECTED_TEXT_COLOR, anchor="mm", font_size=NUMBER_FONT_SIZE)
        else:
            draw.text((32,25), "Players", fill=UNSELECTED_TEXT_COLOR, anchor="mm", font_size=SUBTITLE_SIZE)
            draw.text((32,40), "+", fill=UNSELECTED_TEXT_COLOR, anchor="mm", font_size=UP_DOWN_SIZE)
            draw.text((32,100), "-", fill=UNSELECTED_TEXT_COLOR, anchor="mm", font_size=UP_DOWN_SIZE)
            draw.text((32,70), str(players), fill=UNSELECTED_TEXT_COLOR, anchor="mm", font_size=NUMBER_FONT_SIZE)

        if selected == CARDS_SELECTED:
            draw.rectangle([69,18,123,110], fill=SELECTED_BACKGROUND)
            draw.text((96,25), "Cards", fill = SELECTED_TEXT_COLOR, anchor="mm", font_size=SUBTITLE_SIZE)
            draw.text((96,40),"+", fill=SELECTED_TEXT_COLOR, anchor="mm", font_size=UP_DOWN_SIZE)
            draw.text((96, 100), "-", fill=SELECTED_TEXT_COLOR, anchor="mm", font_size=UP_DOWN_SIZE)
            draw.text((96,70), str(cards), fill=SELECTED_TEXT_COLOR, anchor="mm", font_size=NUMBER_FONT_SIZE)
        else:
            draw.text((96,25), "Cards", fill = UNSELECTED_TEXT_COLOR, anchor="mm", font_size=SUBTITLE_SIZE)
            draw.text((96,40),"+", fill=UNSELECTED_TEXT_COLOR, anchor="mm", font_size=UP_DOWN_SIZE)
            draw.text((96, 100), "-", fill=UNSELECTED_TEXT_COLOR, anchor="mm", font_size=UP_DOWN_SIZE)
            draw.text((96,70), str(cards), fill=UNSELECTED_TEXT_COLOR, anchor="mm", font_size=NUMBER_FONT_SIZE)

        if selected == DEAL_SELECTED:
            draw.rectangle([1,113,126,127], fill=SELECTED_BACKGROUND)
            draw.text((64,120), "Press CENTER to deal", SELECTED_TEXT_COLOR, anchor="mm", font_size=PRESS_TO_DEAL_SIZE)
        else:
            draw.text((64,120), "Press CENTER to deal", UNSELECTED_TEXT_COLOR, anchor="mm", font_size=PRESS_TO_DEAL_SIZE)

def is_button_pushed(button: int):
    return GPIO.input(button) == GPIO.LOW

def send_deal_command(players: int, cards: int, port):
    message = f"DEAL: {players},{cards}\n"
    port.write(message.encode('utf-8'))
    print(f"Sent message ({message}) to arduino")

def draw_message(string: str):
    with canvas(device) as draw:
        draw.rectangle([0,0,128,128], fill=UNSELECTED_BACKGROUND)
        draw.multiline_text((64,64), string, fill="black", anchor="mm", font_size=MESSAGE_TEXT_SIZE)
            
def main():
    time.sleep(15)

    try: 
        global serial_spi, device, arduino
        serial_spi = spi(port=0, device=0, gpio_RST=27, gpio_DC=25, gpio_LIGHT=24)
        device = st7735(serial_spi, width=128,  height=128, bgr=True, h_offset=1, v_offset=2, rotate=1)
        arduino = serial.Serial(port="/dev/ttyUSB0",baudrate=9600, timeout=1)
        time.sleep(2)

        playerCount = MINIMUM_PLAYERS
        cardCount = MINIMUM_CARDS
        currSelect = PLAYERS_SELECTED
        draw_menu(currSelect, playerCount, cardCount)

        while True:
            if is_button_pushed(JOYSTICK_UP):
                print("Up")
                if currSelect == CARDS_SELECTED:
                    cardCount+=1
                elif currSelect == PLAYERS_SELECTED:
                    if playerCount == MAXIMUM_PLAYERS:
                        playerCount = MINIMUM_PLAYERS
                    else: 
                        playerCount += 1
                draw_menu(currSelect, playerCount, cardCount)

            if is_button_pushed(JOYSTICK_RIGHT):
                print("Right")
                if currSelect == PLAYERS_SELECTED:
                    currSelect = CARDS_SELECTED
                elif currSelect == CARDS_SELECTED:
                    currSelect = PLAYERS_SELECTED
                draw_menu(currSelect, playerCount, cardCount)

            if is_button_pushed(JOYSTICK_LEFT):
                print("Left")
                if currSelect == PLAYERS_SELECTED:
                    currSelect = CARDS_SELECTED
                elif currSelect == CARDS_SELECTED:
                    currSelect = PLAYERS_SELECTED
                draw_menu(currSelect, playerCount, cardCount)

            if is_button_pushed(JOYSTICK_DOWN):
                print("Down")
                if currSelect == CARDS_SELECTED:
                    if cardCount == MINIMUM_CARDS:
                        pass
                    else:
                        cardCount-=1
                elif currSelect == PLAYERS_SELECTED:
                    if playerCount == MINIMUM_PLAYERS:
                        playerCount = MAXIMUM_PLAYERS
                    else: 
                        playerCount -= 1
                draw_menu(currSelect, playerCount, cardCount)
                
            if is_button_pushed(JOYSTICK_CENTER):
                print("Center")

                #Check if should break
                if cardCount == 0 or playerCount == 0:
                    break

                # Selecting deal on screen
                old_selected = currSelect
                currSelect = DEAL_SELECTED
                draw_menu(currSelect,playerCount, cardCount)
                time.sleep(0.1)
                currSelect = old_selected
                draw_message("Dealing...\nPress center to cancel")

                # Sending stuffs
                message = f"DEAL {playerCount},{cardCount}\n"
                print(f"Sending: {message.strip()}")
                arduino.write(message.encode('utf-8'))
                print(f"Message sent!")
                while arduino.in_waiting == 0:
                    if is_button_pushed(JOYSTICK_CENTER):
                        arduino.write("STOP\n".encode('utf-8'))
                        print("Sent stop")
                        time.sleep(0.2)
                        break;
                
                result = arduino.readline().decode('utf-8').strip()

                print(result)

                if result == "DEALT":
                    draw_message("Success!\nAll cards dealt!")
                    time.sleep(2)
                elif result == "STOPPED":
                    draw_message("ERROR:\nDealing was finished early.")
                    time.sleep(2)
                draw_menu(currSelect, playerCount, cardCount);

            time.sleep(0.1)

    finally:

        draw_message("Shutting down") 
        time.sleep(2)
        
        # Closing things
        if 'device' in globals(): device.cleanup()
        GPIO.cleanup()
        if 'arduino' in globals() and arduino.is_open: arduino.close()


if __name__ == "__main__":
    main()
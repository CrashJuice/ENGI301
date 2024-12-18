# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Aquatrac smart water bottle
--------------------------------------------------------------------------
License:   
Copyright 2024 Juan Aizprua

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
This file provides an interface to a PWM controllered buzzer.
  - Ex:  https://www.adafruit.com/product/1536


Combines water level sensor, buzzer, button, and leds together to create a program that helps you keep track of how much water you are drinking and if you 
are on track for the amount you should be drinking in a day.

"""








from button import Button
from led import LED
from buzzer import Buzzer
from waterlevelsensor import get_water_level
import Adafruit_BBIO.GPIO as GPIO
import time
import threading 



RED_LED_PIN = "P2_4"  # Red LED pin
GREEN_LED_PIN = "P2_6"  # Green LED pin
BUTTON_PIN = "P2_2"  # Button pin
BUZZER_PIN = "P2_1"  # Buzzer pin

red_led = LED(pin=RED_LED_PIN, low_off=True)  # Red LED, off when LOW
green_led = LED(pin=GREEN_LED_PIN, low_off=True)  # Green LED, off when LOW

# Initialize Button
button = Button(pin=BUTTON_PIN, sleep_time=0.1, active_low=True)

buzzer = Buzzer(pin=BUZZER_PIN) 

# Target water goal
TARGET_WATER = 100  # Target water intake in %

previous_water_level = 0.0  # Stores the last recorded water level
water_drunk = 0.0           # Amount of water consumed in percentage
faillasttime = False  # Tracks if user failed previously
minsections = 0  # Tracks the number of 30-minute sections

# Global variable to check progress (shared between monitor and button press)
def check_user_progress():
    global minsections, water_drunk, faillasttime
    
    required_intake = (minsections / 32) * TARGET_WATER  # Calculate required intake for this section
    
    if water_drunk >= required_intake:
        green_led.on()  # On track
        red_led.off()   # Turn off red LED
        time.sleep(10)
        green_led.off()  # Turn off green LED after 10 seconds
    else:
        green_led.off()  # Turn off green LED
        red_led.on()     # Behind
        time.sleep(10)
        red_led.off()    # Turn off red LED after 10 seconds

        if faillasttime:
            buzzer.play(800, 2.0, False)  # Play buzzer for 2 seconds
            time.sleep(2.0)
            buzzer.play(980, 2.0, True)   # Play buzzer again for 2 seconds
            time.sleep(2.0)

        faillasttime = True  # Mark that they failed this time

def button_press_check():
    """ Check button press and call check_user_progress() if pressed """
    if button.is_pressed():
        print("Button Pressed!")
        check_user_progress()

def check_water_level():
    global previous_water_level, water_drunk
    
    current_water_level = get_water_level()  # Get the current water level
    
    if current_water_level is not None:
        # If the current water level is lower than the previous one, calculate the difference
        if current_water_level < previous_water_level:
            water_drunk += previous_water_level - current_water_level  # Add the difference to water drunk
            
        previous_water_level = current_water_level  # Update previous water level to current
        
        print(f"Current water level: {current_water_level:.2f}%")
        print(f"Water drank: {water_drunk:.2f}%")
    else:
        print("Failed to get water level.")

def monitor_water_level():
    global minsections, faillasttime, water_drunk 
    
    while True:
        check_water_level()  # Call the function to check the user's water intake
        
        # Calculate the target water intake for this 30-minute interval
        required_intake = (minsections / 32) * TARGET_WATER  # Target for the current 30-minute section
        
        if water_drunk >= required_intake:
            # The user is on track, reset faillasttime if they were previously behind
            if faillasttime:
                faillasttime = False  # Reset if user caught up
            print(f"You're on track! You've consumed {water_drunk:.2f}%.")
        else:
            # The user is behind on their goal
            red_led.on()  # Behind
            time.sleep(5)
            red_led.off()
            print(f"You're behind! You've consumed {water_drunk:.2f}%.")
            if faillasttime:
                buzzer.play(800, 2.0, False)      # Play buzzer for 1 second
                time.sleep(2.0)
                buzzer.play(980, 2.0, True)       # Play buzzer for 1 second
                time.sleep(2.0)   
            faillasttime = True  # Mark that they failed this time
        
        # Increment the 30-minute sections counter
        minsections += 1
        
        # Wait for 30 minutes before checking again
        time.sleep(30)  

def main():
    # Start monitor_water_level function in a separate thread
    monitor_thread = threading.Thread(target=monitor_water_level)
    monitor_thread.daemon = True  # Daemonize the thread so it exits when the program exits
    monitor_thread.start()
    
    while True:
        button_press_check()  # Continuously check for button press
        time.sleep(0.1)  # Small delay to prevent overloading the CPU

if __name__ == "__main__":
    main()

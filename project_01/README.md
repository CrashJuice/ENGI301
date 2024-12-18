# Smart Water Bottle Project

## Overview
The Smart Water Bottle project is designed to help users track their water intake and stay hydrated throughout the day. It monitors water levels, provides feedback via LEDs, and alerts users with a buzzer when they are falling behind their hydration goals. The system is controlled using a BeagleBone Black and incorporates various components to provide real-time feedback.

## Features
- **Water Level Monitoring**: Uses a water level sensor to measure the amount of water consumed.
- **Visual Feedback**:
  - **Green LED**: Indicates the user is on track with their hydration goal.
  - **Red LED**: Indicates the user is behind on their hydration goal.
- **Auditory Feedback**:
  - **Buzzer**: Alerts the user if they have fallen behind for consecutive intervals.
- **User Interaction**:
  - **Button**: Allows the user to check their progress manually.

## Components
- **PocketBeagle**: Microcontroller used to run the program and interface with hardware.
- **LEDs**: Visual indicators (Red and Green).
  - Red LED pin: `P2_4`
  - Green LED pin: `P2_6`
- **Button**: User input to manually check progress.
  - Button pin: `P2_2`
- **Buzzer**: Provides auditory feedback.
  - Buzzer pin: `P2_1`
- **Water Level Sensor**: Measures the percentage of water consumed.
- **Adafruit BBIO Library**: Used for GPIO control on the PocketBeagle.

## Functionality
1. **Monitoring Water Intake**:
   - The water level sensor tracks the current water level in the bottle.
   - If the water level decreases, the system calculates the amount of water consumed.

2. **Hydration Goals**:
   - The daily hydration goal is set to 100%.
   - The program divides the day into 30-minute intervals to track progress.
   - Users must consume a proportional amount of water in each interval to stay on track.

3. **Feedback**:
   - **On Track**: Green LED turns on for 10 seconds.
   - **Behind Goal**: Red LED turns on for 10 seconds.
     - If the user falls behind for two consecutive intervals, the buzzer sounds twice with a 2-second delay between sounds.

4. **User Interaction**:
   - Pressing the button checks the user's current progress and provides immediate feedback via LEDs.

## How It Works
1. **Initialization**:
   - The LEDs, button, buzzer, and water level sensor are initialized.
   - The program tracks the user's water consumption over time.

2. **Main Functions**:
   - **Monitor Water Level**: Continuously checks the water level and updates the amount of water consumed.
   - **Check User Progress**: Evaluates the user's current progress against the hydration goal and provides feedback via LEDs and buzzer.
   - **Button Press Check**: Allows the user to manually check their progress by pressing the button.

3. **Threading**:
   - The water level monitoring function runs in a separate thread to ensure real-time updates while the button press is checked in the main loop.

## Installation and Usage
1. **Hardware Setup**:
   - Connect the LEDs, button, buzzer, and water level sensor to the PocketBeagle using the specified pins.
2. **Software Requirements**:
   - Install Python 3.
   - Install the Adafruit BBIO library.
   ```bash
   pip3 install Adafruit_BBIO
   ```
3. **Run the Program**:
   - Save the project files (`smartwaterbottle.py`, `led.py`, `button.py`, `buzzer.py`, `waterlevelsensor.py`) in the same directory on the PocketBeagle.
   - Run the main script:
     ```bash
     python3 smartwaterbottle.py
     ```

## Code Structure
- **smartwaterbottle.py**: Main script that integrates all components and logic.
- **led.py**: Controls the LEDs.
- **button.py**: Handles button press events.
- **buzzer.py**: Controls the buzzer for auditory feedback.
- **waterlevelsensor.py**: Reads data from the water level sensor.

## Challenges Faced
- Debugging GPIO errors and ensuring proper initialization of components.
- Managing concurrency between the water level monitoring and button press detection.
- Ensuring real-time feedback with minimal delays.

## Future Improvements
- Add a display to show detailed water consumption statistics.
- Implement a mobile app integration for tracking progress remotely.
- Optimize the buzzer's sound patterns for better user experience.
- Use a rechargeable battery to make the system portable.

## Acknowledgments
- **Adafruit BBIO Library**: For GPIO control on the BeagleBone Black.
- **Rice University ENGI 301 Course**: For providing the resources and framework to develop this project.

---

This project was built by Juan Aizprua as part of an ENGI 301 assignment to explore embedded systems.

Hackster Link! 
https://www.hackster.io/juanaizprua89/smart-water-bottle-a7e579 

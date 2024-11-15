# ev3-Autonomous-Navigation
 Autonomous Navigation with Collision Avoidance 
# EV3 Autonomous Navigation 🚀

## Project Overview
This project involves an EV3 robot capable of autonomous navigation with collision avoidance using various sensors. The robot operates in a simulated environment where it must collect yellow cubes and deliver them to a designated green zone while avoiding blue cubes and walls. The project demonstrates the integration of perception and planning to achieve autonomous navigation.
![robot](https://github.com/user-attachments/assets/93b44d6d-84c0-482e-beac-c24d7f7943f6)
VIdeo Demo: https://youtu.be/IKBdK9oSI1g
## Objective
Navigate an enclosed environment to collect yellow cubes.
Transport the collected cubes to the green zone.
Avoid obstacles like blue cubes and walls.
Once all yellow cubes are collected, park in the red zone.

## Features
- Color Detection: Using a combination of camera and color sensors to detect objects and zones.
- Obstacle Avoidance: Ultrasonic sensor for detecting obstacles and planning detours.
- Autonomous Path Planning: Gyroscope and navigation algorithms to guide the robot.
- Mission Completion: Sequential task execution to collect cubes, avoid obstacles, and park.

## Project Structure
The project consists of the following files:

- mission.py: Main Python code containing navigation logic and sensor integration.
- world.wbt: World file used in the Webots simulation environment.
- robot.json: Configuration file for the EV3 robot.
These files are to be uploaded to Gears Simulator to execute the project.

Setup Instructions
## Prerequisites
- Python 3.x
- Webots (Robot simulator)
- Access to Gears
Running the Simulation
Clone the repository:
```bash
git clone https://github.com/yourusername/ev3-Autonomous-Navigation.git
```
Upload the files (mission.py, world.wbt, robot.json) to Gears.
Run the simulation on Gears to observe the robot's autonomous navigation.

## Technical Details
### Sensors Used
- Camera Sensor: Detects colored objects (yellow cubes, blue obstacles, purple start zone, green delivery zone, red parking zone).
Color Sensors:
- Downward-facing sensor for detecting surface colors.
- Front-facing sensor for detecting cubes and zones.
- Ultrasonic Sensor: Measures distances to prevent collisions.
- Gyro Sensor: Maintains orientation and helps in navigation.
How It Works
- Initialization: The robot starts in the purple zone and rotates to scan for yellow cubes using the camera sensor.
- Cube Collection: The robot uses the find_and_pick_yellow_cube() function to locate and collect yellow cubes.
- Obstacle Avoidance: Ultrasonic and color sensors help the robot avoid walls and blue cubes.
- Cube Delivery: After collecting a cube, the robot navigates to the green zone to drop it off.
Mission Completion: Once all yellow cubes are collected, the robot navigates to the red zone to park.
### Challenges & Solutions
- Navigation & Path Planning: Initially attempted GPS-based path planning, but switched to camera-based navigation due to limitations.
- Obstacle Avoidance: Implemented reactive navigation using ultrasonic sensors to adjust the robot's path dynamically.
### Future Improvements
Implement GPS-based navigation for more efficient path planning.
Optimize the robot's movement to avoid redundant trips to the starting position.
Enhance collision avoidance algorithms for smoother navigation.
## References
- Gears Wiki
- GearsBot Tutorial

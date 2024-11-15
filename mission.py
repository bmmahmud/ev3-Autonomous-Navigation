##### B M Ashik Mahmud
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MoveSteering
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4, INPUT_5, INPUT_6
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
from ev3dev2.sensor.virtual import GPSSensor, CameraSensor
import time
import math
from ev3dev2.sensor.lego import UltrasonicSensor

# Initialize motors and sensors
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)
color_sensor = ColorSensor(INPUT_1)
front_color_sensor = ColorSensor(INPUT_4)
gyro_sensor = GyroSensor(INPUT_2)
camera_sensor = CameraSensor(INPUT_3)
ultrasonic_sensor_front = UltrasonicSensor(INPUT_5)
# Initialize MagnetActuator
magnet_actuator = LargeMotor(OUTPUT_C)

# Constants
ROTATION_SPEED = 20
MOVE_SPEED = 50
SLOW_SPEED = 10
TARGET_X = 50  # Center of camera view

# Color constants
COLOR_YELLOW = 4
COLOR_GREEN = 3
COLOR_RED = 5
COLOR_BLACK = 1
COLOR_PURPLE = 2
COLOR_BLUE = 2
COLOR_WHITE = 6

# Function to rotate 
def rotate(degrees):
    gyro_sensor.reset()
    if degrees > 0:
        while gyro_sensor.angle < degrees:
            tank_drive.on(SpeedPercent(ROTATION_SPEED), SpeedPercent(-ROTATION_SPEED))
    else:
        while gyro_sensor.angle > degrees:
            tank_drive.on(SpeedPercent(-ROTATION_SPEED), SpeedPercent(ROTATION_SPEED))
    tank_drive.off()
# Function to find color with different HSV
def find_color_object(color_name, hsv_range):
    for _ in range(36):  # 36 * 10 degrees = 360 degrees
        camera_sensor.capture_image()
        blobs = camera_sensor.find_blobs(hsv_range, pixels_threshold=5)
        if blobs:
            return blobs[0]
        rotate(10)
    return None

# Move to target
def navigate_to_object(blob, color_name, hsv_range, target_color):
    steering_drive.on(0, SpeedPercent(MOVE_SPEED))  # Start moving forward

    while True:
        # CONTROL FLOOR DETECTION SPEEDS
        if color_sensor.color == target_color and target_color == COLOR_GREEN:
            tank_drive.on_for_seconds(SLOW_SPEED, SLOW_SPEED, 4.7)
            steering_drive.off()
            return True
        
        elif color_sensor.color == target_color and target_color == COLOR_PURPLE:
            tank_drive.on_for_seconds(SLOW_SPEED, SLOW_SPEED, 2)
            steering_drive.off()
            return True
        
        elif color_sensor.color == target_color and target_color == COLOR_RED:
            tank_drive.on_for_seconds(SLOW_SPEED, SLOW_SPEED, 4)
            steering_drive.off()
            return True

        if front_color_sensor.color != COLOR_BLACK:
            steering_drive.on(0, SpeedPercent(SLOW_SPEED))
        
        if front_color_sensor.color == COLOR_BLUE:
            # Pause the robot
            steering_drive.off()
            # Move backward for 0.5 seconds
            tank_drive.on_for_seconds(SpeedPercent(-20), SpeedPercent(-20), 1)
            # Rotate left by 10 degrees (counterclockwise)
            rotate(35)
        if front_color_sensor.color == COLOR_BLACK and ultrasonic_sensor_front.distance_centimeters <= 15:
            # Pause the robot
            steering_drive.off()
            # Move backward for 1 second (adjust the time based on how far you want to go back)
            tank_drive.on_for_seconds(SpeedPercent(-20), SpeedPercent(-20), 1)
            # Rotate left by 10 degrees (counterclockwise)
            rotate(-10)  # Rotate 10 degrees to the left
        
        if front_color_sensor.color == COLOR_YELLOW:
            steering_drive.off()
            rotate(180)
            pick_up_cube()
            tank_drive.on_for_seconds(-7, -7, 1.5)
            return True
        
        # Capture the image and detect objects
        camera_sensor.capture_image()
        blobs = camera_sensor.find_blobs(hsv_range, pixels_threshold=5)
        
        if not blobs:
            print(f"Lost sight of {color_name} object. Stopping.")
            steering_drive.off()
            return False
        
        largest_blob = blobs[0]
        centroid_x = largest_blob[1]
        
        # Calculate the deviation and adjust steering
        deviation_x = centroid_x - TARGET_X
        turn_rate = deviation_x * 0.5
        
        # Adjust speed based on detected color
        current_speed = SLOW_SPEED if color_sensor.color != COLOR_WHITE else MOVE_SPEED
        steering_drive.on(turn_rate, SpeedPercent(current_speed))
    
    print(f"Failed to reach {color_name} object")
    return False

def pick_up_cube():
    magnet_actuator.on(SpeedPercent(100))

def drop_cube():
    magnet_actuator.off()

def find_and_pick_yellow_cube():
    yellow_hsv = (40, 70, 70, 100, 70, 100)
    yellow_blob = find_color_object("yellow", yellow_hsv)
    if yellow_blob:
        if navigate_to_object(yellow_blob, "yellow", yellow_hsv, COLOR_YELLOW):
            return True
    print("Failed to find or reach yellow cube")
    return False

def return_to_purple():
    print("Returning to purple surface")
    while color_sensor.color != COLOR_PURPLE:
        # Simple strategy: move forward slowly while checking for purple
        tank_drive.on(MOVE_SPEED, MOVE_SPEED)
        time.sleep(0.1)
    print("Reached purple surface")
    tank_drive.on_for_seconds(SpeedPercent(SLOW_SPEED), SpeedPercent(SLOW_SPEED), 3)
    tank_drive.off()

def find_green_area():
    green_hsv = (90, 150, 40, 100, 10, 100)
    return find_color_object("green", green_hsv)

def find_red_area():
    red_hsv = (0, 30, 40, 100, 10, 100)
    return find_color_object("red", red_hsv)

def find_purple_area():
    purple_hsv = (250, 300, 40, 100, 20, 100)
    return find_color_object("purple", purple_hsv)

def drive_to_colored_area(color_name, color_code, hsv_range):
    print(f"Driving to {color_name} area")
    while True:
        blob = find_color_object(color_name, hsv_range)
        if blob:
            if navigate_to_object(blob, color_name, hsv_range, color_code):
                if color_code == COLOR_GREEN:
                    print("Rotating 100 degrees on green surface")
                    rotate(100)
                return True
        else:
            print(f"Lost sight of {color_name} area. Searching again.")
            rotate(45)  # Rotate a bit to search again

def move_forward_for_one_second():
    """Move the robot forward for 1 second at 50% speed."""
    
    # Set both motors to move forward at 50% speed
    tank_drive.on(SpeedPercent(50), SpeedPercent(50))  # Move forward at 50% speed
    
    # Wait for 1 second
    time.sleep(1)
    
    # Stop the motors after 1 second
    tank_drive.off()
    


def main():
    # Initial 90-degree left turn
    rotate(-80)
    
    duration_of_dropoff = 3
    duration_of_diveon = 3.5
    
    for i in range(3):  # Repeat 3 times for 3 yellow cubes
        if find_and_pick_yellow_cube():
            move_forward_for_one_second()
            drive_to_colored_area("purple", COLOR_PURPLE, (250, 300, 40, 100, 20, 100))
            
            #Facing to green
            rotate(-80)
            
            if drive_to_colored_area("green", COLOR_GREEN, (90, 150, 40, 100, 10, 100)):
                #ADJUSTMENT
                rotate(-5)
                
                # Move back a bit after BEFORE the cube
                tank_drive.on_for_seconds(-MOVE_SPEED, -MOVE_SPEED, duration_of_dropoff)
                duration_of_dropoff = max(0, duration_of_dropoff - 1)
                drop_cube()
                
                rotate(2)
                
                #Going end of the green area
                tank_drive.on_for_seconds(MOVE_SPEED, MOVE_SPEED, duration_of_diveon)
                duration_of_diveon = max(0, duration_of_diveon - 1)
                
                drive_to_colored_area("purple", COLOR_PURPLE, (250, 300, 40, 100, 20, 100))
            else:
                print("Failed green area")
        else:
            print(f"Failed to find or pick up {i+1}")
    
    # Drive to red area
    print("Attempting to drive to red area")
    drive_to_colored_area("red", COLOR_RED, (0, 30, 40, 100, 10, 100))
    
    print("Mission completed!")

if __name__ == "__main__":
    main()
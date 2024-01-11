from wpimath.geometry import Transform3d, Translation3d, Pose3d, Rotation3d
from wpimath.units import degreesToRadians

# Joystick IDs

# Motor Configs
LEFT_MOTOR_1_PORT = 1
LEFT_MOTOR_2_PORT = 2
RIGHT_MOTOR_1_PORT = 3
RIGHT_MOTOR_2_PORT = 4

# Pressure Sensor Constants

# Solenoids

# Button Mapping

# Drivetrain Config

# Vision Sensors
CAMERA_NAME = "photonvision"
ROBOT_TO_CAM = Transform3d(Pose3d(), Pose3d(Translation3d(0, 0, 1), Rotation3d(0, degreesToRadians(30), 0)))

# Electrical Subsystem
NOMINAL_VOLTAGE = 11.0
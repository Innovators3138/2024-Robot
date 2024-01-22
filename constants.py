from wpimath.geometry import Transform3d, Translation3d, Pose3d, Rotation3d
from wpimath.units import degreesToRadians, inchesToMeters

# Joystick IDs
DRIVER_JOYSTICK = 0
OPERATOR_CONTROLLER = 2
# Motor Configs
LEFT_MOTOR_1_PORT = 1
LEFT_MOTOR_2_PORT = 2
RIGHT_MOTOR_1_PORT = 3
RIGHT_MOTOR_2_PORT = 4

# Pressure Sensor Constants

# Solenoids

# Button Mapping

# Drivetrain Config
TRACK_WIDTH = inchesToMeters(23.0)
WHEEL_DIAMETER = inchesToMeters(4.0)
DRIVE_GEAR_RATIO = 12.0 / 62.0 * 22.0 / 30.0

# Arm Config
ARM_MOTOR_1_PORT = 5
ARM_MOTOR_2_PORT = 6

ARM_KP = 0.1  # Proportional coefficient
ARM_KI = 0.0  # Integral coefficient
ARM_KD = 0.0  # Derivative coefficient
ARM_KFF = 0.000015  # Feedforward coefficient
ARM_K_MAX_OUTPUT = 1.0  # Maximum output
ARM_K_MIN_OUTPUT = -1.0  # Minimum output

# Smart Motion coefficients
ARM_MAX_VEL = 2000  # Example maximum velocity
ARM_MAX_ACCEL = 1500  # Example maximum acceleration
ARM_MIN_VEL = 0  # Minimum velocity
ARM_ALLOWED_ERROR = 2  # Allowed closed loop error



# Vision Sensors
CAMERA_NAME = "photonvision"
ROBOT_TO_CAM = Transform3d(Pose3d(), Pose3d(Translation3d(0, 0, 1), Rotation3d(0, degreesToRadians(30), 0)))

# Electrical Subsystem
NOMINAL_VOLTAGE = 11.0
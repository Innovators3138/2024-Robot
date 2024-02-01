import math

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
ARM_MOTOR_1_PORT = 5
ARM_MOTOR_2_PORT = 6
INTAKE_MOTOR_PORT = 7
SHOOTER_MOTOR_PORT = 8

# Pressure Sensor Constants

# Solenoids

# Button Mapping

# Drivetrain Config
import math

# Drivebase Config
TRACK_WIDTH = inchesToMeters(23.0)
WHEEL_DIAMETER = inchesToMeters(4.0)
DRIVE_GEAR_RATIO = 12.0 / 62.0 * 22.0 / 30.0
DRIVE_ENCODER_CPR = 4096
NEO_FREE_SPEED = 5676  # RPM
DRIVE_MOTOR_FREE_SPEED = NEO_FREE_SPEED / 60  # RPS
DRIVE_WHEEL_FREE_SPEED = DRIVE_MOTOR_FREE_SPEED * WHEEL_DIAMETER * math.pi / DRIVE_GEAR_RATIO
DRIVE_KP = 0.04
DRIVE_KI = 0.0
DRIVE_KD = 0.0
DRIVE_FF = 1 / DRIVE_WHEEL_FREE_SPEED
DRIVE_MIN = -1.0
DRIVE_MAX = 1.0

# Arm Config
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

ARM_GROUND_PICKUP_POSITION = 1470  # +131.4 deg Relative to vertical
ARM_SHOOTER_POSITION = 439  # +39.3 deg Relative to vertical
ARM_FRONT_AMP_POSITION = 192  # +17.2 deg Relative to vertical
ARM_REAR_AMP_POSITION = -699  # -62.5 Relative to vertical

# Shooter Config
SHOOTER_KP = 0.25
SHOOTER_KI = 0.001
SHOOTER_KD = 20.0
SHOOTER_KF = 1023.0 / 7200.0
SHOOTER_IZ = 300
SHOOTER_PID_LOOP_IDX = 0
SHOOTER_SLOT_IDX = 0
SHOOTER_TIMEOUT_MS = 30
SHOOTER_PEAK_OUT = 1.0
SHOOTER_ENCODER_CPR = 4096

# Intake Config
INTAKE_KP = 0.25
INTAKE_KI = 0.001
INTAKE_KD = 20.0
INTAKE_KF = 1023.0 / 7200.0
INTAKE_IZ = 300
INTAKE_PID_LOOP_IDX = 0
INTAKE_SLOT_IDX = 0
INTAKE_TIMEOUT_MS = 30
INTAKE_PEAK_OUT = 1.0
INTAKE_ENCODER_CPR = 4096

# Vision Sensors
CAMERA_NAME = "photonvision"
ROBOT_TO_CAM = Transform3d(Pose3d(), Pose3d(Translation3d(0, 0, 1), Rotation3d(0, degreesToRadians(30), 0)))

# Electrical Subsystem
NOMINAL_VOLTAGE = 11.0

import math

from wpimath.geometry import Transform3d, Translation3d, Pose3d, Rotation3d
from wpimath.units import degreesToRadians, inchesToMeters

# Joystick IDs
STEERING_WHEEL = 0
THROTTLE = 1
OPERATOR_CONTROLLER = 2

# CAN Configs
LEFT_MOTOR_1_PORT = 1
LEFT_MOTOR_2_PORT = 2
RIGHT_MOTOR_1_PORT = 3
RIGHT_MOTOR_2_PORT = 4
ARM_MOTOR_1_PORT = 5
ARM_MOTOR_2_PORT = 6
INTAKE_MOTOR_PORT = 7
SHOOTER_MOTOR_PORT = 8
CANDLE_PORT = 9

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
ARM_REAR_KU = 1.0
ARM_REAR_TU = 1.0
ARM_REAR_KP = 1.0*ARM_REAR_KU  # Proportional coefficient
ARM_REAR_KI = 0.001  # Integral coefficient
ARM_REAR_KD = 2.0/40.0 * ARM_REAR_KU*ARM_REAR_TU  # Derivative coefficient
ARM_REAR_KFF = 0.0  # Feedforward coefficient
ARM_REAR_IZONE = 200

ARM_FRONT_KU = 0.6
ARM_FRONT_TU = 1.0
ARM_FRONT_KP = 1.0*ARM_FRONT_KU  # Proportional coefficient
ARM_FRONT_KI = 0.001  # Integral coefficient
ARM_FRONT_KD = 3.0/40.0 * ARM_FRONT_KU*ARM_REAR_TU  # Derivative coefficient
ARM_FRONT_KFF = 0.0  # Feedforward coefficient
ARM_K_MAX_OUTPUT = 1.0  # Maximum output
ARM_K_MIN_OUTPUT = -1.0  # Minimum output
ARM_FRONT_IZONE = 200


# Smart Motion coefficients
ARM_MAX_VEL = 1500  # Example maximum velocity
ARM_MAX_ACCEL = 1000  # Example maximum acceleration
ARM_MIN_VEL = 0  # Minimum velocity
ARM_ALLOWED_ERROR = 2  # Allowed closed loop error

ARM_GROUND_PICKUP_POSITION = 318
ARM_NEUTRAL_POSITION = 1530
#ARM_SHOOTER_POSITION = 1160  # +39.3 deg Relative to vertical
ARM_SHOOTER_POSITION = 1280
ARM_FRONT_AMP_POSITION = 1626  # +17.2 deg Relative to vertical
ARM_REAR_AMP_POSITION = 1383  # -62.5 Relative to vertical
ARM_DRIVING_POSITION = 1000

# intake Config
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
INTAKE_IN_RPM = 600
INTAKE_OUT_RPM = -300
INTAKE_FEED_RPM = 800

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

SHOOTER_SHOOT_RPM = 6000
SHOOTER_OUT_RPM = -INTAKE_OUT_RPM

#Retroreflective Sensor
RETROREFLECTIVE_THRESHOLD = 3.5



# Vision Sensors
CAMERA_NAME = "photonvision"
ROBOT_TO_CAM = Transform3d(Pose3d(), Pose3d(Translation3d(0, 0, 1), Rotation3d(0, degreesToRadians(30), 0)))

# Electrical Subsystem
NOMINAL_VOLTAGE = 11.0

# Autonomous Routines
SIMPLE_AUTO_DISTANCE = 2.0 # meters
AUTO_DURATION = 15 # seconds
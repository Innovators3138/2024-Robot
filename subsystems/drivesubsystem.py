import wpilib
import wpilib.drive
import commands2

from rev import CANSparkMax, SparkMaxAbsoluteEncoder

import constants
from utils import LazyCANSparkMax


class DriveSubsystem(commands2.Subsystem):
    left_motor_1 = LazyCANSparkMax(constants.LEFT_MOTOR_1_PORT)
    left_motor_2 = LazyCANSparkMax(constants.LEFT_MOTOR_2_PORT)
    right_motor_1 = LazyCANSparkMax(constants.RIGHT_MOTOR_1_PORT)
    right_motor_2 = LazyCANSparkMax(constants.RIGHT_MOTOR_2_PORT)
    left_encoder: SparkMaxAbsoluteEncoder
    right_encoder: SparkMaxAbsoluteEncoder

    def __init__(self) -> None:
        super().__init__()

        self.left_motor_2.follow(self.left_motor_1)
        self.right_motor_2.follow(self.right_motor_1)

        self.left_motor_1.setInverted(False)
        self.right_motor_1.setInverted(True)
        self.drive = wpilib.drive.DifferentialDrive(self.left_motor_1, self.right_motor_1)

        self.left_encoder = self.left_motor_1.getAbsoluteEncoder(SparkMaxAbsoluteEncoder.Type.kDutyCycle)
        self.right_encoder = self.right_motor_1.getAbsoluteEncoder(SparkMaxAbsoluteEncoder.Type.kDutyCycle)
        self.right_encoder.setInverted(False)
        self.right_encoder.setInverted(True)
import math
import time
import typing

from wpilib import (
    SPI,
    Field2d,
    SmartDashboard
)
from wpimath.controller import PIDController
from wpilib.drive import DifferentialDrive
from wpilib.interfaces import Gyro
import wpimath
from wpimath.estimator import DifferentialDrivePoseEstimator
from wpimath.geometry import (
    Pose2d,
    Rotation2d,
)
from wpimath.kinematics import (
    DifferentialDriveKinematics,
    DifferentialDriveWheelSpeeds,
    ChassisSpeeds,
)
import wpimath.units

import commands2

from rev import SparkMaxAlternateEncoder
from navx import AHRS

import constants
from utils import LazyCANSparkMax
from subsystems.visionsubsystem import VisionSubsystem


def initialize_navx(port: SPI.Port) -> Gyro:
    ahrs = AHRS(port)
    while not ahrs.isConnected():
        time.sleep(0.020)
    while ahrs.isCalibrating():
        time.sleep(0.020)
    return ahrs


class DriveSubsystem(commands2.Subsystem):

    left_motor_1: LazyCANSparkMax
    left_motor_2: LazyCANSparkMax
    right_motor_1: LazyCANSparkMax
    right_motor_2: LazyCANSparkMax
    left_encoder: SparkMaxAlternateEncoder
    right_encoder: SparkMaxAlternateEncoder
    current_pose2d: Pose2d
    vision_subsystem: VisionSubsystem
    pose_estimator: DifferentialDrivePoseEstimator
    kinematics: DifferentialDriveKinematics
    wheel_speeds: DifferentialDriveWheelSpeeds
    chassis_speeds: ChassisSpeeds


    def __init__(self) -> None:
        super().__init__()
        (self.left_motor_1, self.left_motor_2, self.right_motor_1, self.right_motor_2) = self.initialize_drive_motors()
        self.drive = DifferentialDrive(self.left_motor_1, self.right_motor_1)
        (self.left_encoder, self.right_encoder) = self.initialize_drive_encoders()
        self.gyro = initialize_navx(SPI.Port.kMXP)
        self.current_pose2d = Pose2d()

        self.vision_subsystem = VisionSubsystem(constants.ROBOT_TO_CAM)
        self.kinematics = DifferentialDriveKinematics(constants.TRACK_WIDTH)
        self.pose_estimator = DifferentialDrivePoseEstimator(
            self.kinematics,
            self.gyro.getRotation2d(),
            self.left_encoder.getPosition(),
            self.right_encoder.getPosition(),
            self.current_pose2d,
            (0.05, 0.05, wpimath.units.degreesToRadians(5.0)),
            (0.5, 0.5, wpimath.units.degreesToRadians(30.0))
        )
        self.reset_pose()

        self.field = Field2d()
        SmartDashboard.putData("Field", self.field)
        self.field.setRobotPose(self.pose_estimator.getEstimatedPosition())
        self.chassis_speeds = ChassisSpeeds(0,0,0)

    def arcade_drive(self, fwd: float, rot: float):
        self.drive.arcadeDrive(fwd, rot)

    def update(self):
        vision_pose = Pose2d()
        self.pose_estimator.update(self.gyro.getRotation2d(), self.left_encoder.getPosition(),
                                   self.right_encoder.getPosition())
        old_vision_pose = vision_pose
        vision_pose = self.vision_subsystem.best_candidate
        if vision_pose != old_vision_pose:
            self.pose_estimator.addVisionMeasurement(vision_pose, self.vision_subsystem.observation_time)
        self.wheel_speeds = DifferentialDriveWheelSpeeds(self.left_encoder.getVelocity()*self.left_encoder.getPositionConversionFactor(),
                                                         self.right_encoder.getVelocity()*self.right_encoder.getPositionConversionFactor())
        self.chassis_speeds = self.kinematics.toChassisSpeeds(self.wheel_speeds)


    def periodic(self) -> None:
        pass

    def initialize_drive_encoders(self) -> typing.Tuple[SparkMaxAlternateEncoder, SparkMaxAlternateEncoder]:
        left_encoder = self.left_motor_1.getAlternateEncoder(constants.DRIVE_ENCODER_CPR)
        right_encoder = self.right_motor_1.getAlternateEncoder(constants.DRIVE_ENCODER_CPR)
        left_encoder.setPosition(0)
        right_encoder.setPosition(0)
        right_encoder.setInverted(False)
        right_encoder.setInverted(True)
        left_encoder.setPositionConversionFactor(math.pi * constants.WHEEL_DIAMETER)
        right_encoder.setPositionConversionFactor(math.pi * constants.WHEEL_DIAMETER)
        return left_encoder, right_encoder

    def initialize_drive_motors(self) -> typing.Tuple[LazyCANSparkMax, LazyCANSparkMax, LazyCANSparkMax, LazyCANSparkMax]:
        left_motor_1 = LazyCANSparkMax(constants.LEFT_MOTOR_1_PORT)
        left_motor_2 = LazyCANSparkMax(constants.LEFT_MOTOR_2_PORT)
        right_motor_1 = LazyCANSparkMax(constants.RIGHT_MOTOR_1_PORT)
        right_motor_2 = LazyCANSparkMax(constants.RIGHT_MOTOR_2_PORT)
        left_motor_2.follow(left_motor_1, False)
        right_motor_2.follow(right_motor_1, False)
        left_motor_1.setInverted(False)
        right_motor_1.setInverted(True)
        return left_motor_1, left_motor_2, right_motor_1, right_motor_2

    def get_pose(self) -> Pose2d:
        return self.pose_estimator.getEstimatedPosition()

    def reset_pose(self) -> None:
        self.pose_estimator.resetPosition(self.gyro.getRotation2d(), self.left_encoder.getPosition(), self.right_encoder.getPosition(), Pose2d())
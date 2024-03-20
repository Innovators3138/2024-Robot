import math
import time
import typing

import wpilib
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

from pathplannerlib.auto import AutoBuilder
from pathplannerlib.config import ReplanningConfig, PIDConstants

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

        AutoBuilder.configureLTV(
            self.get_pose,
            self.reset_pose,
            self.get_robot_relative_speeds,
            self.drive_robot_relative,
            (0.0625, 0.125, 2.0),
            (1.0, 2.0),
            0.02,
            ReplanningConfig(),
            self.should_flip_path,
            self
        )

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
        SmartDashboard.putNumber("Left Encoder", self.left_encoder.getPosition())
        SmartDashboard.putNumber("Right Encoder", self.right_encoder.getPosition())

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
        left_motor_1.setInverted(True)
        right_motor_1.setInverted(False)
        return left_motor_1, left_motor_2, right_motor_1, right_motor_2

    def get_pose(self) -> Pose2d:
        return self.pose_estimator.getEstimatedPosition()

    def reset_pose(self, pose=Pose2d()) -> None:
        self.pose_estimator.resetPosition(self.gyro.getRotation2d(), self.left_encoder.getPosition(), self.right_encoder.getPosition(), pose)

    def get_robot_relative_speeds(self):
        return self.chassis_speeds

    def drive_robot_relative(self, speeds: ChassisSpeeds):
        self.wheel_speeds = self.kinematics.toWheelSpeeds(speeds)
        left_speed_fps = self.wheel_speeds.left_fps
        right_speed_fps = self.wheel_speeds.right_fps
        left_speed_rpm = left_speed_fps * 12 / (constants.WHEEL_DIAMETER * math.pi)
        right_speed_rpm = right_speed_fps * 12 / (constants.WHEEL_DIAMETER * math.pi)

        left_controller = self.left_motor_1.getPIDcontroller()
        right_controller = self.right_motor_1.getPIDcontroller()
        left_controller.setP(constants.DRIVE_KP)
        right_controller.setP(constants.DRIVE_KP)
        left_controller.setI(constants.DRIVE_KI)
        right_controller.setI(constants.DRIVE_KI)
        left_controller.setD(constants.DRIVE_KD)
        right_controller.setD(constants.DRIVE_KD)
        left_controller.setIZone(0.0)
        right_controller.setIZone(0.0)
        left_controller.setFF(constants.DRIVE_FF)
        right_controller.setFF(constants.DRIVE_FF)
        left_controller.setOutputRange(constants.DRIVE_MIN, constants.DRIVE_MAX)
        right_controller.setOutputRange(constants.DRIVE_MIN, constants.DRIVE_MAX)
        left_controller.setReference(left_speed_rpm, self.left_motor_1.ControlType.kVelocity)
        right_controller.setReference(right_speed_rpm, self.right_motor_1.ControlType.kVelocity)

    def should_flip_path(self) -> bool:
        return wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kRed
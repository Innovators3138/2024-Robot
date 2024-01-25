import math
import time
import typing

import wpilib
import wpilib.drive
import wpilib.interfaces
import wpimath
import wpimath.estimator
import wpimath.geometry
import wpimath.kinematics
import wpimath.units

import commands2

import rev
import navx

import constants
import utils
from subsystems.visionsubsystem import VisionSubsystem


def initialize_navx(port: wpilib.SPI.Port) -> wpilib.interfaces.Gyro:
    ahrs = navx.AHRS(port)
    while not ahrs.isConnected():
        time.sleep(0.020)
    while ahrs.isCalibrating():
        time.sleep(0.020)
    return ahrs


class DriveSubsystem(commands2.Subsystem):

    left_motor_1: utils.LazyCANSparkMax
    left_motor_2: utils.LazyCANSparkMax
    right_motor_1: utils.LazyCANSparkMax
    right_motor_2: utils.LazyCANSparkMax
    left_encoder: rev.SparkMaxAlternateEncoder
    right_encoder: rev.SparkMaxAlternateEncoder
    pose2d: wpimath.geometry.Pose2d
    vision_subsystem: VisionSubsystem
    pose_estimator: wpimath.estimator.DifferentialDrivePoseEstimator
    pose_estimator: wpimath.estimator.DifferentialDrivePoseEstimator
    kinematics: wpimath.kinematics.DifferentialDriveKinematics

    def __init__(self) -> None:
        super().__init__()
        (self.left_motor_1, self.left_motor_2, self.right_motor_1, self.right_motor_2) = self.initialize_drive_motors()
        self.drive = wpilib.drive.DifferentialDrive(self.left_motor_1, self.right_motor_1)
        (self.left_encoder, self.right_encoder) = self.initialize_drive_encoders()

        self.pose2d = wpimath.geometry.Pose2d()

        self.gyro = initialize_navx(wpilib.SPI.Port.kMXP)
        self.odometry = wpimath.kinematics.DifferentialDriveOdometry(self.gyro.getRotation2d(),
                                                                     self.left_encoder.getPosition(),
                                                                     self.right_encoder.getPosition(),
                                                                     self.pose2d)
        self.vision_subsystem = VisionSubsystem(constants.ROBOT_TO_CAM)
        self.kinematics = wpimath.kinematics.DifferentialDriveKinematics(constants.TRACK_WIDTH)
        self.pose_estimator = wpimath.estimator.DifferentialDrivePoseEstimator(
            self.kinematics,
            self.gyro.getRotation2d(),
            self.left_encoder.getPosition(),
            self.right_encoder.getPosition(),
            self.pose2d,
            (0.05, 0.05, wpimath.units.degreesToRadians(5.0)),
            (0.5, 0.5, wpimath.units.degreesToRadians(30.0))
        )

    def arcade_drive(self, fwd: float, rot: float):
        self.drive.arcadeDrive(fwd, rot)

    def update(self):
        vision_pose = wpimath.geometry.Pose2d()
        self.pose_estimator.update(self.gyro.getRotation2d(), self.left_encoder.getPosition(),
                                   self.right_encoder.getPosition())
        old_vision_pose = vision_pose
        vision_pose = self.vision_subsystem.best_candidate
        if vision_pose != old_vision_pose:
            self.pose_estimator.addVisionMeasurement(vision_pose, self.vision_subsystem.observation_time)

    def periodic(self) -> None:
        pass

    def initialize_drive_encoders(self) -> typing.Tuple[rev.SparkMaxRelativeEncoder, rev.SparkMaxRelativeEncoder]:
        left_encoder = self.left_motor_1.getAlternateEncoder(constants.DRIVE_ENCODER_CPR)
        right_encoder = self.right_motor_1.getAlternateEncoder(constants.DRIVE_ENCODER_CPR)
        left_encoder.setPosition(0)
        right_encoder.setPosition(0)
        right_encoder.setInverted(False)
        right_encoder.setInverted(True)
        left_encoder.setPositionConversionFactor(math.pi * constants.WHEEL_DIAMETER)
        right_encoder.setPositionConversionFactor(math.pi * constants.WHEEL_DIAMETER)
        return left_encoder, right_encoder

    def initialize_drive_motors(self) -> typing.Tuple[utils.LazyCANSparkMax, utils.LazyCANSparkMax, utils.LazyCANSparkMax, utils.LazyCANSparkMax]:
        left_motor_1 = utils.LazyCANSparkMax(constants.LEFT_MOTOR_1_PORT)
        left_motor_2 = utils.LazyCANSparkMax(constants.LEFT_MOTOR_2_PORT)
        right_motor_1 = utils.LazyCANSparkMax(constants.RIGHT_MOTOR_1_PORT)
        right_motor_2 = utils.LazyCANSparkMax(constants.RIGHT_MOTOR_2_PORT)
        left_motor_2.follow(left_motor_1, False)
        right_motor_2.follow(right_motor_1, False)
        left_motor_1.setInverted(False)
        right_motor_1.setInverted(True)
        return left_motor_1, left_motor_2, right_motor_1, right_motor_2

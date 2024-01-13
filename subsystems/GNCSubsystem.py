import time

from wpilib import AnalogEncoder, SPI
from wpilib.interfaces import Gyro
from wpimath.geometry import Pose2d, Pose3d
from wpimath.kinematics import DifferentialDriveKinematics, DifferentialDriveOdometry, DifferentialDriveWheelSpeeds, DifferentialDriveWheelPositions
from wpimath.estimator import DifferentialDrivePoseEstimator
from wpimath.units import degreesToRadians

from navx import AHRS

import constants
from .visionsubsystem import VisionSubsystem

class GNCSubsystem(object):

    pose2d: Pose2d
    vision_subsystem: VisionSubsystem
    pose_estimator: DifferentialDrivePoseEstimator
    kinematics: DifferentialDriveKinematics

    def __init__(self, drive, initial_pose: Pose2d):
        super().__init__()

        self.left_encoder = drive.left_encoder
        self.right_encoder = drive.right_encoder
        self.gyro = self.initialize_navx(SPI.Port.kMXP)
        self.odometry = DifferentialDriveOdometry(self.gyro.getRotation2d(),
                                                  self.left_encoder.getPosition(),
                                                  self.right_encoder.getPosition(),
                                                  initial_pose)
        self.vision_subsystem = VisionSubsystem(constants.ROBOT_TO_CAM)
        self.kinematics = DifferentialDriveKinematics(constants.TRACK_WIDTH)
        self.pose_estimator = DifferentialDrivePoseEstimator(
            self.kinematics,
            self.gyro.getRotation2d(),
            self.left_encoder.getPosition(),
            self.right_encoder.getPosition(),
            initial_pose,
            (0.05, 0.05, degreesToRadians(5.0)),
            (0.5, 0.5, degreesToRadians(30.0))
        )

    def update(self):
        vision_pose = Pose2d()
        self.pose_estimator.update(self.gyro.getRotation2d(), self.left_encoder.getPosition(), self.right_encoder.getPosition())
        old_vision_pose = vision_pose
        vision_pose = self.vision_subsystem.best_candidate
        if vision_pose != old_vision_pose:
            self.pose_estimator.addVisionMeasurement(vision_pose, self.vision_subsystem.observation_time)








    def initialize_navx(self, port: SPI.Port) -> Gyro:

        ahrs = AHRS(port)
        while not ahrs.isConnected():
            time.sleep(0.020)
        while not ahrs.isCalibrating():
            time.sleep(0.020)
        return ahrs



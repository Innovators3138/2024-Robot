import time

from wpilib import AnalogEncoder, SPI
from wpilib.interfaces import Gyro
from wpimath.geometry import Pose2d, Pose3d
from wpimath.kinematics import DifferentialDriveKinematics, DifferentialDriveOdometry, DifferentialDriveWheelSpeeds, DifferentialDriveWheelPositions

from navx import AHRS
from subsystems import VisionSubsystem
from subsystems import DriveSubsystem

class GNCSubsystem(object):

    pose3d: Pose3d
    pose2d: Pose2d

    def __init__(self, drive: DriveSubsystem, initial_pose: Pose2d):
        super().__init__()

        self.left_encoder = drive.left_encoder
        self.right_encoder = drive.right_encoder
        self.gyro = self.initialize_navx(SPI.Port.kMXP)
        self.odometry = DifferentialDriveOdometry(self.gyro.getRotation2d(),
                                                  self.left_encoder.getPosition(),
                                                  self.right_encoder.getPosition(),
                                                  initial_pose)

    def update(self):
        self.pose2d = self.odometry.update(self.gyro.getRotation2d(),
                                           self.left_encoder.getPosition(),
                                           self.right_encoder.getPosition())

    def initialize_navx(self, port: SPI.Port) -> Gyro:

        ahrs = AHRS(port)
        while not ahrs.isConnected():
            time.sleep(0.020)
        while not ahrs.isCalibrating():
            time.sleep(0.020)
        return ahrs



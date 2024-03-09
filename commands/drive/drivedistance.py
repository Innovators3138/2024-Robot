import math
from enum import Enum, auto

from wpimath.geometry import Transform2d
import commands2

import constants
from subsystems.drivesubsystem import DriveSubsystem

class DriveDistance(commands2.Command):
    class Axis(Enum):
        x = auto()
        y = auto()

    def __init__(self, distance: float, speed_factor: float, drive: DriveSubsystem) -> None:
        super().__init__(self)

        self.distance = distance
        self.speed_factor = speed_factor
        self.drive = drive
        self.addRequirements([self.drive])
        self.target_pose = None
        self.distance_to_target = None

    def initialize(self) -> None:
        current_pose = self.drive.pose_estimator.getEstimatedPosition()
        self.target_pose = current_pose + Transform2d(self.distance, 0, 0)
        self.update_distance_to_target()

    def execute(self) -> None:
        self.update_distance_to_target()
        self.drive.arcade_drive(self.speed_factor, 0)

    def end(self, interrupted: bool) -> bool:
        self.drive.arcade_drive(0,0)

    def isFinished(self) -> bool:
        return self.distance_to_target < constants.SIMPLE_AUTO_DISTANCE

    def update_distance_to_target(self) -> None:
        current_pose = self.drive.pose_estimator.getEstimatedPosition()
        self.distance_to_target = current_pose.translation().distance(
            self.target_pose.translation()
        )
import math
from enum import Enum, auto

import commands2

import constants
from subsystems.drivesubsystem import DriveSubsystem
from wpilib import Timer


class DriveDistance(commands2.Command):

    def __init__(self, drive_subsystem: DriveSubsystem):
        print("Init DriveDistance")
        super().__init__()

        self.drive_subsystem = drive_subsystem
        self.addRequirements(self.drive_subsystem)

    def isFinished(self) -> bool:
        return True


class DriveForward(DriveDistance):

    def __init__(self, drive_subsystem: DriveSubsystem) -> None:
        print("Init DriveForward")
        DriveDistance.__init__(self, drive_subsystem)

    def execute(self):
        print("Execute DriveForward")
        self.drive_subsystem.simple_drive_forward()


class StopDrive(DriveDistance):

    def __init__(self, drive_subsystem: DriveSubsystem) -> None:
        super().__init__(drive_subsystem)

    def execute(self):
        self.drive_subsystem.stop_drive()

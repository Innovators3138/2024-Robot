from commands2.command import Command
from wpimath.geometry import Pose2d

from wpilib import DataLogManager

from subsystems.drivesubsystem import DriveSubsystem

class ResetDrive(Command):
    def __init__(self, drive_subsystem, position: Pose2d = Pose2d()) -> None:
        super().__init__()
        self.drive_subsystem = drive_subsystem
        self.position = position
        self.addRequirements(self.drive_subsystem)

    def initialize(self) -> None:
        DataLogManager.log(f"Command: {self.getName()}")

    def execute(self) -> None:
        self.drive_subsystem.reset_pose()

    def end(self, interrupted: bool):
        DataLogManager.log("... DONE")

    def isFinished(self) -> bool:
        return True
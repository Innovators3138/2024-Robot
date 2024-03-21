from commands2 import ParallelCommandGroup, Command, SequentialCommandGroup, WaitCommand

from subsystems.drivesubsystem import DriveSubsystem
from commands.drive.simpledriveforward import DriveDistance, StopDrive
class SimpleDrive(SequentialCommandGroup):
    def __init__(self, drive_subsystem: DriveSubsystem):
        SequentialCommandGroup.__init__(
            self,
            DriveDistance(drive_subsystem),
            WaitCommand(3.0),
            StopDrive(drive_subsystem)
        )
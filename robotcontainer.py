import constants

from subsystems import DriveSubsystem

class RobotContainer(object):
    """Container for the robot
    
    """
    drive_subsystem: DriveSubsystem

    def __init__(self):
        # Do all subsystem inits here
        self.drive_subsystem = DriveSubsystem()

        self.configure_buttons()

    def configure_buttons(self):
        # link up the button actions with commands here
        pass

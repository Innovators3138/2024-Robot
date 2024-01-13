import constants
import commands2
from subsystems import DriveSubsystem

class RobotContainer(object):
    """Container for the robot
    
    """
    drive_subsystem: DriveSubsystem

    def __init__(self):
        # Do all subsystem inits here
        self.drive_subsystem = DriveSubsystem()

        self.configure_buttons()

        self.driver_controller = commands2.button.CommandJoystick(0)

        self.drive_subsystem.setDefaultCommand(
            commands2.cmd.run(
                lambda: self.drive_subsystem.arcadeDrive(
                    -self.driver_controller.getY(),
                    -self.driver_controller.getX()
                ),
                (self.drive_subsystem)
            )

        )

    def configure_buttons(self):
        # link up the button actions with commands here
        pass

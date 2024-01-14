from wpimath.geometry import Pose2d

import constants
import commands2

from subsystems import DriveSubsystem, GNCSubsystem

class RobotContainer(object):
    """Container for the robot
    
    """
    drive_subsystem: DriveSubsystem
    GNC_subsystem: GNCSubsystem

    def __init__(self):
        # Do all subsystem inits here
        self.drive_subsystem = DriveSubsystem()
        self.GNC_subsystem = GNCSubsystem(self.drive_subsystem, Pose2d())

        self.driver_controller = commands2.button.CommandJoystick(constants.DRIVER_JOYSTICK)
        self.operator_controller = commands2.button.CommandGenericHID(constants.OPERATOR_CONTROLLER)

        self.configure_buttons()

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

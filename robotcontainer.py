from commands2 import Subsystem
from wpimath.geometry import Pose2d
import wpilib

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


        wpilib.SmartDashboard.putNumberArray("Targets", [x.fiducialId for x in
                                                         self.drive_subsystem.vision_subsystem.camera.getLatestResult().targets])

        self.driver_controller = commands2.button.CommandJoystick(constants.DRIVER_JOYSTICK)
        # self.driver_steering_wheel = commands2.button.CommandJoystick(1)
        # self.operator_controller = commands2.button.CommandGenericHID(constants.OPERATOR_CONTROLLER)

        self.configure_buttons()

        self.drive_subsystem.setDefaultCommand(
            commands2.cmd.run(
                lambda: self.drive_subsystem.arcade_drive(
                    -1.0 * self.driver_controller.getY(),
                    -1.0 * self.driver_controller.getX(),
                ),
                self.drive_subsystem
            )

        )

    def configure_buttons(self):
        # link up the button actions with commands here
        pass

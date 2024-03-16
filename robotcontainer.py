import os
from commands2 import Subsystem
from wpimath.geometry import Pose2d
import wpilib

import constants
import commands2

from pathplannerlib.auto import PathPlannerAuto, NamedCommands

import subsystems.lightssubsystem
from subsystems import DriveSubsystem, ArmSubsystem, LightsSubsystem
from commands.drive import DriveDistance
from commands.arm.armposition import ArmPosition


class RobotContainer(object):
    """Container for the robot
    
    """
    drive_subsystem: DriveSubsystem
    arm_subsystem: ArmSubsystem
    lights_subsystem: LightsSubsystem

    def __init__(self):
        # Do all subsystem inits here
        #self.drive_subsystem = DriveSubsystem()
        self.arm_subsystem = ArmSubsystem()
        self.lights_subsystem = LightsSubsystem()

        self.lights_subsystem.change_animation(subsystems.lightssubsystem.AnimationTypes.SetAll)
        self.lights_subsystem.set_colors(subsystems.lightssubsystem.Colors.Blue)

        #wpilib.SmartDashboard.putNumberArray("Targets", [x.fiducialId for x in
        #                                                 self.drive_subsystem.vision_subsystem.camera.getLatestResult().targets])


        #self.driver_steering_wheel = commands2.button.CommandJoystick(constants.STEERING_WHEEL)
        #self.driver_throttle = commands2.button.CommandJoystick(constants.THROTTLE)
        self.operator_controller = commands2.button.CommandGenericHID(constants.OPERATOR_CONTROLLER)

        # self.simple_auto = commands2.SequentialCommandGroup(
        #     DriveDistance
        # )
        #
        # self.chooser = wpilib.SendableChooser()
        # paths_path = os.path.join(wpilib.getDeployDirectory(), "pathplanner")
        # for file in os.listdir(paths_path):
        #     relevant_name = file.split(".")[0]
        #     self.chooser.addOption(
        #         relevant_name,
        #         commands2.SequentialCommandGroup(
        #             commands2.ParallelCommandGroup(
        #                 commands2.waitcommand(14.9),
        #                 [
        #                 ]
        #             )
        #
        #         )
        #     )
        #
        # self.chooser.setDefaultOption("Simple Auto", self.simple_auto)
        #
        # wpilib.SmartDashboard.putData("Autonomous", self.chooser)

        self.configure_buttons()
        self.arm_subsystem.setDefaultCommand(ArmPosition(self.arm_subsystem, constants.ARM_NEUTRAL_POSITION))
        #self.drive_subsystem.setDefaultCommand(
        #    commands2.cmd.run(
        #        lambda: self.drive_subsystem.arcade_drive(
        #            -1.0 * self.driver_throttle.getRawAxis(2)*self.driver_throttle.getRawAxis(5),
        #            -1.0 * self.driver_steering_wheel.getRawAxis(0)
        #        ),
        #        self.drive_subsystem
        #    )
        #
        #)

        wpilib.DriverStation.silenceJoystickConnectionWarning(True)

    def configure_buttons(self):
        # link up the button actions with commands here
        self.operator_controller.button(1).onTrue(
            self.arm_subsystem.set_position(constants.ARM_FRONT_AMP_POSITION)
        )

    def get_autonomous_command(self):
        return PathPlannerAuto('Example Auto')

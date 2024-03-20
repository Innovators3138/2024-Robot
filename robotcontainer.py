import math
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
from commands.arm.armposition import *
from commands.intake.intakespeed import *
from commands.shooter.shooterspeed import *
from commands.intakecommands import GroundIntake, PrepareRearAmpScore, PrepareFrontAmpScore, RearAmpScore, FrontAmpScore
from commands.shootercommands import PrepareToShoot, Shoot
from commands.resetdrive import ResetDrive


class RobotContainer(object):
    """Container for the robot
    
    """
    drive_subsystem: DriveSubsystem
    arm_subsystem: ArmSubsystem
    intake_subsystem: IntakeSubsystem
    lights_subsystem: LightsSubsystem
    shooter_subsystem: ShooterSubsystem

    def __init__(self):
        # Do all subsystem inits here
        self.drive_subsystem = DriveSubsystem()
        self.arm_subsystem = ArmSubsystem()
        self.intake_subsystem = IntakeSubsystem()
        self.shooter_subsystem = ShooterSubsystem()
        self.lights_subsystem = LightsSubsystem()

        # self.lights_subsystem.change_animation(subsystems.lightssubsystem.AnimationTypes.SetAll)
        # self.lights_subsystem.set_colors(subsystems.lightssubsystem.Colors.Blue)

        # wpilib.SmartDashboard.putNumberArray("Targets", [x.fiducialId for x in
        #                                                 self.drive_subsystem.vision_subsystem.camera.getLatestResult().targets])

        self.driver_steering_wheel = commands2.button.CommandJoystick(constants.STEERING_WHEEL)
        self.driver_throttle = commands2.button.CommandJoystick(constants.THROTTLE)
        self.operator_controller = commands2.button.CommandGenericHID(constants.OPERATOR_CONTROLLER)

        self.simple_auto = commands2.SequentialCommandGroup(
            ResetDrive(self.drive_subsystem),
            DriveDistance(
                -1 * constants.SIMPLE_AUTO_DISTANCE * constants.WHEEL_DIAMETER * math.pi,
                0.2,
                self.drive_subsystem,
            ),
        )
        self.nothing_auto = commands2.WaitCommand(constants.AUTO_DURATION)

        self.chooser = wpilib.SendableChooser()

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

        self.chooser.addOption("Do Nothing Auto", self.nothing_auto)
        self.chooser.setDefaultOption("Simple Auto", self.simple_auto)
        wpilib.SmartDashboard.putData("Auto Choices", self.chooser)

        self.configure_buttons()
        # self.arm_subsystem.setDefaultCommand(ArmNeutralPosition(self.arm_subsystem))
        self.drive_subsystem.setDefaultCommand(
            commands2.cmd.run(
                lambda: self.drive_subsystem.arcade_drive(
                    -1.0 * (1.0-(self.driver_throttle.getRawAxis(2)+1)/2.0) * self.driver_throttle.getRawAxis(5),
                    -1.0 * self.driver_steering_wheel.getRawAxis(0)
                ),
                self.drive_subsystem
            )
        )

        wpilib.DriverStation.silenceJoystickConnectionWarning(True)

    def configure_buttons(self):
        # link up the button actions with commands here
        """
        self.operator_controller.button(1).whileTrue(
            ArmRearAmpPosition(self.arm_subsystem)
        )
        self.operator_controller.button(2).whileTrue(
            ArmNeutralPosition(self.arm_subsystem)
        )
        self.operator_controller.button(3).whileTrue(
            ArmRearPickupPosition(self.arm_subsystem)
        )
        """
        self.operator_controller.button(1).whileTrue(
            GroundIntake(self.arm_subsystem, self.intake_subsystem, self.shooter_subsystem)
        )
        self.operator_controller.button(2).whileTrue(
            PrepareToShoot(self.arm_subsystem, self.intake_subsystem, self.shooter_subsystem)
        )

        self.operator_controller.button(3).whileTrue(
            Shoot(self.arm_subsystem, self.intake_subsystem, self.shooter_subsystem)
        )

        self.operator_controller.button(4).whileTrue(
            PrepareFrontAmpScore(self.arm_subsystem, self.intake_subsystem, self.shooter_subsystem)
        )

        self.operator_controller.button(5).whileTrue(
            FrontAmpScore(self.arm_subsystem, self.intake_subsystem, self.shooter_subsystem)
        )

        self.operator_controller.button(6).whileTrue(
            PrepareRearAmpScore(self.arm_subsystem, self.intake_subsystem, self.shooter_subsystem)
        )

        self.operator_controller.button(7).whileTrue(
            RearAmpScore(self.arm_subsystem, self.intake_subsystem, self.shooter_subsystem)
        )

    def get_autonomous_command(self):
        return PathPlannerAuto('Example Auto')

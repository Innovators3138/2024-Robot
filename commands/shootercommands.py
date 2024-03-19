from commands2 import ParallelCommandGroup, Command, SequentialCommandGroup

from wpilib import SmartDashboard

from commands.intake.intakespeed import IntakeStop, IntakeFeed
from commands.arm.armposition import ArmShootPosition
from commands.shooter.shooterspeed import ShooterShoot, ShooterStop

import constants
from subsystems.armsubsystem import ArmSubsystem
from subsystems.intakesubsystem import IntakeSubsystem
from subsystems.shootersubsystem import ShooterSubsystem


class PrepareToShoot(ParallelCommandGroup):
    def __init__(self, arm_subsystem: ArmSubsystem, intake_subsystem: IntakeSubsystem,
                 shooter_subsystem: ShooterSubsystem):
        ParallelCommandGroup.__init__(
            self, ArmShootPosition(arm_subsystem), IntakeStop(intake_subsystem), ShooterShoot(shooter_subsystem)
        )


class Shoot(ParallelCommandGroup):
    def __init__(self, arm_subsystem: ArmSubsystem, intake_subsystem: IntakeSubsystem,
                 shooter_subsystem: ShooterSubsystem):
        ParallelCommandGroup.__init__(
            self, ArmShootPosition(arm_subsystem), IntakeFeed(intake_subsystem), ShooterShoot(shooter_subsystem)
        )

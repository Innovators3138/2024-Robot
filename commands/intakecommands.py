from commands2 import ParallelCommandGroup, Command, SequentialCommandGroup

from wpilib import SmartDashboard

from commands.intake.intakespeed import IntakeIn, IntakeStop, IntakeOutRear, IntakeOutFront
from commands.arm.armposition import ArmRearPickupPosition, ArmRearAmpPosition, ArmFrontAmpPosition
from commands.shooter.shooterspeed import ShooterStop, ShooterFeedFront

import constants
from subsystems.armsubsystem import ArmSubsystem
from subsystems.intakesubsystem import IntakeSubsystem
from subsystems.shootersubsystem import ShooterSubsystem

class GroundIntake(ParallelCommandGroup):
    def __init__(self, arm_subsystem: ArmSubsystem, intake_subsystem: IntakeSubsystem, shooter_subsystem: ShooterSubsystem):
        ParallelCommandGroup.__init__(
            self, ArmRearPickupPosition(arm_subsystem), IntakeIn(intake_subsystem), ShooterStop(shooter_subsystem)
        )

class PrepareRearAmpScore(ParallelCommandGroup):
    def __init__(self, arm_subsystem: ArmSubsystem, intake_subsystem: IntakeSubsystem, shooter_subsystem: ShooterSubsystem):
        ParallelCommandGroup.__init__(
            self, ArmRearAmpPosition(arm_subsystem), IntakeStop(intake_subsystem), ShooterStop(shooter_subsystem)
        )

class RearAmpScore(ParallelCommandGroup):
    def __init__(self, arm_subsystem: ArmSubsystem, intake_subsystem: IntakeSubsystem, shooter_subsystem: ShooterSubsystem):
        ParallelCommandGroup.__init__(
            self, ArmRearAmpPosition(arm_subsystem), IntakeOutRear(intake_subsystem), ShooterStop(shooter_subsystem)
        )

class PrepareFrontAmpScore(ParallelCommandGroup):
    def __init__(self, arm_subsystem: ArmSubsystem, intake_subsystem: IntakeSubsystem, shooter_subsystem: ShooterSubsystem):
        ParallelCommandGroup.__init__(
            self, ArmFrontAmpPosition(arm_subsystem), IntakeStop(intake_subsystem), ShooterStop(shooter_subsystem)
        )

class FrontAmpScore(ParallelCommandGroup):
    def __init__(self, arm_subsystem: ArmSubsystem, intake_subsystem: IntakeSubsystem, shooter_subsystem: ShooterSubsystem):
        ParallelCommandGroup.__init__(
            self, ArmFrontAmpPosition(arm_subsystem), IntakeOutFront(intake_subsystem), ShooterFeedFront(shooter_subsystem)
        )
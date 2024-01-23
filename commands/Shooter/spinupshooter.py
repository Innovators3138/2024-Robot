from commands2 import Command

import constants
from subsystems import ShooterSubsystem


class SpinUpShooter(Command):
    def __init__(self, shooter: ShooterSubsystem, rpm: float) -> None:
        super().__init__()
        self.shooter = shooter
        self.rpm = rpm
        self.addRequirements(shooter)

    def initialize(self) -> None:
        self.shooter.spin_up(self.rpm)



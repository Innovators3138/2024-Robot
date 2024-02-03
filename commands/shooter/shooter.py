from commands2 import Command

import constants
from subsystems import ShooterSubsystem

class SetShooterState(Command):
    def __init__(self, shooter: ShooterSubsystem) -> None:
        super().__init__(self)
        self.shooter = shooter
        self.addRequirements([self.shooter])

    def execute(self) -> None:
        pass

    def  isFinished(self) -> bool:
        return True

class SpinUpShooter(SetShooterState):
    def __init__(self, shooter: ShooterSubsystem, rpm: float) -> None:
        super().__init__(shooter)
        self.rpm = rpm

    def execute(self) -> None:
        self.shooter.set_shooter_spin_up(self.rpm)

class OpenLoopShooter(SetShooterState):
    def __init__(self, shooter: ShooterSubsystem, voltage: float) -> None:
        super().__init__(shooter)
        self.voltage = voltage

    def execute(self) -> None:
        self.shooter.set_shooter_open_loop(self.voltage)

class HoldShooter(SetShooterState):
    def __init__(self, shooter: ShooterSubsystem) -> None:
        super().__init__(shooter)

    def execute(self) -> None:
        self.shooter.set_shooter_hold()

class StopShooter(SetShooterState):
    def __init__(self, shooter: ShooterSubsystem) -> None:
        super().__init__(shooter)

    def execute(self) -> None:
        self.shooter.stop()



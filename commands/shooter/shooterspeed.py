from commands2 import Command

from subsystems import ShooterSubsystem


class SetShooterState(Command):
    def __init__(self, shooter_subsystem: ShooterSubsystem):
        super().__init__()
        self.shooter_subsystem = shooter_subsystem
        self.addRequirements(self.shooter_subsystem)

    def execute(self) -> None:
        raise NotImplementedError("Must be implemented by subclass")

    def isFinished(self) -> bool:
        return True


class ShooterShoot(SetShooterState):
    def __init__(self, shooter_subsystem: ShooterSubsystem) -> None:
        SetShooterState.__init__(self, shooter_subsystem)

    def execute(self) -> None:
        self.shooter_subsystem.set_shooter_shoot()


class ShooterFeedFront(SetShooterState):
    def __init__(self, shooter_subsystem: ShooterSubsystem) -> None:
        SetShooterState.__init__(self, shooter_subsystem)

    def execute(self) -> None:
        self.shooter_subsystem.set_shooter_feed_front()

class ShooterFeedRear(SetShooterState):
    def __init__(self, shooter_subsystem: ShooterSubsystem) -> None:
        SetShooterState.__init__(self, shooter_subsystem)

    def execute(self) -> None:
        self.shooter_subsystem.set_shooter_feed_rear()

class ShooterStop(SetShooterState):
    def __init__(self, shooter_subsystem: ShooterSubsystem) -> None:
        SetShooterState.__init__(self, shooter_subsystem)

    def execute(self) -> None:
        self.shooter_subsystem.set_shooter_stop()


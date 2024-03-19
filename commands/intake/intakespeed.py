from commands2 import Command

from subsystems import IntakeSubsystem


class SetIntakeState(Command):
    def __init__(self, intake_subsystem: IntakeSubsystem):
        super().__init__()
        self.intake_subsystem = intake_subsystem
        self.addRequirements(self.intake_subsystem)

    def execute(self) -> None:
        raise NotImplementedError("Must be implemented by subclass")

    def isFinished(self) -> bool:
        return True


class IntakeIn(SetIntakeState):
    def __init__(self, intake_subsystem: IntakeSubsystem) -> None:
        SetIntakeState.__init__(self, intake_subsystem)

    def execute(self) -> None:
        self.intake_subsystem.set_intake_in()


class IntakeOutRear(SetIntakeState):
    def __init__(self, intake_subsystem: IntakeSubsystem) -> None:
        SetIntakeState.__init__(self, intake_subsystem)

    def execute(self) -> None:
        self.intake_subsystem.set_intake_out_rear()


class IntakeOutFront(SetIntakeState):
    def __init__(self, intake_subsystem: IntakeSubsystem) -> None:
        SetIntakeState.__init__(self, intake_subsystem)

    def execute(self) -> None:
        self.intake_subsystem.set_intake_out_front()


class IntakeFeed(SetIntakeState):
    def __init__(self, intake_subsystem: IntakeSubsystem) -> None:
        SetIntakeState.__init__(self, intake_subsystem)

    def execute(self) -> None:
        self.intake_subsystem.set_intake_feed()


class IntakeStop(SetIntakeState):
    def __init__(self, intake_subsystem: IntakeSubsystem) -> None:
        SetIntakeState.__init__(self, intake_subsystem)

    def execute(self) -> None:
        self.intake_subsystem.set_intake_stop()

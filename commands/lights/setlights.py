from commands2 import Command

from subsystems import LightsSubsystem


class SetLightState(Command):
    def __init__(self, light_subsystem: LightsSubsystem):
        super().__init__()
        self.light_subsystem = light_subsystem
        self.addRequirements(self.light_subsystem)

    def execute(self) -> None:
        raise NotImplementedError("Must be implemented by subclass")

    def isFinished(self) -> bool:
        return True


class LightsPrematch(SetLightState):
    def __init__(self, light_subsystem: LightsSubsystem) -> None:
        SetLightState.__init__(self, light_subsystem)

    def execute(self) -> None:
        self.light_subsystem.set_lights_prematch()


class LightsNoNote(SetLightState):
    def __init__(self, light_subsystem: LightsSubsystem) -> None:
        SetLightState.__init__(self, light_subsystem)

    def execute(self) -> None:
        self.light_subsystem.set_lights_no_note()


class LightsNoteInIntake(SetLightState):
    def __init__(self, light_subsystem: LightsSubsystem) -> None:
        SetLightState.__init__(self, light_subsystem)

    def execute(self) -> None:
        self.light_subsystem.set_lights_note_in_intake()


class LightsShooterUpToSpeed(SetLightState):
    def __init__(self, light_subsystem: LightsSubsystem) -> None:
        SetLightState.__init__(self, light_subsystem)

    def execute(self) -> None:
        self.light_subsystem.set_lights_shooter_up_to_speed()


class LightsCelebrate(SetLightState):
    def __init__(self, light_subsystem: LightsSubsystem) -> None:
        SetLightState.__init__(self, light_subsystem)

    def execute(self) -> None:
        self.light_subsystem.set_lights_celebrate()


class LightsOff(SetLightState):
    def __init__(self, light_subsystem: LightsSubsystem) -> None:
        SetLightState.__init__(self, light_subsystem)

    def execute(self) -> None:
        self.light_subsystem.set_lights_off()

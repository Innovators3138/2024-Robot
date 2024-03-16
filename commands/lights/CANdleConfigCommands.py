from commands2 import InstantCommand
from subsystems import LightsSubsystem


class CANdleConfigCommands:
    class ConfigBrightness(InstantCommand):
        def __init__(self, lights_subsystem: LightsSubsystem, brightness_percent: float):
            super().__init__()
            lights_subsystem.config_brightness(brightness_percent)

            def runsWhenDisabled():
                return True

    class ConfigLosBehavior(InstantCommand):
        def __init(self, lights_subsystem: LightsSubsystem, disable_when_los: bool):
            super().__init__()
            lights_subsystem.config_los(disable_when_los)

            def runsWhenDisabled():
                return True

    class ConfigStatusLedBehavior(InstantCommand):
        def __init__(self, lights_subsystem: LightsSubsystem, disable_while: bool):
            super().__init__()
            lights_subsystem.config_status_led_behavior(disable_while)

            def runsWhenDisabled():
                return True

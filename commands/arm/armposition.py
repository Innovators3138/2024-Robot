from commands2 import Command

from subsystems import ArmSubsystem

import constants
class SetArmState(Command):
    def __init__(self, arm_subsystem: ArmSubsystem):
        super().__init__()
        self.arm_subsystem = arm_subsystem
        self.addRequirements(self.arm_subsystem)

    def execute(self) -> None:
        raise NotImplementedError("Must be implemented by subclass")

    def isFinished(self) -> bool:
        return True

class ArmRearPickupPosition(SetArmState):
    def __init__(self, arm_subsystem: ArmSubsystem) -> None:
        SetArmState.__init__(self, arm_subsystem)

    def execute(self) -> None:
        self.arm_subsystem.set_arm_ground_pickup_position()

class ArmRearAmpPosition(SetArmState):
    def __init__(self, arm_subsystem: ArmSubsystem) -> None:
        SetArmState.__init__(self, arm_subsystem)

    def execute(self) -> None:
        self.arm_subsystem.set_arm_rear_amp_position()

class ArmNeutralPosition(SetArmState):
    def __init__(self, arm_subsystem: ArmSubsystem) -> None:
        SetArmState.__init__(self, arm_subsystem)

    def execute(self) -> None:
        self.arm_subsystem.set_arm_neutral_position()

class ArmDrivingPosition(SetArmState):
    def __init__(self, arm_subsystem: ArmSubsystem) -> None:
        SetArmState.__init__(self, arm_subsystem)

    def execute(self) -> None:
        self.arm_subsystem.set_arm_driving_position()

class ArmShootPosition(SetArmState):
    def __init__(self, arm_subsystem: ArmSubsystem) -> None:
        SetArmState.__init__(self, arm_subsystem)

    def execute(self) -> None:
        self.arm_subsystem.set_arm_shoot_position()

class ArmFrontAmpPosition(SetArmState):
    def __init__(self, arm_subsystem: ArmSubsystem) -> None:
        SetArmState.__init__(self, arm_subsystem)

    def execute(self) -> None:
        self.arm_subsystem.set_arm_front_amp_position()
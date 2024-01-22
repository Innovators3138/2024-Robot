from commands2 import Command

from subsystems import ArmSubsystem

import constants
class ArmPosition(Command):

    arm_subsystem: ArmSubsystem
    def __init__(self, arm_subsystem: ArmSubsystem, position) -> None:
        super().__init__()
        self.arm = arm_subsystem
        self.position = position
        self.addRequirements([self.arm])

    def initialize(self):
        self.arm.set_position(self.position)

    def execute(self) -> None:
        pass

    def end(self):
        pass

    def isFinished(self) -> bool:
        return abs(self.arm.arm_motor_1.getSelectedSensorPosition(0) - self.position) < constants.ARM_ALLOWED_ERROR

    def interrupted(self):
        self.end()
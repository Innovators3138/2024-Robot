from commands2 import Command

from subsystems import ArmSubsystem

import constants
class ArmToFrontAmpPosition(Command):

    arm_subsystem: ArmSubsystem
    def __init__(self, arm_subsystem: ArmSubsystem) -> None:
        super().__init__()
        self.arm = arm_subsystem
        self.position = constants.ARM_FRONT_AMP_POSITION
        self.addRequirements(self.arm)

    def initialize(self):
        self.arm.set_position(self.position)

    def isFinished(self) -> bool:
        return abs(self.arm.arm_motor_1.getSelectedSensorPosition(0) - self.position) < constants.ARM_ALLOWED_ERROR

    def interrupted(self):
        self.end()
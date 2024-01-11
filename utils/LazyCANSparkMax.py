import rev
import constants

class LazyCANSparkMax(rev.CANSparkMax):
    def __init__(self, deviceId: int):
        super().__init__(deviceId, rev.CANSparkLowLevel.MotorType.kBrushless)

        self.restoreFactoryDefaults()
        self.clearFaults()
        self.enableVoltageCompensation(constants.NOMINAL_VOLTAGE)

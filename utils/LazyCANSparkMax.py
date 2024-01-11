from rev import CANSparkLowLevel, CANSparkMax
import constants


class LazyCANSparkMax(CANSparkMax):
    def __init__(self, deviceId: int):
        super().__init__(deviceId, CANSparkLowLevel.MotorType.kBrushless)

        self.restoreFactoryDefaults()
        self.clearFaults()
        self.enableVoltageCompensation(constants.NOMINAL_VOLTAGE)

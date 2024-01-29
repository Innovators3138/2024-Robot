from phoenix5 import WPI_TalonSRX, ControlMode, FeedbackDevice
import commands2
import constants
class ArmSubsystem(commands2.Subsystem):
    """

    """
    arm_motor_1: WPI_TalonSRX
    arm_motor_2: WPI_TalonSRX
    def __init__(self):
        super().__init__()
        self.arm_motor_1 = WPI_TalonSRX(constants.ARM_MOTOR_1_PORT)
        self.arm_motor_2 = WPI_TalonSRX(constants.ARM_MOTOR_2_PORT)
        self.arm_motor_1.clearStickyFaults()
        self.arm_motor_2.clearStickyFaults()
        self.arm_motor_1.configFactoryDefault()
        self.arm_motor_2.configFactoryDefault()
        self.arm_motor_2.follow(self.arm_motor_1)
        self.arm_motor_1.configSelectedFeedbackSensor(FeedbackDevice.CTRE_MagEncoder_Absolute)

        self.arm_motor_1.configNominalOutputForward(0, 30)
        self.arm_motor_1.configNominalOutputReverse(0, 30)
        self.arm_motor_1.configPeakOutputForward(1.0, 30)
        self.arm_motor_1.configPeakOutputReverse(-1.0, 30)

        self.arm_motor_1.selectProfileSlot(0, 0)
        self.arm_motor_1.config_kP(0, constants.ARM_KP, 30)
        self.arm_motor_1.config_kI(0, constants.ARM_KI, 30)
        self.arm_motor_1.config_kD(0, constants.ARM_KD, 30)
        self.arm_motor_1.config_kF(0, constants.ARM_KFF, 30)

        self.arm_motor_1.configMotionCruiseVelocity(constants.ARM_MAX_VEL, 30)
        self.arm_motor_1.configMotionAcceleration(constants.ARM_MAX_ACCEL)

    def set_position(self, position):
        self.arm_motor_1.set(ControlMode.MotionMagic, position)


    def stop(self):
        self.arm_motor_1.stopMotor()





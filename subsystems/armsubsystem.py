import wpilib
from enum import Enum, auto

from wpilib import SmartDashboard

import phoenix5
from phoenix5 import WPI_TalonSRX, ControlMode, FeedbackDevice
import commands2
import constants


class ArmSubsystem(commands2.Subsystem):
    """

    """
    arm_motor_1: WPI_TalonSRX
    arm_motor_2: WPI_TalonSRX
    arm_position: float

    class ArmState(Enum):
        GroundPickupPosition = auto()
        RearAmpPosition = auto()
        NeutralPosition = auto()
        DrivingPosition = auto()
        ShootPosition = auto()
        FrontAmpPosition = auto()

    def __init__(self):
        super().__init__()
        self.arm_motor_1 = WPI_TalonSRX(constants.ARM_MOTOR_1_PORT)
        self.arm_motor_2 = WPI_TalonSRX(constants.ARM_MOTOR_2_PORT)
        self.arm_motor_1.clearStickyFaults()
        self.arm_motor_2.clearStickyFaults()
        self.arm_motor_1.configFactoryDefault()
        self.arm_motor_2.configFactoryDefault()
        self.arm_motor_2.follow(self.arm_motor_1)
        self.arm_motor_1.setInverted(True)
        self.arm_motor_2.setInverted(phoenix5.InvertType.OpposeMaster)
        self.arm_motor_1.configSelectedFeedbackSensor(FeedbackDevice.CTRE_MagEncoder_Absolute, 0, 50)
        self.arm_motor_1.setSensorPhase(True)
        self.arm_motor_1.setNeutralMode(phoenix5.NeutralMode.Brake)
        self.arm_motor_2.setNeutralMode(phoenix5.NeutralMode.Brake)

        self.arm_motor_1.configNominalOutputForward(0, 30)
        self.arm_motor_1.configNominalOutputReverse(0, 30)
        self.arm_motor_1.configPeakOutputForward(1.0, 30)
        self.arm_motor_1.configPeakOutputReverse(-1.0, 30)
        self.arm_motor_1.configForwardSoftLimitThreshold(constants.ARM_FRONT_AMP_POSITION)
        self.arm_motor_1.configReverseSoftLimitThreshold(constants.ARM_GROUND_PICKUP_POSITION)
        self.arm_motor_1.configForwardSoftLimitEnable(True)
        self.arm_motor_1.configReverseSoftLimitThreshold(True)

        self.arm_motor_1.selectProfileSlot(0, 0)
        self.arm_motor_1.config_kP(0, constants.ARM_REAR_KP, 30)
        self.arm_motor_1.config_kI(0, constants.ARM_REAR_KI, 30)
        self.arm_motor_1.config_kD(0, constants.ARM_REAR_KD, 30)
        self.arm_motor_1.config_kF(0, constants.ARM_REAR_KFF, 30)

        self.arm_motor_1.configMotionCruiseVelocity(constants.ARM_MAX_VEL, 30)
        self.arm_motor_1.configMotionAcceleration(constants.ARM_MAX_ACCEL)

        self.arm_position = self.arm_motor_1.getSensorCollection().getPulseWidthPosition()
        self.state = self.ArmState.NeutralPosition
        SmartDashboard.putNumber("Arm Position:", constants.ARM_NEUTRAL_POSITION)

    def periodic(self) -> None:

        self.arm_position = self.arm_motor_1.getSensorCollection().getPulseWidthPosition()
        k_p = constants.ARM_REAR_KP
        k_i = constants.ARM_REAR_KI
        k_d = constants.ARM_REAR_KD
        k_ff = constants.ARM_REAR_KFF
        if self.arm_position > constants.ARM_NEUTRAL_POSITION:
            # We are on the front side
            k_p = constants.ARM_FRONT_KP
            k_i = constants.ARM_FRONT_KI
            k_d = constants.ARM_FRONT_KD
            k_ff = constants.ARM_FRONT_KFF

        SmartDashboard.putNumber("Arm k_p", k_p)
        SmartDashboard.putNumber("Arm k_i", k_i)
        SmartDashboard.putNumber("Arm k_d", k_d)
        SmartDashboard.putNumber("Arm k_ff", k_ff)

        self.arm_motor_1.config_kP(0, k_p, 30)
        self.arm_motor_1.config_kI(0, k_i, 30)
        self.arm_motor_1.config_kD(0, k_d, 30)
        self.arm_motor_1.config_kF(0, k_ff, 30)

        if self.state == self.ArmState.GroundPickupPosition:
            self.set_position(constants.ARM_GROUND_PICKUP_POSITION)
        elif self.state == self.ArmState.RearAmpPosition:
            self.set_position(constants.ARM_REAR_AMP_POSITION)
        elif self.state == self.ArmState.NeutralPosition:
            self.set_position(constants.ARM_NEUTRAL_POSITION)
        elif self.state == self.ArmState.DrivingPosition:
            self.set_position(constants.ARM_DRIVING_POSITION)
        elif self.state == self.ArmState.ShootPosition:
            self.set_position(constants.ARM_SHOOTER_POSITION)
        elif self.state == self.ArmState.FrontAmpPosition:
            self.set_position(constants.ARM_FRONT_AMP_POSITION)
        else:
            self.state = self.ArmState.NeutralPosition


        SmartDashboard.putString("Arm State", str(self.state))
        SmartDashboard.putNumber("Arm Position", self.arm_motor_1.getSelectedSensorPosition(0))

    def set_position(self, position) -> None:
        SmartDashboard.putNumber("Desired Arm Position", position)

        arb_ff = 0.0831 + 0.000186 * self.arm_position - 0.00000018 * self.arm_position ** 2
        self.arm_motor_1.set(phoenix5.ControlMode.MotionMagic, position, phoenix5.DemandType.ArbitraryFeedForward, arb_ff)

    def set_arm_ground_pickup_position(self):
        self.state = self.ArmState.GroundPickupPosition

    def set_arm_rear_amp_position(self):
        self.state = self.ArmState.RearAmpPosition

    def set_arm_neutral_position(self):
        self.state = self.ArmState.NeutralPosition

    def set_arm_driving_position(self):
        self.state = self.ArmState.DrivingPosition

    def set_arm_shoot_position(self):
        self.state = self.ArmState.ShootPosition

    def set_arm_front_amp_position(self):
        self.state = self.ArmState.FrontAmpPosition

    def stop(self):
        self.arm_motor_1.stopMotor()

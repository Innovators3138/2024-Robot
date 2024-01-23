import wpilib
import wpimath.controller
from commands2 import PIDSubsystem

import phoenix5

import constants
class ShooterSubsystem(PIDSubsystem):


    def __init__(self) -> None:
        super().__init__(
            wpimath.controller.PIDController(
                constants.SHOOTER_KP,
                constants.SHOOTER_KI,
                constants.SHOOTER_KD
            )
        )

        self.shooter_motor_1 = phoenix5.WPI_TalonSRX(constants.SHOOTER_MOTOR_1_PORT)
        self.shooter_motor_2 = phoenix5.WPI_TalonSRX(constants.SHOOTER_MOTOR_2_PORT)
        self.shooter_motor_1.configFactoryDefault()
        self.shooter_motor_2.configFactoryDefault()
        self.shooter_motor_1.enableVoltageCompensation(True)
        self.shooter_motor_2.enableVoltageCompensation(True)
        self.shooter_motor_1.clearStickyFaults()
        self.shooter_motor_2.clearStickyFaults()
        self.shooter_motor_1.setNeutralMode(phoenix5.NeutralMode.Coast)
        self.shooter_motor_2.setNeutralMode(phoenix5.NeutralMode.Coast)
        self.shooter_motor_2.follow(self.shooter_motor_1)

        self.shooter_motor_1.configSelectedFeedbackSensor(phoenix5.FeedbackDevice.CTRE_MagEncoder_Relative,
                                                          constants.SHOOTER_PID_LOOP_IDX,
                                                          constants.SHOOTER_TIMEOUT_MS)

        self.shooter_motor_1.setSensorPhase(True)

        self.shooter_motor_1.configNominalOutputForward(0.0, constants.SHOOTER_TIMEOUT_MS)
        self.shooter_motor_1.configNominalOutputReverse(0.0, constants.SHOOTER_TIMEOUT_MS)
        self.shooter_motor_1.configPeakOutputForward(1.0, constants.SHOOTER_TIMEOUT_MS)
        self.shooter_motor_1.configPeakOutputReverse(-1.0, constants.SHOOTER_TIMEOUT_MS)

        self.shooter_motor_1.config_kF(constants.SHOOTER_PID_LOOP_IDX, constants.SHOOTER_KF,
                                       constants.SHOOTER_TIMEOUT_MS)
        self.shooter_motor_1.config_kP(constants.SHOOTER_PID_LOOP_IDX, constants.SHOOTER_KP,
                                       constants.SHOOTER_TIMEOUT_MS)
        self.shooter_motor_1.config_kI(constants.SHOOTER_PID_LOOP_IDX, constants.SHOOTER_KI,
                                       constants.SHOOTER_TIMEOUT_MS)
        self.shooter_motor_1.config_kD(constants.SHOOTER_PID_LOOP_IDX, constants.SHOOTER_KD,
                                       constants.SHOOTER_TIMEOUT_MS)
    def spin_up(self, target_rpm) -> None:
        """

        """

        # Convert target_rpm to units/100 ms
        target_unitsper100ms = target_rpm * constants.SHOOTER_ENCODER_CPR / 600.0
        self.shooter_motor_1.set(phoenix5.ControlMode.Velocity, target_unitsper100ms)



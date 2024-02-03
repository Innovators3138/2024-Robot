from enum import Enum, auto

import wpilib
import wpimath.controller
from commands2 import PIDSubsystem

import phoenix5

import constants


class ShooterSubsystem(PIDSubsystem):
    class ShooterState(Enum):
        OpenLoop = auto()
        SpinUp = auto()
        Hold = auto()

    def __init__(self) -> None:
        super().__init__(
            wpimath.controller.PIDController(
                constants.SHOOTER_KP,
                constants.SHOOTER_KI,
                constants.SHOOTER_KD
            )
        )

        self.shooter_motor = phoenix5.WPI_TalonSRX(constants.SHOOTER_MOTOR_PORT)
        self.shooter_motor.configFactoryDefault()
        self.shooter_motor.enableVoltageCompensation(True)
        self.shooter_motor.clearStickyFaults()
        self.shooter_motor.setNeutralMode(phoenix5.NeutralMode.Coast)

        self.shooter_motor.configSelectedFeedbackSensor(phoenix5.FeedbackDevice.CTRE_MagEncoder_Relative,
                                                        constants.SHOOTER_PID_LOOP_IDX,
                                                        constants.SHOOTER_TIMEOUT_MS)

        self.shooter_motor.setSensorPhase(True)

        self.shooter_motor.configNominalOutputForward(0.0, constants.SHOOTER_TIMEOUT_MS)
        self.shooter_motor.configNominalOutputReverse(0.0, constants.SHOOTER_TIMEOUT_MS)
        self.shooter_motor.configPeakOutputForward(1.0, constants.SHOOTER_TIMEOUT_MS)
        self.shooter_motor.configPeakOutputReverse(-1.0, constants.SHOOTER_TIMEOUT_MS)

        self.shooter_motor.config_kF(constants.SHOOTER_PID_LOOP_IDX, constants.SHOOTER_KF,
                                     constants.SHOOTER_TIMEOUT_MS)
        self.shooter_motor.config_kP(constants.SHOOTER_PID_LOOP_IDX, constants.SHOOTER_KP,
                                     constants.SHOOTER_TIMEOUT_MS)
        self.shooter_motor.config_kI(constants.SHOOTER_PID_LOOP_IDX, constants.SHOOTER_KI,
                                     constants.SHOOTER_TIMEOUT_MS)
        self.shooter_motor.config_kD(constants.SHOOTER_PID_LOOP_IDX, constants.SHOOTER_KD,
                                     constants.SHOOTER_TIMEOUT_MS)

        self.target_rpm = 0.0

        self.state = ShooterSubsystem.ShooterState.Hold
        wpilib.SmartDashboard.putString("Shooter State", "Hold")

    def periodic(self) -> None:
        if self.state == self.ShooterState.SpinUp:
            wpilib.SmartDashboard.putString("Shooter State", "Spin Up")
            target_unitsper100ms = self.target_rpm * constants.SHOOTER_ENCODER_CPR / 600.0
            self.shooter_motor.set(phoenix5.ControlMode.Velocity, target_unitsper100ms)
        elif self.state == self.ShooterState.Hold:
            wpilib.SmartDashboard.putString("Shooter State", "Hold")
            self.set_shooter_hold()
        elif self.state == self.ShooterState.OpenLoop:
            wpilib.SmartDashboard.putString("Shooter State", "Open Loop")
            self.shooter_motor.configVoltageCompSaturation(constants.NOMINAL_VOLTAGE)
            self.shooter_motor.enableVoltageCompensation(True)
            self.shooter_motor.setVoltage(12.0)
        else:
            self.set_shooter_open_loop(0.0)
            self.target_rpm = 0.0

    def set_shooter_open_loop(self, voltage: float) -> None:
        self.state = self.ShooterState.OpenLoop

    def set_shooter_spin_up(self, target_rpm: float) -> None:
        self.state = self.ShooterState.SpinUp

    def set_shooter_hold(self) -> None:
        self.state = self.ShooterState.Hold

    def stop(self) -> None:
        self.state = self.ShooterState.OpenLoop

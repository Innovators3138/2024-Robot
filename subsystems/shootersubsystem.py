from enum import Enum, auto

from wpilib import SmartDashboard

import wpimath.controller
import commands2

import phoenix5

from utils.math import rpm_to_units, units_to_rpm
import constants


class ShooterSubsystem(commands2.Subsystem):
    shooter_motor: phoenix5.WPI_TalonSRX
    shooter_speed: float

    class ShooterState(Enum):
        Shoot = auto()
        FeedFront = auto()
        FeedRear = auto()
        Stop = auto()

    def __init__(self) -> None:
        super().__init__()

        self.shooter_motor = phoenix5.WPI_TalonSRX(constants.SHOOTER_MOTOR_PORT)
        self.shooter_motor.configFactoryDefault()
        self.shooter_motor.enableVoltageCompensation(True)
        self.shooter_motor.clearStickyFaults()
        self.shooter_motor.setNeutralMode(phoenix5.NeutralMode.Coast)

        self.shooter_motor.configSelectedFeedbackSensor(phoenix5.FeedbackDevice.CTRE_MagEncoder_Relative,
                                                        constants.SHOOTER_PID_LOOP_IDX,
                                                        constants.SHOOTER_TIMEOUT_MS)

        self.shooter_motor.setSensorPhase(True)
        self.shooter_motor.setInverted(True)

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

        self.shooter_speed = self.shooter_motor.getSensorCollection().getQuadratureVelocity()
        self.state = self.ShooterState.Stop
        SmartDashboard.putNumber("Shooter Speed:", 0)

    def periodic(self) -> None:
        if self.state == self.ShooterState.Shoot:
            self.set_speed(constants.SHOOTER_SHOOT_RPM)
        elif self.state == self.ShooterState.FeedFront:
            self.set_speed(constants.SHOOTER_OUT_RPM)
        elif self.state == self.ShooterState.FeedRear:
            self.set_speed(-constants.SHOOTER_OUT_RPM)
        elif self.state == self.ShooterState.Stop:
            self.set_speed(0)
        else:
            self.set_speed(0)

        self.shooter_speed = self.shooter_motor.getSensorCollection().getQuadratureVelocity()
        SmartDashboard.putString("Shooter State", str(self.state))
        SmartDashboard.putNumber("Shooter Speed:", units_to_rpm(self.shooter_speed, constants.INTAKE_ENCODER_CPR))

    def set_speed(self, target_rpm) -> None:
        self.shooter_motor.set(phoenix5.ControlMode.Velocity, rpm_to_units(target_rpm, constants.SHOOTER_ENCODER_CPR))

    def set_shooter_shoot(self) -> None:
        self.state = self.ShooterState.Shoot

    def set_shooter_feed_front(self) -> None:
        self.state = self.ShooterState.FeedFront

    def set_shooter_feed_rear(self) -> None:
        self.state = self.ShooterState.FeedRear

    def set_shooter_stop(self) -> None:
        self.state = self.ShooterState.Stop

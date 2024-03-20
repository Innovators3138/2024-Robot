from enum import Enum, auto

import commands2
from wpilib import SmartDashboard
from wpilib import AnalogInput
import phoenix5

from utils.math import rpm_to_units, units_to_rpm
import constants


class IntakeSubsystem(commands2.Subsystem):
    intake_motor: phoenix5.WPI_TalonSRX
    reflective_sensor: AnalogInput
    intake_speed: float

    class IntakeState(Enum):
        IntakeIn = auto()
        IntakeOutRear = auto()
        IntakeOutFront = auto()
        IntakeFeed = auto()
        IntakeStop = auto()

    def __init__(self):
        super().__init__()
        self.intake_motor = phoenix5.WPI_TalonSRX(constants.INTAKE_MOTOR_PORT)
        self.intake_motor.clearStickyFaults()
        self.intake_motor.configFactoryDefault()
        self.intake_motor.setNeutralMode(phoenix5.NeutralMode.Coast)
        self.intake_motor.configPeakCurrentLimit(30, 0)
        self.intake_motor.configPeakCurrentDuration(2000)
        self.intake_motor.configContinuousCurrentLimit(10, 0)


        self.intake_motor.configSelectedFeedbackSensor(phoenix5.FeedbackDevice.CTRE_MagEncoder_Relative,
                                                       constants.INTAKE_PID_LOOP_IDX,
                                                       constants.INTAKE_TIMEOUT_MS)
        self.intake_motor.setSensorPhase(False)
        self.intake_motor.setInverted(True)

        self.intake_motor.configNominalOutputForward(0.0, constants.INTAKE_TIMEOUT_MS)
        self.intake_motor.configNominalOutputReverse(0.0, constants.INTAKE_TIMEOUT_MS)
        self.intake_motor.configPeakOutputForward(1.0, constants.INTAKE_TIMEOUT_MS)
        self.intake_motor.configPeakOutputReverse(-1.0, constants.INTAKE_TIMEOUT_MS)

        self.intake_motor.config_kF(constants.INTAKE_PID_LOOP_IDX, constants.SHOOTER_KF,
                                    constants.INTAKE_TIMEOUT_MS)
        self.intake_motor.config_kP(constants.INTAKE_PID_LOOP_IDX, constants.SHOOTER_KP,
                                    constants.INTAKE_TIMEOUT_MS)
        self.intake_motor.config_kI(constants.INTAKE_PID_LOOP_IDX, constants.SHOOTER_KI,
                                    constants.INTAKE_TIMEOUT_MS)
        self.intake_motor.config_kD(constants.INTAKE_PID_LOOP_IDX, constants.SHOOTER_KD,
                                    constants.INTAKE_TIMEOUT_MS)

        self.reflective_sensor = AnalogInput(0)

        self.intake_speed = self.intake_motor.getSensorCollection().getQuadratureVelocity()
        self.state = self.IntakeState.IntakeStop
        SmartDashboard.putNumber("Intake Speed:", 0)
        SmartDashboard.putNumber("Reflective Sensor", self.reflective_sensor.getAverageValue())

    def periodic(self):
        if self.state == self.IntakeState.IntakeIn:
            self.set_speed(constants.INTAKE_IN_RPM)
            if self.reflective_tripped():
                self.set_speed(0)
        elif self.state == self.IntakeState.IntakeOutRear:
            self.set_speed(constants.INTAKE_OUT_RPM)
        elif self.state == self.IntakeState.IntakeOutFront:
            self.set_speed(-constants.INTAKE_OUT_RPM)
        elif self.state == self.IntakeState.IntakeFeed:
            self.set_speed(constants.SHOOTER_SHOOT_RPM)
        elif self.state == self.IntakeState.IntakeStop:
            self.set_speed(0)
        else:
            self.set_speed(0)

        self.intake_speed = self.intake_motor.getSensorCollection().getQuadratureVelocity()
        SmartDashboard.putString("Intake State", str(self.state))
        SmartDashboard.putNumber("Intake Speed:", units_to_rpm(self.intake_speed, constants.INTAKE_ENCODER_CPR))
        SmartDashboard.putNumber("Reflective Sensor", self.reflective_sensor.getAverageVoltage())

    def set_speed(self, target_rpm) -> None:
        """

        """
        self.intake_motor.set(phoenix5.ControlMode.Velocity, rpm_to_units(target_rpm, constants.INTAKE_ENCODER_CPR))

    def set_intake_in(self):
        self.state = self.IntakeState.IntakeIn

    def set_intake_out_rear(self):
        self.state = self.IntakeState.IntakeOutRear

    def set_intake_out_front(self):
        self.state = self.IntakeState.IntakeOutFront

    def set_intake_feed(self):
        self.state = self.IntakeState.IntakeFeed

    def set_intake_stop(self):
        self.state = self.IntakeState.IntakeStop

    def reflective_tripped(self) -> bool:
        return self.reflective_sensor.getAverageVoltage() > constants.RETROREFLECTIVE_THRESHOLD

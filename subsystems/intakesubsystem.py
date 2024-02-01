import commands2
import wpilib
import phoenix5
import constants


class IntakeSubsystem(commands2.Subsystem):
    intake_motor: phoenix5.WPI_TalonSRX

    def __init__(self):
        super().__init__()
        self.intake_motor = phoenix5.WPI_TalonSRX(constants.INTAKE_MOTOR_PORT)
        self.intake_motor.clearStickyFaults()
        self.intake_motor.configFactoryDefault()
        self.intake_motor.setNeutralMode(phoenix5.NeutralMode.Coast)

        self.intake_motor.configSelectedFeedbackSensor(phoenix5.FeedbackDevice.CTRE_MagEncoder_Relative,
                                                       constants.INTAKE_PID_LOOP_IDX,
                                                       constants.INTAKE_TIMEOUT_MS)
        self.intake_motor.setSensorPhase(True)

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

    def spin_up(self, target_rpm) -> None:
        """

        """

        # Convert target_rpm to units/100 ms
        target_unitsper100ms = target_rpm * constants.INTAKE_ENCODER_CPR / 600.0
        self.intake_motor.set(phoenix5.ControlMode.Velocity, target_unitsper100ms)

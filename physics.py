import typing

import wpilib
import wpilib.simulation

import constants

from pyfrc.physics.core import PhysicsInterface
from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units

if typing.TYPE_CHECKING:
    from robot import MyRobot



MOTOR_CFG_NEO = motor_cfgs.MotorModelConfig(
    "NEO",
    12 * units.volts,
    5820 * units.cpm,
    1.7 * units.amp,
    3.28 * units.N_m,
    181 * units.amp,
)

class PhysicsEngine:

    def __init__(self, physics_controller: PhysicsInterface, robot: "MyRobot"):
        self.physics_controller = physics_controller

        self.lf_motor = wpilib.simulation.PWMSim(robot.container.drive_subsystem.left_motor_1.getChannel())
        self.rf_motor = wpilib.simulation.PWMSim(robot.container.drive_subsystem.right_motor_1.getChannel())

        self.navx = wpilib.simulation.SimDeviceSim("navX-Sensor[0]")
        self.navx_yaw = self.navx.getDouble("Yaw")

        bumper_width = 3.25 * units.inch

        self.drivetrain = tankmodel.TankModel.theory(
            MOTOR_CFG_NEO,
            110 * units.lbs,
            1.0 / constants.DRIVE_GEAR_RATIO,
            2,
            24.0 * units.inch + bumper_width * 2,
            28.0 * units.inch + bumper_width * 2,
            4.0 * units.inch
        )

    def update_sim(self, now: float, tm_diff: float) -> None:
        lf_motor = self.lf_motor.getSpeed()
        rf_motor = self.rf_motor.getSpeed()

        transform = self.drivetrain.calculate(lf_motor, rf_motor, tm_diff)
        pose = self.physics_controller.move_robot(transform)
        self.navx_yaw.set(-pose.rotation().radians())

import typing

import wpilib
import wpilib.simulation


import constants

from pyfrc.physics.core import PhysicsInterface
from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units

if typing.TYPE_CHECKING:
    from robot import MyRobot

class PhysicsEngine:

    def __init__(self, physics_controller: PhysicsInterface, robot: "MyRobot"):
        self.physics_controller = physics_controller

        self.lf_motor = wpilib.simulation.PWMSim(robot.container.drive_subsystem.left_motor_1.getChannel())
        self.rf_motor = wpilib.simulation.PWMSim(robot.container.drive_subsystem.right_motor_1.getChannel())

        self.navx = wpilib.simulation.SimDeviceSim("navX-Sensor[0]")
        self.navx_yaw = self.navx.getDouble("Yaw")

        bumper_width = 3.25 * units.inch

        self.drivetrain = tankmodel.TankModel.theory(
            motor_cfgs.MOTOR_CFG_CIM,
            110 * units.lbs,
            10.71,
            2,
            24 * units.inch + bumper_width * 2,
            28 * units.inch + bumper_width * 2,
            6 * units.inch
        )

    def update_sim(self, now: float, tm_diff: float) -> None:
        lf_motor = self.lf_motor.getSpeed()
        rf_motor = self.rf_motor.getSpeed()

        transform = self.drivetrain.calculate(lf_motor, rf_motor, tm_diff)
        pose = self.physics_controller.move_robot(transform)
        self.navx_yaw.set(-pose.rotation().degrees())

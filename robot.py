import typing

import wpilib
import commands2
import robotcontainer


class MyRobot(commands2.TimedCommandRobot):
    """

    """
    container = None
    autonomous_command: typing.Optional[commands2.Command] = None

    def robotInit(self) -> None:
        """
        
        """
        self.container = robotcontainer.RobotContainer()

    def disabledInit(self) -> None:
        """"""

    def disabledPeriodic(self) -> None:
        """"""

    def autonomousInit(self) -> None:
        """
        """
        self.autonomous_command = self.container.get_autonomous_command()
        if self.autonomous_command:
            self.autonomous_command.schedule()

    def autonomousPeriodic(self) -> None:
        """
        """

    def teleopInit(self) -> None:
        """
        """

    def teleopPeriodic(self) -> None:
        """"""
        if wpilib.RobotBase.isSimulation():
            wpilib.DataLogManager.start()
        else:
            wpilib.DataLogManager.start("/u/logs")

        wpilib.DriverStation.startDataLog(wpilib.DataLogManager.getLog())

    def testInit(self) -> None:
        # Cancels all running commands at the start of test mode
        commands2.CommandScheduler.getInstance().cancelAll()


if __name__ == "__main__":
    wpilib.run(MyRobot)

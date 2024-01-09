import wpilib
import commands2

import robotcontainer


class MyRobot(commands2.TimedCommandRobot):
    """
    
    """

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

    def autonomousPeriodic(self) -> None:
        """
        """

    def teleopInit(self) -> None:
        """
        """

    def teleopPeriodic(self) -> None:
        """"""
        wpilib.DataLogManager.start()

        wpilib.DriverStation.startDataLog(wpilib.DataLogManager.getLog())

    def testInit(self) -> None:
        # Cancels all running commands at the start of test mode
        commands2.CommandScheduler.getInstance().cancelAll()


if __name__ == "__main__":
    wpilib.run(MyRobot)

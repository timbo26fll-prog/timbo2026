from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()


Der_Motor = Motor(Port.E, Direction.CLOCKWISE)
Izq_Motor= Motor(Port.A, Direction.COUNTERCLOCKWISE)

izq_mecansimo =Motor(Port.B)
Der_mecansimo =Motor(Port.F)

robot = DriveBase(Izq_Motor,Der_Motor, 56, 78)

robot.settings(straight_speed=720)
robot.use_gyro(True)

robot.straight(650)
robot.turn(30)
robot.straight(180)
robot.straight(-150)
robot.turn(-120)
robot.straight(-150)
robot.turn(-50)
robot.straight(750)



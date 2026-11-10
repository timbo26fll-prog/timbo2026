from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

sensorIzq = ColorSensor(Port.C)
sensorDer = ColorSensor(Port.D)
 # ---------- 1. Alinear contra la línea de arranque ----------
UMBRAL_IZQ = 30   # ajustá cada uno con tus lecturas sobre blanco/negro
UMBRAL_DER = 30   # (punto medio entre blanco y negro de ESE sensor)


def alinear_en_linea(velocidad=100, retroceso=40, timeout=4000):
    """Retrocede y avanza: cada rueda frena cuando SU sensor ve negro."""
    # 1) Retroceder y soltar el DriveBase para que no pelee con los motores
    robot.straight(-retroceso)
    robot.stop()

    izq_listo = False
    der_listo = False

    # 2) Avanzar con cada motor por separado
    motorIzquierda.run(velocidad)
    motorDerecha.run(velocidad)

    reloj = StopWatch()
    while not (izq_listo and der_listo):
        if not izq_listo and sensorIzq.reflection() < UMBRAL_IZQ:
            motorIzquierda.brake()
            izq_listo = True
        if not der_listo and sensorDer.reflection() < UMBRAL_DER:
            motorDerecha.brake()
            der_listo = True
        # Seguridad: si algo falla, no gira eternamente
        if reloj.time() > timeout:
            break
        wait(2)

    # 3) Frenar todo y dejar el DriveBase limpio
    motorIzquierda.stop()
    motorDerecha.stop()
    wait(100)
    robot.stop()
    robot.reset()  # desde acá: rumbo 0 = recto como quedó alineado 


hub = PrimeHub()

motorDerecha = Motor(Port.E, Direction.CLOCKWISE)
motorIzquierda= Motor(Port.A, Direction.COUNTERCLOCKWISE)

izq_mecansimo =Motor(Port.B)
Der_mecansimo =Motor(Port.F)

robot = DriveBase(motorIzquierda,motorDerecha, 56, 78)

robot.settings(straight_speed=720)
robot.use_gyro(True)

Der_mecansimo.run_angle(-600, -75)


robot.straight(860)
robot.turn(-90)

robot.settings(100,300)
robot.straight(240)

robot.settings(720,720)
robot.straight(-150)
robot.turn(-25)

robot.straight(400)
robot.turn(20)

alinear_en_linea()
robot.turn(45)

robot.straight(60)
robot.turn(-47)
robot.straight(40)
robot.straight(-20)

wait(300)




Der_mecansimo.run_angle(-320, -300)


robot.straight(-70)
robot.turn(55)
robot.straight(-800)






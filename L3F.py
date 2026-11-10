from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()


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


motorDerecha = Motor(Port.E, Direction.CLOCKWISE)
motorIzquierda= Motor(Port.A, Direction.COUNTERCLOCKWISE)

izq_mecansimo =Motor(Port.B)
Der_mecansimo =Motor(Port.F)

robot = DriveBase(motorIzquierda,motorDerecha, 56, 78)

robot.settings(straight_speed=720)
robot.use_gyro(True)



wait(1000)
izq_mecansimo.run_angle(300, -60)
wait(1000)
robot.straight(1650)
robot.straight(-130)
robot.turn(-90)



robot.straight(250)
robot.turn(100)
robot.straight(150)
robot.turn(42)

robot.settings(360,360,200,200)
alinear_en_linea()

Der_mecansimo.run_angle(300, 30)

robot.straight(70)

Der_mecansimo.run_angle(600,-30)
wait(500)


robot.straight(-45)
robot.turn(15)
izq_mecansimo.run_angle(300, 80)
robot.turn(-15)
robot.straight(-220)
robot.turn(-35)
robot.settings(960,960)
wait(100)
robot.straight(-130)
robot.settings(360,360,200,200)
robot.straight(210)


robot.turn(-65)
robot.straight(-500)
robot.turn(45)
robot.settings(720,720,360,360)
robot.straight(-1400)
robot.stop()





from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()

# Velocidades generales (mm/s, mm/s², grados/s, grados/s²).
VEL_RECTA = 350
ACEL_RECTA = 600
VEL_GIRO = 250
ACEL_GIRO = 800


# ---------- Calibración (medí cada sensor sobre negro y blanco) ----------
NEGRO_D = 10
BLANCO_D = 70
OBJETIVO = (NEGRO_D + BLANCO_D) // 2   # borde de la línea para el sensor D

NEGRO_I = 10
BLANCO_I = 70
UMBRAL_IZQ = (NEGRO_I + BLANCO_I) // 2
UMBRAL_DER = OBJETIVO


sensorIzq = ColorSensor(Port.C)
sensorDer = ColorSensor(Port.D)
# ---------- 2. Buscar la línea antes de seguirla ----------
def enganchar_linea(vel=60, giro_busqueda=10, vel_pivote=40, timeout=3000):
    """Busca la línea y deja el sensor D sobre el BORDE IZQUIERDO
    (la línea a la derecha del sensor), que es el borde de afuera
    de una curva a la derecha.
    Devuelve True si la encontró, False si se venció el tiempo."""
    reloj = StopWatch()

    # Fase A: avanzar despacio, en un arco leve a la derecha,
    # hasta tocar la línea con cualquier sensor
    encontrado = None
    while reloj.time() < timeout:
        if sensorDer.reflection() < UMBRAL_DER:
            encontrado = "der"
            break
        if sensorIzq.reflection() < UMBRAL_IZQ:
            encontrado = "izq"
            break
        skere.drive(vel, giro_busqueda)
        wait(5)

    if encontrado is None:
        skere.stop()
        return False

    # Si la tocó con D viniendo desde la izquierda, D ya está en el
    # borde izquierdo: no hay nada más que hacer.

    # Si la tocó con el IZQUIERDO, la línea está a la izquierda de D.
    # Pivotamos a la izquierda: D entra a la línea y sale por el
    # borde izquierdo. Ahí queda en el mismo lugar que el otro caso.
    if encontrado == "izq":
        skere.stop()
        reloj.reset()
        # entra a la línea
        while sensorDer.reflection() >= UMBRAL_DER and reloj.time() < 1500:
            skere.drive(0, -vel_pivote)
            wait(5)
        # la cruza hasta salir por el borde izquierdo
        while sensorDer.reflection() < UMBRAL_DER and reloj.time() < 2500:
            skere.drive(0, -vel_pivote)
            wait(5)
        skere.stop()

    return True


# ---------- 1. Alinear contra una línea ----------
def alinear_en_linea(velocidad=100, retroceso=40, timeout=4000):
    """Retrocede y avanza: cada rueda frena cuando SU sensor ve negro."""
    skere.straight(-retroceso)
    skere.stop()

    izq_listo = False
    der_listo = False
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
        if reloj.time() > timeout:
            break
        wait(2)

    motorIzquierda.stop()
    motorDerecha.stop()
    wait(100)
    skere.stop()
    skere.reset()  # rumbo 0 = recto como quedó alineado


# ---------- 3. Seguir la curva con el sensor D ----------
def seguir_curva_sensor_d(distancia_mm, vel_max=130, vel_min=60,
                          kp=0.8, kd=3, lado=1, giro_max=90,
                          entrada_mm=60, tiempo_perdido=600):
    """Sigue el borde de la línea con el sensor D.
    lado=1:  la línea queda a la DERECHA del sensor (borde izquierdo).
             Es el que usamos para la curva a la derecha.
    lado=-1: la línea queda a la IZQUIERDA del sensor.
    entrada_mm: los primeros mm va lento y corrigiendo suave,
                para no pasarse justo después de engancharse."""
    inicio = skere.distance()
    error_anterior = sensorDer.reflection() - OBJETIVO  # evita el tirón inicial
    reloj_perdido = StopWatch()

    while abs(skere.distance() - inicio) < distancia_mm:
        luz = sensorDer.reflection()          # una sola lectura por vuelta
        error = luz - OBJETIVO
        derivada = error - error_anterior
        giro = (kp * error + kd * derivada) * lado

        # Entrada suave: al principio limita el giro y la velocidad
        recorrido = abs(skere.distance() - inicio)
        if recorrido < entrada_mm:
            limite = giro_max * 0.5
            vel_tope = vel_min
        else:
            limite = giro_max
            vel_tope = vel_max
        giro = max(-limite, min(limite, giro))

        # Más lento cuanto más tiene que corregir (curva cerrada = más lento)
        velocidad = max(vel_min, vel_tope - abs(giro) * 0.6)
        skere.drive(velocidad, giro)
        error_anterior = error

        # Si ve blanco puro mucho tiempo, perdió la línea
        if luz < BLANCO_D - 5:
            reloj_perdido.reset()
        elif reloj_perdido.time() > tiempo_perdido:
            break
        wait(10)   # 10 ms: la derivada queda menos nerviosa

    skere.stop()




motorDerecha = Motor(Port.E, Direction.CLOCKWISE)
motorIzquierda= Motor(Port.A, Direction.COUNTERCLOCKWISE)

izq_mecansimo =Motor(Port.B)
Der_mecansimo =Motor(Port.F)

skere = DriveBase(motorIzquierda, motorDerecha, 56, 78)

skere.settings(VEL_RECTA, ACEL_RECTA, VEL_GIRO, ACEL_GIRO)
skere.settings(straight_speed=720)
skere.use_gyro(True)

Der_mecansimo.run_angle(300, 200)

UMBRAL_IZQ = 30   # ajustá cada uno con tus lecturas sobre blanco/negro
UMBRAL_DER = 30   # (punto medio entre blanco y negro de ESE sensor)


skere.straight(700)
alinear_en_linea()
skere.straight(400)
skere.turn(-90)
skere.straight(490)
skere.turn(85)


seguir_curva_sensor_d(500,300)
Der_mecansimo.run_angle(150,-250)
skere.straight(-100)
Der_mecansimo.run_angle(300,300)
skere.straight(-210)
skere.turn(88)
alinear_en_linea()
skere.straight(-35)
izq_mecansimo.run_angle(1200,1100)

skere.straight(10)






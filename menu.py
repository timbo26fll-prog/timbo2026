from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Button, Color, Port
from pybricks.tools import wait
import usys

# ================== MENÚ DE LANZAMIENTOS ==================
# Botón IZQUIERDA / DERECHA : cambiar de lanzamiento
# Botón CENTRO              : correr el lanzamiento que se ve en la pantalla
# Botón BLUETOOTH           : durante un lanzamiento lo corta y vuelve al menú;
#                             en el menú termina el programa.
#
# Cada lanzamiento sigue en su propio archivo (L1F.py, L2F.py, ...).
# En Pybricks Code tienen que estar todos los archivos cargados junto a menu.py.
# Si cambiás L3 o L4, editá su archivo: el menú no hace falta tocarlo.
# Para sacar o agregar un lanzamiento, editá esta lista.
LANZAMIENTOS = ["L1F", "L2F", "L3F", "L4F", "L5F"]

hub = PrimeHub()

# El botón del centro lo usamos para elegir, así que el de parar pasa a ser
# el de Bluetooth.
hub.system.set_stop_button(Button.BLUETOOTH)


def frenar_todo():
    """Deja quietos los 4 motores (por si un lanzamiento se cortó a la mitad)."""
    for puerto in (Port.A, Port.E, Port.B, Port.F):
        try:
            Motor(puerto).stop()
        except Exception:
            pass


def esperar_que_suelten():
    while hub.buttons.pressed():
        wait(10)


def correr(nombre):
    """Importa el archivo del lanzamiento; importarlo lo ejecuta."""
    # Si ya se importó antes, lo borramos para que vuelva a ejecutarse.
    if nombre in usys.modules:
        del usys.modules[nombre]
    __import__(nombre)


seleccion = 0

while True:
    hub.light.on(Color.GREEN)
    hub.display.char(LANZAMIENTOS[seleccion][1])  # muestra el número: "L3F" -> "3"

    esperar_que_suelten()
    botones = set()
    while not botones:
        botones = hub.buttons.pressed()
        wait(10)

    if Button.RIGHT in botones:
        seleccion = (seleccion + 1) % len(LANZAMIENTOS)
    elif Button.LEFT in botones:
        seleccion = (seleccion - 1) % len(LANZAMIENTOS)
    elif Button.CENTER in botones:
        esperar_que_suelten()   # arranca recién al soltar, con la mano fuera
        hub.light.on(Color.RED)
        wait(300)
        try:
            correr(LANZAMIENTOS[seleccion])
        except SystemExit:
            # Apretaron Bluetooth durante el lanzamiento: volvemos al menú.
            pass
        frenar_todo()
        hub.system.set_stop_button(Button.BLUETOOTH)
        # Pasa solo al lanzamiento siguiente, listo para la próxima salida.
        seleccion = (seleccion + 1) % len(LANZAMIENTOS)

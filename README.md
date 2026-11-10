# 🤖 Robototh — FIRST LEGO League 2026

Programas del robot del equipo **Robototh**, de la Escuela Técnica de Bella Unión (Artigas, Uruguay), para la instancia final de FIRST LEGO League Challenge 2026.

**Equipo:** Timoteo Butierrez · Gonzalo Pérez · Mateo Cardozo · Arthur Alves

---

## Contenido

- [Qué hay en este repositorio](#qué-hay-en-este-repositorio)
- [El robot](#el-robot)
- [Por qué programamos con Pybricks](#por-qué-programamos-con-pybricks)
- [Estrategia del juego del robot](#estrategia-del-juego-del-robot)
- [Programas de este repositorio](#programas-de-este-repositorio)
- [Cómo probamos los lanzamientos](#cómo-probamos-los-lanzamientos)
- [Lo que aprendimos](#lo-que-aprendimos)

---

## Qué hay en este repositorio

```
.
├── L1F.py                              Lanzamiento 1
├── L2F.py                              Lanzamiento 2
├── L3F.py                              Lanzamiento 3
├── L4F.py                              Lanzamiento 4
├── L5F.py                              Lanzamiento 5
└── docs/
    └── Prueba de misiones Robototh.xlsx   Registro de las 21 pruebas de cada lanzamiento
```

- **`L1F.py` … `L5F.py`:** un programa de Pybricks por lanzamiento. La `F` es de *final*: son las versiones para la instancia final.
- **`docs/Prueba de misiones Robototh.xlsx`:** la planilla donde anotamos cada prueba. Tiene una hoja por lanzamiento (`l1` … `l5`) y una hoja `plantilla` vacía para copiar. Cada hoja registra 21 tiradas con si fue un éxito y cuántos puntos hizo, y calcula el porcentaje de éxito y la media de puntos. Los resultados están en [Cómo probamos los lanzamientos](#cómo-probamos-los-lanzamientos).

---

## El robot

Pasamos por tres versiones. Cada una salió de lo que vimos que fallaba en la pista.

| Versión | Etapa | Características |
|---|---|---|
| **El Facha** | Práctica | Estructura sencilla para experimentar con el movimiento, la estabilidad y la ubicación de los componentes |
| **Urutoth V1** | Etapa virtual | Cuadrado y modular, encaje rápido, doble salida para mecanismos (laterales y superiores). 17 × 15,1 × 6,5 cm |
| **Urutoth V2** | Instancia final | Más compacto, estable y sin rueda loca |

### Por qué hicimos Urutoth V2

Cuando confirmamos que en el evento presencial usaríamos la misma pista, evaluamos a Urutoth V1 y vimos que su diseño no nos dejaba hacer algunas misiones de forma eficiente. Por eso lo rediseñamos.

| Aspecto | Urutoth V1 | Urutoth V2 |
|---|---|---|
| Tamaño | Grande: no llegaba a algunas misiones | Compacto: llega a todas las misiones |
| Estabilidad | Con casco se inclinaba hacia adelante | Ya no tiene ese problema |
| Apoyo | Rueda loca: impedía Checkpoints | Sin rueda loca |
| Sensores | Más juntos | Más separados, funcionan mejor |
| Cableado | Menos ordenado | Más ordenado y ruedas ajustadas |

Todos los mecanismos se construyen sobre un mismo **casco base**, y cada casco está pensado según las capacidades y limitaciones de Urutoth y las condiciones de la pista.

### Componentes

- 1 SPIKE Prime Hub
- 2 motores de tracción y 2 motores para mecanismos
- 2 sensores de color
- 2 ruedas de 56 mm

### Puertos

Así están conectados según los programas (`L1F.py` … `L5F.py`):

| Puerto | Uso | Nombre en el código |
|---|---|---|
| A | Motor de tracción izquierdo (sentido antihorario) | `motorIzquierda` / `Izq_Motor` |
| E | Motor de tracción derecho (sentido horario) | `motorDerecha` / `Der_Motor` |
| B | Motor de mecanismo izquierdo | `izq_mecansimo` |
| F | Motor de mecanismo derecho | `Der_mecansimo` |
| C | Sensor de color izquierdo | `sensorIzq` |
| D | Sensor de color derecho | `sensorDer` |

La base de movimiento se configura en todos los programas como `DriveBase(izquierdo, derecho, 56, 78)`: ruedas de **56 mm** y **78 mm** entre ruedas, con el giroscopio activado (`use_gyro(True)`).

---

## Por qué programamos con Pybricks

Buscábamos **más precisión** en los movimientos del robot. Pybricks nos permite programar en **Python** y resuelve el manejo del giroscopio:

- **DriveBase:** le indicamos el diámetro de las ruedas y la distancia entre ellas, y calcula solo los movimientos.
- **Giroscopio:** giros más exactos.
- **Sensores de color:** para seguir líneas y una rutina propia para alinearnos con la línea.

Los integrantes nuevos del equipo tuvieron que aprender Python para usarlo.

### Rutinas propias que usamos

Varias funciones se repiten entre los programas:

| Función | Qué hace | Se usa en |
|---|---|---|
| `alinear_en_linea()` | Retrocede un poco y avanza con cada rueda por separado; cada rueda frena cuando **su** sensor ve negro. Así el robot queda derecho sobre la línea y se reinicia el rumbo | L1, L2, L3, L5 |
| `enganchar_linea()` | Avanza en un arco suave buscando la línea y deja el sensor derecho sobre el borde, listo para seguirla. Si no la encuentra, devuelve `False` | L2 (también definida en L5) |
| `seguir_curva_sensor_d()` | Sigue el borde de la línea con el sensor derecho usando un control PD (proporcional + derivativo). Entra despacio, frena en las curvas cerradas y corta si pierde la línea | L2, L5 |
| `recto()` | Avanza una distancia con una velocidad dada y permite encadenar movimientos sin frenar | Definida en L2 |

Los umbrales de los sensores (`UMBRAL_IZQ`, `UMBRAL_DER`, `NEGRO_*`, `BLANCO_*`) se ajustan midiendo cada sensor sobre blanco y negro en la pista.

---

## Estrategia del juego del robot

### 1. Elegimos las misiones con una fórmula de costo-beneficio

Para decidir por qué misiones empezar, usamos esta fórmula:

```
Resultado = dificultad × distancia ÷ puntos
```

| Dato | Qué significa |
|---|---|
| Dificultad | Del 1 al 5, según cuánto nos costaba la misión |
| Distancia | Qué tan lejos está la misión |
| Puntos | Lo que otorga la misión |

**Cuanto menor es el resultado, más nos conviene la misión.**

| Misión | Cálculo | Resultado | Conclusión |
|---|---|---|---|
| Robótica | 1 × 64 ÷ 20 | 3,2 | Conviene |
| Prueba de precisión | 5 × 135 ÷ 20 | 33,75 | Conviene menos |

### 2. Agrupamos las misiones en 5 lanzamientos

| Lanzamiento | Qué hace | Puntos | Tiempo | Pts/s |
|---|---|---|---|---|
| **L1** | Dron y conectores; recoge 2 Minecraft | 60 | 19 s | 3,2 |
| **L2** | Cubo lejano y checkpoints | 35 | 27 s | 1,3 |
| **L3** | Cubo a la impresora y filamento; se lleva cubo y modelo 3D | 50 | 32 s | 1,6 |
| **L4** | Micro:bit, 2 cubos, modelo 3D y Robótica | 100 | 8 s | **12,5** |
| **L5** | Bloques de código, prueba de fuerza y prueba de precisión | 95 | _por medir_ | — |

**Puntaje objetivo: 425 puntos**

- 340 puntos de lanzamientos
- 85 puntos extra (fichas de precisión e inspección)

### 3. Por qué ese orden

- **Empezamos con el dron** para llevarlo a la base y que no moleste, y hacemos conectores para ganar espacio en la pista.
- **Después vamos a lo más lejano** y volvemos dejando lo recolectado cerca de Robótica.
- **Al final hacemos las misiones más cercanas entre sí.** L4 es el lanzamiento que más rinde (12,5 puntos por segundo).

---

## Programas de este repositorio

Cada lanzamiento es un programa independiente.

| Archivo | Lanzamiento | Misiones | Cómo lo hace |
|---|---|---|---|
| [`L1F.py`](L1F.py) | L1 | Dron, conectores y Minecraft | Ajusta el mecanismo derecho, va recto hasta la zona, se alinea con `alinear_en_linea()`, acciona el mecanismo derecho y vuelve marcha atrás a la base |
| [`L2F.py`](L2F.py) | L2 | Cubo lejano y checkpoints | Recorrido largo hasta el círculo de arriba a la derecha, se alinea, busca la línea con `enganchar_linea()` y la sigue con `seguir_curva_sensor_d()`. Si no encuentra la línea, prende la luz del hub en rojo. No usa motores de mecanismo |
| [`L3F.py`](L3F.py) | L3 | Impresora, filamento, cubo y modelo 3D | Usa los dos mecanismos: el izquierdo para el cubo y el derecho en la impresora, después de alinearse con la línea. Vuelve marcha atrás a velocidad alta |
| [`L4F.py`](L4F.py) | L4 | Micro:bit, cubos, modelo 3D y Robótica | El más corto: solo rectas y giros, sin sensores ni mecanismos |
| [`L5F.py`](L5F.py) | L5 | Bloques de código, fuerza y precisión | Combina alineación y seguimiento de línea, y usa el mecanismo derecho y el izquierdo (este último a alta velocidad) para las misiones |

### Cómo correr un lanzamiento

1. Abrir [Pybricks Code](https://code.pybricks.com) en Chrome o Edge.
2. Conectar el SPIKE Prime Hub (con el firmware de Pybricks instalado).
3. Abrir el archivo del lanzamiento (`L1F.py` … `L5F.py`) y ejecutarlo.
4. Dejar el robot **quieto en Home** al arrancar, para que el giroscopio se calibre.

---

## Cómo probamos los lanzamientos

Repetimos **cada lanzamiento 21 veces**, para saber qué tan confiable es y no quedarnos con una sola prueba que salió bien. Los datos completos de cada tirada están en [`docs/Prueba de misiones Robototh.xlsx`](docs/Prueba%20de%20misiones%20Robototh.xlsx).

| Criterio | Qué cuenta como éxito |
|---|---|
| L1 a L4 | El robot vuelve a la base |
| L5 | El robot no rompe las misiones |

| Lanzamiento | Programa | Éxitos (de 21) | % de éxito | Promedio de puntos | Puntos esperados |
|---|---|---|---|---|---|
| L1 | `L1F.py` | 20 | 95 % | 63,3 | 60 |
| L2 | `L2F.py` | 19 | 90 % | 33,8 | 35 |
| L3 | `L3F.py` | 21 | 100 % | 31,9 | 50 |
| L4 | `L4F.py` | 21 | 100 % | 89,0 | 100 |
| L5 | `L5F.py` | _pendiente_ | _pendiente_ | _pendiente_ | 95 |

Lo que nos dicen los datos:

- **L4** es el más confiable y el que más suma: volvió a la base las 21 veces, con 100 puntos en 11 de ellas.
- **L3** siempre vuelve, pero el puntaje varía mucho (entre 10 y 50 puntos): la parte de la impresora y el filamento todavía no es constante.
- **L2** casi siempre hace sus 35 puntos; falló en 2 tiradas.
- **L1** a veces supera lo esperado (hasta 80 puntos), pero tiene tiradas bajas (20–40).
- **L5** todavía no tiene pruebas cargadas en la planilla.

---

## Lo que aprendimos

- **Peso:** los engranajes dejaban de agarrar por mala distribución del peso. Sumamos ruedas o piezas similares para repartirlo.
- **Engranajes:** de chico a grande ganamos fuerza; de grande a chico, velocidad.
- **Diseño:** pasar a un robot más compacto y estable nos permitió llegar a todas las misiones.
- **Programación:** aprendimos Python, a usar el giroscopio y a seguir líneas.

---

Guardamos las versiones de los programas en Google Drive y las publicamos acá para que cualquiera pueda ver nuestro código.

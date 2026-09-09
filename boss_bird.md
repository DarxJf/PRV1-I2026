# 🎮 Especificaciones 🚀

## 🪶 1. División en Tres Aves (Split)

* Activación: Al presionar la barra espaciadora tras haber lanzado un ave, esta debe dividirse en tres aves independientes con el mismo comportamiento que el ave original.
* Vector de Trayectoria:
    * Una de las aves mantendrá la trayectoria central original.
    * Las otras dos se desviarán a partir del ángulo y la velocidad que llevaba el ave al momento de la división (una con desviación hacia arriba y otra hacia abajo).

## 🛑 2. Condición de Colisión

* La división solo se permite antes de cualquier impacto.
* Una vez que el ave colisione o golpee algún elemento de la escena, la habilidad quedará deshabilitada para ese lanzamiento.

## ⏱️ 3. Control del Marcador y Fin del Turno

* El marcador de lanzamiento no debe reiniciarse hasta que todas las aves en juego (resultado de la división) hayan reducido su velocidad casi por completo.
* El turno no se dará por terminado mientras alguna de las sub-aves se mantenga en movimiento significativo.

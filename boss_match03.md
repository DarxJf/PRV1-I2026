# 🎮 Especificaciones 🚀

## 🕹️ 1. Nueva Mecánica de Interacción (Drag & Drop)

Arrastrar en lugar de hacer clic: Cambia la forma de mover las baldosas. Ahora se deben arrastrar en vez de seleccionar con un clic.
Acople al apuntador: Mientras el jugador mantenga presionado el botón del mouse, la baldosa debe mantenerse unida al apuntador del mouse.
Liberación: Al soltar el clic del mouse, la baldosa se liberará y se moverá si el movimiento es válido.

## 🚫 2. Restricción de Movimientos

Solo se permite mover baldosas hacia posiciones donde se genere un coincidencia (match) válida.
🔄 3. Reordenamiento Automático del Tablero
Si en algún momento no existen coincidencias posibles en el tablero, este debe recrearse de forma automática.
Tras cada movimiento, el sistema debe verificar el tablero; si no hay coincidencias disponibles, el proceso de recreación se repetirá hasta garantizar al menos un movimiento válido.

## 💥 4. Implementación de Power-Ups

### 💣 Power-Up de Coincidencia de 4 Baldosa (Limpia-Líneas)

* Generación: Se crea al lograr una coincidencia de exactamente 4 baldosas.
* Ubicación: Aparece en la posición de la última baldosa movida (ej. si moviste de (1, 2) a (1, 3) para formar la combinación, se creará en (1, 3)).
Propiedades: Hereda el color de las baldosas combinadas. Puede moverse como cualquier baldosa normal (si se hace un match) o activarse directamente haciendo clic sobre él.
* Efecto: Al activarse o formar parte de una combinación, explota y destruye sus baldosas vecinas en horizontal y vertical como si fueran parte del match.

### ⚡ Power-Up de Coincidencia de 5+ Baldosas (Bomba de Color)

* Generación: Se crea al lograr una coincidencia de 5 o más baldosas.
Ubicación: Aparece en la posición de la última baldosa movida.
* Propiedades: Hereda el color de las baldosas combinadas. Puede moverse o activarse con un clic.
* Efecto: Al activarse o combinarse, explota y destruye todas las baldosas del mismo color presentes en todo el tablero.

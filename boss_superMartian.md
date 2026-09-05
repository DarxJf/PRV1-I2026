# 🎮 Especificaciones 🚀

## 🗺️ 1. Creación de Nuevo Nivel (Tiled)

Diseño libre: Crea un nuevo nivel utilizando Tiled. Tienes libertad para agregar los elementos que desees.

## 2. Bloque Especial y Llave

Comportamiento del bloque: Define un objeto completamente sólido que se pueda golpear desde abajo para generar una llave.
Animación de aparición: La llave debe spawnear en la misma posición del bloque y simular que nace de él (puedes utilizar técnicas de tweening).
Finalización del nivel: Al recoger la llave, el nivel debe finalizar y dar paso al siguiente. Usa efectos de fade-in y fade-out, o cualquier otra transición (como el cierre en círculo al estilo cartoon).

## 💥 3. Condición de Puntaje y Evento de Victoria

Puntaje objetivo: Define una meta de puntos que el jugador deba alcanzar para que aparezca el bloque de la llave.
Retroalimentación sonora: Debe sonar un efecto de audio indicando que el nivel ha sido completado.
Bloqueo del estado: Se debe detener el temporizador de la partida y el jugador no podrá recolectar más monedas.

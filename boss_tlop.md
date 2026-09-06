# 🎮 Especificaciones 🚀

## 1. Sistema de Cofre y Arco

* Interacción con el cofre: Crea un cofre que el jugador pueda abrir al pararse frente a él.
* Recompensa: El cofre otorgará un arco al abrirse. (Puedes usar la textura del cofre y la textura del arco proporcionadas).
* Generación aleatoria: El cofre debe aparecer de forma aleatoria en una habitación y solo puede generarse una única vez.
* Mecánica de disparo: Tras obtener el arco, el jugador podrá disparar flechas (utiliza la clase Projectile para gestionar esto).
Crea un método (por ejemplo, fire) en la clase Bow.
* Utiliza el patrón Factory para instanciar una flecha cada vez que se invoque dicho método.

## 👹 2. Habitación del Jefe y Comportamiento

* Acceso a la sala: Una vez obtenido el arco, debe existir una probabilidad de entrar a la sala del jefe al cruzar una puerta.
* Estructura de la habitación: La sala no contendrá criaturas, vasijas ni interruptores; solo al jefe en el lado opuesto a la puerta de entrada. Habrá únicamente una puerta (por la que se ingresa).
* Puntos de vida: El jefe debe tener una variable de puntos de vida (hitpoints) que disminuya cuando sufra daños.
Ataque y Patrón de Combate:
* Ataca disparando bolas de fuego lentas (como proyectiles) dirigidas a la posición en la que se encontraba el jugador al momento de ser generadas.
* Inmunidad: El jefe es inmune a los ataques con espada, pero vulnerable a las flechas.
* Mecánica de vulnerabilidad: Cuando una flecha impacta al jefe, este pierde su inmunidad durante unos segundos, permitiendo que el jugador le haga daño con la espada.
* Daño al jugador: Si una bola de fuego alcanza al jugador, este morirá. Si el jugador entra en contacto directo con el cuerpo del jefe, perderá un corazón completo.

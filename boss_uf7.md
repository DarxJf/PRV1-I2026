# 🎮 Especificaciones 🚀

## 1. Interfaz Gráfica de Usuario (GUI) y Curación

* Panel de estado del personaje: Diseña una GUI que muestre la información de cada integrante del equipo dentro de su propio recuadro (nivel, puntos de experiencia, vida/HP, nivel de magia, etc.).
* Visualización de acciones: Muestra las acciones de cada jugador aplicando cierta transparencia (alpha value), con excepción de las acciones de curación.
* Curación individual: Al seleccionar la acción de curar, debe permitir elegir al objetivo a curar (de la misma forma que en el estado de batalla).
* Curación global: Al seleccionar la acción de curación global, debe ejecutarse exactamente igual que en el estado de batalla.

## 2. Sistema de Turnos de Batalla por Tiempo de Descanso

* Mecánica de descanso: Cada entidad de batalla (battle entity) debe poseer un tiempo de descanso necesario tras realizar un ataque.
* Gestión de turnos: En el método update del estado de batalla, se deben actualizar los contadores/temporizadores de cada entidad. La primera entidad que complete su tiempo de descanso obtendrá el turno para actuar.

# PRV1-I2026

Este repositorio muestra mis soluciones para cada boss final de las islas

---

## LifeUp -> Vida extra

*   **Descripción:** Al destruir un ladrillo, existe una probabilidad del 5% de que caiga un power-up de Vida Extra.

*   **Mecánica de Curación:** Si el jugador ha perdido vidas (tiene menos de 3), recoger este objeto restaura un corazón perdido.

*   **Mecánica de Sobrecarga (Overheal):** Si el jugador recoge el power-up teniendo la vida máxima intacta (3 corazones), el juego premia su habilidad otorgándole un "corazón extra", permitiéndole acumular 4 o más vidas.

*   **Implementación Técnica:** Se aprovechó el sistema de renderizado dinámico en `PlayState` que itera sobre la variable `self.lives`.

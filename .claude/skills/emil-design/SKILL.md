# Habilidades de Diseño UI/UX Dinámico (Emil Kowalski Style)

## Directrices de Animación e Interacción
- **Microinteracciones**: Aplica `transform: scale(0.98)` o `scale(1.02)` en estados `:hover` y `:active` para dar feedback táctil.
- **Transiciones fluidas**: Evita animaciones `linear` o `ease`. Usa curvas `cubic-bezier(0.16, 1, 0.3, 1)` con una duración de `200ms` a `300ms`.
- **Estados focus y hover**: Transiciona cambios de color, bordes y sombras de forma sutil (`transition: all 0.2s ease`).

## Layout y Tipografía
- Usa espaciados consistentes y jerarquía visual clara (contraste de pesos tipográficos).
- Aplica sombreados suaves y multicapa para profundidad visual (`box-shadow: 0 4px 20px -2px rgba(0,0,0,0.05)`).
- Diseña estados de entrada en elementos (`fade-in` combinado con `slide-up` suave).
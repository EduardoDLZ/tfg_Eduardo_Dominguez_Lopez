
**Objetivo**: conseguir acercarse lo máximo posible a un escenario real de un NIDS: entrenar con tráfico observado anteriormente y detectar tráfico posterior.

1. **Etapa 1**: establecer una línea base mediante un análisis preliminar del tráfico de red. El objetivo no es establecer un modelo robusto sino responder qué podemos conseguir con una configuración básica:  
    - ¿Qué modelos son capaces de distinguir las dos clases? (modelos capaces de detectar relaciones no lineales, modelos simples)
    - ¿Existe redundancia de información en el dataset? (análisis de correlación automatizado, limpieza datos más en profundidad para detectar inconsistencias)
    - ¿Son fiables los resultados obtenidos?

2. **Etapa 2**: cómo cambiará el rendimiento cuando optimizados el proceso de preparación, transformación, selección de características y modelado cuando se dispone del conjunto completo. No se aplican los mismos experimentos sobre este dataset porque su función metodológica era establecer una línea base. Efecto estudiar el tamaño del dataset y un efecto de optimización: 


3. **Etapa 3**: pretende estudiar si los resultados se mantiene cuando respetamos la dimensión temporal del tráfico, consiguiendo así un sistema de detección que es entrenado con tráfico observado anteriormente y detecta tráfico posterior.
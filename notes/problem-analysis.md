## Análisis descriptivo del problema

Este problema consiste en desarrollar un modelo de aprendizaje automático capaz de detectar intrusiones maliciosas en redes informáticas y generar alertas automáticas ante posibles amenazas, partiendo de los datos proporcionados por el Instituto de Ciberseguridad de Canadá (CIC).

Para ello vamos a construir un modelo de aprendizaje ¿¿por refuerzo con CNN?? ¿¿automático supervisado??

El conjunto de datos que vamos a utilizar contiene los siguientes valores: 
- $X$ serán los valores de los atributos **Source IP, Source Port, Destination IP, Destination Port, Protocol....**
- $y$ serán el valor que tome el atributo **Label** $\in {DDoS, BENIGN}$

Estamos por tanto ante un problema de **clasificación binaria**.
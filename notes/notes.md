Preguntas:

* ¿Dividir en subsecciones gráficos de correlación? -> OK
* ¿Referenciación papers para Log Scaler y Standard Scaler?
* ¿Descripción de atributos {ECE,CWE,SYN...} Flag Count?
* ¿Explicar hiperparámetros si no hago búsqueda?
* ¿Eliminar/Mantener Window TCP Features (`Init_Win_bytes_forward`, `Init_Win_bytes_backward`)? -> Eliminar
* ¿Por qué no ha usado cross validation? Justificar porque la división ha sido una vez
* ¿Dónde explico las métricas en 05 Desarrollo o 02 Marco Teórico? En 05 puedo contextualizar mejor las métricas al análisis de intrusiones. En 02 puedo poner más métricas (aunque no las utilice en la experimentación) pero no las puedo contextualizar.

Consejos:

* Siempre referenciar imágenes ("En la imagen \\ref{}...")
* Cuanta más información sobre los datos mejor
* Terminar con "." en los itemize
* Utilizar h! o ht! para no dejar espacios en blanco
* Priorizar párrafos pequeños a itemize
* Texto en negrita únicamente si es muy muy importante
* Títulos sin siglas
* Las secciones tienen que tener una longitud aceptable. En otro caso, o se alargan o se añaden en otra.
* Introducción: motivación, justificación, explicar proceso, (planificación se puede meter)
* Capitulo para dataset
* No tengo que meter última tecnología de Transformers porque algoritmos básicos han funcionado -> Simple -> Jugar con el preprocesamiento, algoritmos, ajuste para sacar casi el 100%
* Lo que yo no haya creado en Estado del arte
* 60-100 citas de papers
* Copiar frases y buscar papers




Tareas:

* Explicar mi trabajo escalable -> Comencé con dataset pequeño -> Terminé todo dataset
* ~~Ya después de preocupo si es DDoS o DoS cuando lo detecte -> Dejar como nota que es DoS~~
* Explicar por qué no utilizo Transformers y Redes Neuronales
* ~~Explicar complejidad computacional de DT, RF, SVM, MLPClassifier~~
* ~~Simplificar std-variance de variables clave~~
* ~~4 variables clave como itemize~~
* Explicar riesgo de sobreajuste al tomar 4 variables clave
* ~~Texto de variables numéricas y categóricas~~
* Diagrama del pipeline
* Especificar los hiperparametros
* Explicar en pie de pagina origen del dataset
* Dataframe modelos/conjuntos características a un anexo. 
* Explicar solo los mejores
* Mas tablas y figuras

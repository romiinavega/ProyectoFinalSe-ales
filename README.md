# ProyectoFinalSeñales
 
 
## FUNCIONALIDAD
* Analisis de tiempo real para calcular las frecuencias de audio  
* Identificar Sexta cuerda guitarrra "Mi" este afinada o si es necesario aflojar o apretar la cuerda

**Calculos**

***La frecuencia de la sexta cuerda de una guitarra es de 80.42 hz, pero debido al ruido ambiental se detecta como 164hz a partir de ello fue que se desarrolló la siguiente solución:***

* Sexta cuerda afinada: el analisis indico una frecuencia de 164 para tener el margen de error de le marca un rango de 160 a 170.
* Apretar cuerda: se indica que la Frecuencia Dominante es decir, el numero que nos indica el analisis de tiempo real, tiene que ser mayor a 170.
* Aflojar la cuerda: sea menor a 160, en este caso un "else".


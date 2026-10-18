# Batería de compatibilidad de documentos

Esta batería original combina casos de estructura, objetos, referencias y edición inspirados en los temarios oficiales [MO-110](https://arch-center.azureedge.net/Learning/Credentials/MO-110_OD_MOS365_Word.pdf), [MO-111](https://arch-center.azureedge.net/Learning/Credentials/MO-111_OD_MOS365_WordExpert.pdf) y una [evaluación avanzada de Washburn Tech](https://www.washburntech.edu/business-community/files/Word-2016-L3-Assessment_Final.pdf). No reproduce las preguntas del examen ni certifica todas las funciones o versiones de Word.

## Generar

Requiere Python con python-docx, lxml, Pillow y openpyxl. Se debe seleccionar el runtime y las dependencias del entorno de trabajo.

```text
python tools/compatibility/build-word-battery.py --output <carpeta-nueva> --diagram-font <fuente.ttf>
```

La carpeta debe ser nueva para evitar modificar documentos existentes. La fuente del diagrama es opcional. El generador crea cuatro DOCX sintéticos, una imagen propia, veinte destinatarios ficticios, una macro de ejemplo en texto y un manifiesto con hashes. No crea una macro ejecutable ni ejecuta VBA.

1. Libro maestro: estilos, idiomas, listas, secciones, columnas, orientación mixta, tablas combinadas, cabeceras repetidas, imágenes, un gráfico con XLSX incrustado, un cuadro de texto, ecuación OMML, notas, comentarios, revisiones, campos, citas e índices.
2. Formularios: controles de texto, fecha, lista y casilla; tabla anidada y una fila más alta que una hoja; instrucciones para pruebas interactivas.
3. Correspondencia: campos MERGEFIELD e IF y un CSV separado.
4. Carga: 500 bloques con saltos explícitos y marcadores iniciales/finales. Es una muestra de rendimiento; generar el archivo no prueba su velocidad ni certifica su apariencia.

## Comparar

Abrir el libro maestro en Word, actualizar todos los campos e índices, guardar una copia y exportar una referencia PDF. Registrar versión, archivo y hash. La actualización puede requerir elegir «Actualizar toda la tabla» varias veces. Las fuentes del documento son referencias a nombres de fuentes; no se distribuyen fuentes comerciales.

Importar exactamente esa copia en Scribe y comprobar por separado representación, edición y exportación. Probar tres salidas: sin cambios, un cambio de texto compatible y un cambio estructural. La conservación del paquete original no demuestra que sus objetos se puedan editar. Una reconstrucción puede perder objetos que siguen presentes en el original.

Las instrucciones interactivas dentro del archivo son casos pendientes hasta ejecutarlos y registrar el resultado. Dictado, lectura, micrófono, macros, combinación, accesibilidad, objetos 3D, SmartArt y servicios conectados requieren comprobaciones distintas; ningún DOCX único prueba todo ello.

No cambiar permisos, seguridad de macros ni el Centro de confianza para completar la prueba. Si una operación está bloqueada, registrar el bloqueo. Procesar únicamente copias sintéticas y conservar los originales privados fuera del repositorio.

La matriz de resultados y los límites de la comparación del 17–18 de octubre están en [el informe](../../docs/COMPATIBILIDAD-WORD-BATERIA.md).

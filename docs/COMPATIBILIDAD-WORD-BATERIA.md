# Batería avanzada de compatibilidad con Word

La comparación del 17–18 de octubre de 2026 encontró dos pérdidas de texto en la importación de DOCX. Scribe 3.0.7 recupera los valores de controles de contenido insertados dentro de un párrafo y el texto de cuadros de texto. Selecciona una sola alternativa de representación de Word para evitar duplicados y prefiere imágenes PNG/JPEG compatibles. Los cuadros se muestran en el flujo del documento; su posición y su forma nativa todavía no se reconstruyen.

Se añadieron avisos específicos para ecuaciones nativas, gráficos, controles y campos dinámicos que no se reconstruyen. Un aviso no equivale a implementar esas funciones. Los controles aparecen como texto y no se pueden rellenar como formularios nativos.

## Referencia y método

Se creó una batería sintética propia con un libro maestro, formularios y límites, correspondencia y una carga de 500 páginas. El libro maestro fue abierto sin reparación, actualizado y guardado en Microsoft Word. Su referencia PDF nativa tiene 15 páginas, cuatro índices calculados, secciones en dos columnas y horizontal, tablas, gráfico, ecuación, notas y bibliografía calculada. El hash de la copia DOCX utilizada para la comparación es `9bfac6c40714815d14f3c25a834954b079ec02b598a8c6bd95d9100231f546f9`.

Los temarios oficiales [MO-110](https://arch-center.azureedge.net/Learning/Credentials/MO-110_OD_MOS365_Word.pdf) y [MO-111](https://arch-center.azureedge.net/Learning/Credentials/MO-111_OD_MOS365_WordExpert.pdf), junto con una [evaluación avanzada](https://www.washburntech.edu/business-community/files/Word-2016-L3-Assessment_Final.pdf), orientaron la cobertura. No se afirma haber encontrado «el ejercicio más difícil» ni haber probado todas las funciones de Word. El generador y las instrucciones están en [tools/compatibility](../tools/compatibility/README.md).

Una primera copia de la muestra contenía dos almacenes bibliográficos y Word utilizaba el vacío. Se corrigió la muestra antes de comparar y se comprobó que Word generara la cita y la bibliografía. Este fallo de la muestra no se contabiliza como fallo de Scribe. El generador público utiliza el almacén bibliográfico existente en su plantilla.

## Resultados comprobados

| Caso | Resultado |
| --- | --- |
| Valor de texto, lista y fecha en controles de contenido | Antes ausente; ahora visible en el modelo y en Edge de escritorio y vista móvil |
| Texto dentro de un cuadro de Word | Antes ausente; ahora aparece una vez, como texto del flujo principal |
| Alternativas modernas y heredadas de un objeto | Se importa una rama; prueba de regresión para texto e imagen compatible |
| Exportación sin cambios | Los tres documentos funcionales conservan exactamente los bytes originales |
| Cambio de texto compatible | El inventario de partes nativas del archivo de referencia se conserva |
| Cambio estructural | Se reconstruye el DOCX; pierde ecuación, gráfico, cuadro nativo, notas e historial de cambios de la muestra |
| Formularios tras reconstrucción | Se conserva el texto mostrado; se pierden los cuatro controles interactivos |
| Correspondencia tras reconstrucción | Queda el resultado visible de los cinco campos; no conserva su funcionamiento dinámico |
| Maestro en el editor | 17 páginas frente a 15 de Word; la fidelidad de paginación sigue siendo parcial |
| Carga sintética en Edge en este PC | 500 páginas, marcador final presente, unos 15 s hasta el editor; una medición, sin equivalencia con un teléfono físico |
| Tráfico durante importación de la batería en Edge | Ninguna solicitud de escritura/subida observada en estas pruebas |
| Pruebas automatizadas | 323 TypeScript y 15 JavaScript aprobadas; TypeScript sin errores |

El documento de referencia contiene un gráfico con un libro XLSX incrustado y una ecuación OMML. Que esas partes sobrevivan a un cambio de texto no demuestra representación ni edición en Scribe. Los cuatro controles que crea una exportación reconstruida del maestro pertenecen a sus índices; no son una recuperación de formularios.

## Funciones que siguen faltando o requieren otra prueba

| Prioridad | Función | Estado de esta batería |
| --- | --- | --- |
| Alta | Dictado dentro de Scribe | Falta; no se grabó ni transmitió audio |
| Alta | Lectura en voz alta dentro de Scribe | Falta; el motor de Lore no está integrado en Scribe |
| Alta | Ecuaciones OMML y gráficos nativos editables | Objetos de la referencia detectados; sin representación o edición equivalente |
| Alta | Notas al pie/finales y control de cambios nativos | Conservados en el original; reconstrucción incompleta |
| Alta | Campos de bibliografía, combinación, IF y cálculo | Resultado guardado visible; sin recalcular como Word |
| Alta | Fidelidad de páginas y posiciones flotantes | Parcial; medir por sección y por objeto |
| Media | Texto oculto | El modelo lo muestra como texto normal; falta conservar visibilidad y opción de mostrarlo |
| Media | Controles de formulario y cuadros nativos | Valores/texto recuperados; interacción y geometría pendientes |
| Media | Fila mayor que una hoja | Los 85 marcadores están presentes; falta certificar división visual y PDF propio |
| Media | Idiomas y accesibilidad | Hay texto multilingüe y casos preparados; faltan sesiones de dictado, lectura y navegación accesible |
| Media | VBA ejecutado y DOCM real | Solo se preparó una macro inocua de ejemplo; no se declara ejecución ni compatibilidad VBA |
| Media | Combinación con 20 registros | Plantilla y datos preparados; combinación completa todavía sin ejecutar |
| Ampliación | SmartArt, 3D, OLE adicional, protección, firmas, colaboración y servicios conectados | No ejercitados por este conjunto; no calificarlos como aprobados |

El [dictado de Word](https://support.microsoft.com/es-es/word/dictate-your-documents-in-word) y la [lectura de documentos](https://support.microsoft.com/en-us/word/listen-to-your-word-documents) son funciones interactivas con requisitos que dependen del producto y del motor. El requisito de Auralis de procesar documentos localmente exige comprobar el funcionamiento sin red por separado.

La batería es una base de regresión reproducible. No constituye una certificación de equivalencia total, rendimiento en todos los dispositivos ni conservación de todos los objetos después de reconstruir un documento.

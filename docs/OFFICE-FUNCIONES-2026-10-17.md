# Funciones de documentos comprobadas frente a Office

Este registro complementa la auditoría de 130 puntos. Describe el bloque implementado en Scribe 3.0.6, Folio 8.0.6 y Auralis 3.0.7 BETA. Los estados abiertos de la auditoría se conservan; estos cambios no acreditan equivalencia completa con Office.

## Investigación funcional

Se volvió a inventariar la instalación local de Office16: Word, Excel, PowerPoint, Access, Publisher, OneNote y Outlook. El inventario identifica productos y componentes; contar ejecutables no demuestra haber probado todas sus funciones. La comparación de interfaz de este bloque se efectuó en Word, mediante el ayudante actualizado de Computer Use, que volvió a funcionar.

La cinta y el cuadro Guardar como de Word mostraron funciones de texto, párrafos, estilos, tablas, referencias, revisión y correspondencia, además de DOCX, DOCM, DOC, DOTX, DOTM, PDF, XPS, HTML, RTF, TXT, XML y ODT. Esta observación se usa para organizar el trabajo; no incorpora código, binarios ni recursos de esa instalación a Auralis.

| Área | Implementado y comprobado en este bloque | Trabajo que permanece abierto |
| --- | --- | --- |
| Word y Scribe | Encabezados de tabla de varias filas, alineación vertical, columnas uniformes, propiedades de división para DOCX/PDF; corrección de títulos e índices de apéndices | Paginación completa, división de filas altas en la escritura, tablas anidadas y estilos condicionales, revisión y correspondencia completas |
| Excel y Orbit | Se mantiene el motor y la compatibilidad comprobados anteriormente | Funciones modernas, gráficos y tablas dinámicas, automatización más amplia |
| PowerPoint y Nova | Se mantiene el intercambio de presentaciones anterior | Patrones complejos, animaciones, multimedia y gráficos vinculados |
| Access y Nexus | Se mantienen las tablas, relaciones y consultas locales | Formularios, informes y formatos nativos adicionales |
| Publisher y Canvas | Se mantiene la composición y exportación anterior | Cajas encadenadas, maquetación y preimpresión avanzadas |
| OneNote y Outlook | Productos identificados en el inventario | Sin funciones nuevas implementadas en este bloque |

## Tablas

La opción Propiedades de tabla permite elegir cuántas filas iniciales se repiten. En la escritura, las continuaciones muestran copias no editables de esas filas; se actualizan al modificar el original y no añaden contenido al modelo, al portapapeles ni al archivo. La vista Lectura conserva una única tabla continua. El PDF dibuja las cabeceras en las continuaciones y el DOCX conserva `tblHeader` para que el procesador receptor las repita.

Una cabecera repetida debe ser un prefijo continuo de la tabla. Las combinaciones verticales que atraviesan el límite entre cabecera y cuerpo no se repiten. Los encabezados demasiado altos se conservan como contenido y no generan ciclos de paginación.

Distribuir columnas conserva texto, combinaciones y estructura. La alineación vertical ofrece arriba, centro y abajo, se conserva en el proyecto y se intercambia mediante `vAlign`.

Word abrió la muestra de 45 registros y la exportó a un PDF de tres páginas. En las tres se repiten las dos filas de cabecera y cada registro aparece exactamente una vez. El editor y el PDF propio también producen tres páginas, pero distribuyen los registros de forma diferente: no se declara paginación idéntica. En esta muestra el encabezado general de página no apareció en las continuaciones del PDF de Word; queda pendiente aislar y corregir esa diferencia, separada de las cabeceras de tabla verificadas.

Las propiedades de división permiten conservar el ajuste existente de cada fila, mantener completas las que quepan o permitir su continuación entre páginas. Se aplican al DOCX mediante `cantSplit` y al PDF propio. La escritura mantiene juntas las filas normales; la división visual de una fila mayor que la hoja sigue pendiente. No se presenta como una función terminada de paginación equivalente.

## Índices y apéndices

La comprobación real en Word encontró dos estilos `pStyle` en el mismo párrafo de apéndice: uno de título y otro Normal. Se elimina el conflicto. Los apéndices creados como objetos también participan en la tabla de contenido y conservan las páginas conocidas en su índice. No se inventan números si la paginación no se ha calculado.

Word reconoció los cinco destinos de la tabla de contenido y los dos del índice de apéndices del documento corregido, con páginas 2, 4, 5, 5, 6, 5 y 6. El archivo abierto se exportó a PDF desde la interfaz de Word para revisar su representación. Esta prueba es una muestra de seis páginas, no una certificación de todos los DOCX.

## Fuentes técnicas

- [Repetición de encabezados en Word](https://support.microsoft.com/es-es/word/repeat-table-header-on-subsequent-pages).
- [Propiedad tblHeader de OOXML](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.wordprocessing.tableheader).
- [Propiedad cantSplit de OOXML](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.wordprocessing.cantsplit).

Las pruebas y documentos sintéticos permanecen en `E:\Auralis\Pruebas\2026-10-17-tablas-word`. Los archivos privados de referencia no se publican.

# Saltos, secciones e índices de apéndices

Se corrigieron los saltos en Scribe y en el editor compartido de Folio/Auralis:

- Salto de página o sección en el cursor, conservando ambas partes del párrafo. Ctrl+Enter inserta un salto de página. Dentro de tablas y listas, el salto se coloca después del objeto completo.
- Página vacía arriba, abajo o al final, usando los límites medidos del editor; los saltos explícitos también sirven cuando todavía no existe un mapa de páginas.
- Importación de varios saltos en un mismo párrafo y saltos de columna, conservando su posición respecto al texto.
- Secciones continuas, de página siguiente, par e impar; reinicio de numeración y vínculos de encabezados/pies en DOCX. La paginación del editor respeta la paridad.
- Índice de apéndices exportado como TOC actualizable, apéndices con SEQ alfabético y marcadores para sus enlaces. El editor muestra las páginas medidas en sus índices y conserva sus títulos personalizados.
- Reconocimiento de estilos de título localizados/personalizados y de apéndices identificados mediante SEQ aunque no tengan un estilo de título.

## Referencia privada

El DOCX de VIP Pets con espacios sustituidos por guiones bajos se analizó localmente, sin modificarlo ni incluirlo en el repositorio. Contiene diez campos SEQ de apéndices y cuatro índices TOC. Auralis reconoce diez apéndices y 288 títulos: 243 títulos con nivel de esquema, 35 subtítulos personalizados y diez encabezados de apéndices derivados de SEQ. La copia original conserva su SHA-256.

El índice de figuras aún requiere trabajo: 51 campos SEQ de figura en la referencia frente a 44 figuras con objetos reconocidos. Algunos dibujos/formatos especiales siguen sin reconstruirse. No se declara fidelidad completa de contenido o de paginación.

## Verificación

Se añadieron pruebas de transacciones reales de ProseMirror y de ida y vuelta DOCX: posición del cursor, límites de hojas vacías, texto entre saltos repetidos, títulos personalizados, apéndices dinámicos, marcadores, paridad, orientación y reinicio de numeración. El conjunto pasó 301 pruebas TypeScript y 15 JavaScript antes de la revisión visual final.

El control nativo de Word no pudo iniciarse: `failed to write kernel assets (os error 3)` incluso después de reiniciar el ayudante. Tampoco existe una sesión conectada de Word. El renderizador de DOCX no encontró `soffice.exe`. Por tanto, la verificación en Word y la comparación de su renderizado permanecen pendientes; las pruebas XML/ida y vuelta y las del navegador no sustituyen esa verificación.

Los documentos y los informes privados de prueba permanecen en `E:\Auralis\Pruebas\2026-10-17-secciones` y no se publican.

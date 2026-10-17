# Figuras, secciones y lectura adaptable

Informe de la entrega anterior. La [comprobación posterior en Word](OFFICE-FUNCIONES-2026-10-17.md) encontró y corrigió el conflicto de estilos de apéndice; el control de Word volvió a funcionar para esa prueba.

Actualización BETA: Scribe 3.0.5, Folio 8.0.5 y Auralis 3.0.6.

## Correcciones

- Las imágenes mantienen su orden respecto a los fragmentos de texto de un párrafo DOCX. Una imagen seguida por su nota en el mismo párrafo ya se asocia a su título y al índice de figuras. Se conservan los destinos de los enlaces a títulos e ilustraciones.
- La escritura representa hojas de distintos tamaños, orientaciones y márgenes por sección. Cambiar la selección no cambia la geometría del documento completo. El ajuste de imágenes respeta el ancho disponible.
- Los encabezados, pies, marcas de agua y números se muestran según la sección de cada hoja. La opción de primera página distinta se interpreta también cuando DOCX la desactiva explícitamente; no se hereda esa opción al vincular encabezados.
- Las secciones continuas, la paridad, las hojas vacías, la numeración reiniciada y los párrafos unidos al siguiente intervienen en el cálculo de las páginas. Los índices muestran la numeración de la sección.
- La vista Lectura permite editar en una superficie continua, sin espacios de paginación ni números de índice que dependan de un tamaño de pantalla. Es la vista inicial en pantallas de hasta 700 px. Escribir conserva la representación del papel; insertar una página vacía desde Lectura activa esa representación antes de calcular el punto de inserción.

## Evidencia

El documento privado de referencia se importó localmente: 288 títulos, diez apéndices, 116 tablas y 51 figuras reconocidas en sus cuatro índices. Las 58 imágenes importadas coinciden byte a byte con imágenes del DOCX. Ninguna de las 51 figuras queda con un destino de objeto inexistente. El original permanece intacto y no forma parte del repositorio ni de las entregas.

Las siete figuras pendientes en el informe anterior eran imágenes ya cargadas cuyo texto de nota se reordenaba antes de la imagen. Esta corrección resuelve esa asociación; no representa una nueva capacidad general para reconstruir gráficos o formas especiales.

Pasaron 312 pruebas TypeScript y 15 JavaScript, además de la comprobación TypeScript del entorno. Edge automatizado verificó seis hojas con orientación mixta, selección, crecimiento de texto, deshacer, encabezados, ajuste de imágenes y lectura/edición en una ventana de 390 × 844 px. Esto último es una prueba de ventana móvil, no una prueba física en un teléfono.

## Límites de la validación

Word no pudo controlarse porque el ayudante de Windows falla al inicializar con `failed to write kernel assets (os error 3)`. El renderizador DOCX tampoco dispone de `soffice.exe`. Las pruebas de modelo, XML y navegador no sustituyen la comparación visual con Word. La reconstrucción de objetos especiales y todos los detalles de paginación avanzada siguen sujetos a las limitaciones BETA.

Los informes y capturas privados quedan en `E:\Auralis\Pruebas\2026-10-17-figuras-secciones`.

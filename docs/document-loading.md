# Carga de documentos extensos

La interfaz de carga es común a la web, la instalación web, Android y Windows. La constelación aparece mientras hay trabajo pendiente y desaparece al terminar; no añade esperas mínimas ni porcentajes simulados. La animación respeta la preferencia de movimiento reducido.

PDF y DOCX se leen en trabajadores locales. El trabajador temporal se cierra al terminar o fallar. Los archivos originales y las copias para continuar editando permanecen en el dispositivo.

Las páginas PDF conservan su tamaño inicial, incluido recorte, rotación y escala. Solo las páginas próximas a la vista solicitan su representación y texto. Al abandonar una página se libera el lienzo y se solicita la limpieza de sus recursos de dibujo. La búsqueda, la exportación y el guardado siguen abarcando todo el documento.

El editor de texto pagina por lotes que dejan responder a la interfaz. Los cambios de altura producidos por sus propios separadores no provocan otra paginación completa. El contador de la barra se calcula al cambiar el contenido; el análisis detallado de caracteres se hace cuando se solicita. La composición PDF no recibe las copias del DOCX original ni sus instantáneas de comparación.

Las pruebas de regresión incluyen un PDF de 500 páginas con tamaños y rotaciones distintos y comprueban que abrirlo y exportarlo conserva todas las páginas. El rendimiento real depende del tamaño de las imágenes, las fuentes, la complejidad del documento y los recursos del dispositivo. Estas mejoras no establecen un límite de 500 páginas ni garantizan un tiempo idéntico en todos los equipos.

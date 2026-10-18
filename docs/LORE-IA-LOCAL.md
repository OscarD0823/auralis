# Asistente editorial local de Lore

La revisión ortográfica ligera sigue utilizando diccionarios Hunspell en once idiomas. No necesita un modelo de lenguaje. «IA local» ofrece consultas sobre claridad y coherencia y una conversación sobre el fragmento seleccionado o el capítulo actual.

## Libertad de escritura

Auralis no añade listas de palabras prohibidas, moderación remota ni filtros por género literario. La instrucción editorial pide respetar el vocabulario y los temas del escritor, incluida ficción adulta u oscura. Las sugerencias nunca sustituyen automáticamente el manuscrito.

Se ofrece Qwen 2.5 0.5B Instruct abliteration v3, cuantización Q4_K_M de mradermacher. Es una variante comunitaria orientada a reducir los rechazos del modelo; esto no demuestra ausencia absoluta de rechazos ni calidad editorial perfecta. La procedencia, revisión inmutable y huella digital figuran en `vendor/lore-ai/SOURCE.json`. Se conserva su ficha original y la licencia Apache 2.0 declarada por el distribuidor.

## Uso y privacidad

1. Abre una historia, escribe o selecciona un pasaje y pulsa **IA local**.
2. Descarga el modelo, o importa exactamente el GGUF enlazado. Son unos 380 MiB de pesos y 3 MiB del motor. Se comprueban tamaño y SHA-256 antes de conservarlos.
3. Elige coherencia, ortografía o conversación. Puedes consultar el texto y contexto que recibirá el modelo y avanzar por fragmentos.
4. Contrasta la sugerencia y aplica solo los cambios que decidas.

Los pesos públicos se descargan desde Hugging Face. Los motores proceden de la misma instalación de Auralis. El texto de la novela y las consultas no forman parte de esas solicitudes: la inferencia se ejecuta en un trabajador local mediante WebAssembly. No requiere cuenta ni un servicio de inferencia. El historial del panel dura esta sesión.

La descarga se conserva en IndexedDB. Para abrir la **web** sin conexión hay que preparar también la aplicación desde Actualizaciones; los recursos del programa y los pesos son descargas distintas. El almacenamiento del navegador puede borrarse al limpiar datos del sitio o por falta de espacio. Los proyectos exportados no incluyen los cientos de megabytes de pesos.

## Recursos y alcance

La misma implementación se compila para la web, Android y Windows. Utiliza un solo hilo de CPU, sin GPU obligatoria, contexto de 2048 tokens y respuestas breves. El motor WASM32 se sirve localmente y no exige Memory64 ni JSPI. Sigue siendo necesario que admitan WebAssembly SIMD y excepciones y dispongan de suficiente memoria; no todos los teléfonos podrán cargarlo.

Cancelar, cerrar el panel o agotar el plazo termina el trabajador completo, incluso durante la carga. Un minuto sin consultas libera el modelo de memoria. El corrector ligero permanece disponible si la IA no carga.

La revisión considera un fragmento, el final del anterior y datos breves de los personajes mencionados. No certifica toda la continuidad de una novela ni reemplaza una revisión humana. Un modelo de medio millardo de parámetros puede pasar por alto contradicciones o proponer cambios incorrectos.

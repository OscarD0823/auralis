# Auralis Nexus: exploración, consultas y análisis local

Nexus usa una implementación propia de interfaz y operaciones sobre SQLite (sql.js, con su licencia y avisos). El mismo módulo genera la aplicación independiente y el editor de bases de datos del entorno Auralis. Los archivos se procesan en un trabajador del dispositivo y se guardan en IndexedDB. No se envían a un servidor.

## Bloque del 18 de octubre de 2026

- Navegación por todos los registros con páginas de 25, 50, 100, 250 o 500 filas, búsqueda literal en todos los campos y ordenación. Los filtros se calculan sobre la tabla completa.
- Constructor de SELECT, unión izquierda por una clave externa (incluidas claves compuestas), filtros enlazados y cálculos COUNT/SUM/AVG/MIN/MAX con agrupación. Se puede pasar el resultado al laboratorio SQL y ampliarlo.
- Biblioteca de consultas dentro del propio SQLite, bajo `_auralis_nexus_queries_v1`. Guardar o abrir una consulta nunca la ejecuta. Los valores de los parámetros no se incrustan en el SQL; la recuperación local conserva el borrador por separado. El modo de lectura impide escrituras incluso mediante CTE.
- Mapa navegable de todas las tablas y relaciones. Inspección de índices y valores predeterminados.
- Perfiles de campos (NULL, distintos, mínimo, máximo, suma y promedio) y gráficos de hasta 12 grupos sobre la tabla completa. El perfil cubre hasta 100 columnas; no aplica el filtro del explorador.
- Comprobación explícita de integridad y de claves externas. SQLite documenta que `integrity_check` no detecta errores de claves externas; por eso se ejecutan ambas comprobaciones.
- Exportación de la tabla filtrada o la última consulta a CSV, TSV, JSON y XLSX. Estas salidas admiten hasta 100.000 filas y 64 MB estimados de valores en memoria; rechazan un resultado mayor sin descargar una copia truncada. SQLite conserva la base completa, los BLOB, los índices, las relaciones y las consultas guardadas.
- Formularios de registros con distinción entre texto vacío y NULL, valores predeterminados, conservación de BLOB existentes y eliminación con confirmación. Identificación por rowid cuando está disponible para evitar editar varias filas con una clave primaria nullable.
- Deshacer y rehacer hasta 10 cambios y 80 MB por pila. Los lotes SQL e importaciones tabulares son transacciones; el error revierte la operación. Cancelar termina el trabajador y recupera la última base completada. Navegar o consultar en modo lectura no vuelve a serializar la base entera.

## Uso

1. Abre un SQLite, importa CSV/TSV/XLSX o usa una plantilla.
2. Busca, ordena y navega en **Tabla**. **Registro** abre el formulario.
3. En **Constructor**, elige una relación declarada y los campos o cálculos. **Preparar consulta SQL** permite revisar el texto antes de ejecutarlo.
4. En **Consulta SQL**, introduce parámetros como `:minimo`. Selecciona Texto, Número o NULL. La lectura es el modo inicial; desactívala para cambios de datos o esquema. Guarda la consulta con un nombre si deseas reutilizarla.
5. Usa **Análisis**, **Relaciones**, **Diseño** y **Salud** para examinar la base. Vuelve a ejecutar análisis y diagnósticos tras cambiar los datos.
6. Descarga SQLite para una copia completa y transportable. La biblioteca local depende del almacenamiento disponible y de que el navegador no borre los datos del sitio.

## Límites y trabajo restante

No se declara equivalencia total con Access ni superioridad frente a todas sus versiones. Siguen pendientes ACCDB/MDB nativos, VBA completo, diseñador libre de formularios e informes, permisos multiusuario y conexiones a bases remotas. El constructor visual prepara una unión por vez y no representa autorrelaciones; SQL permite consultas más amplias. Una sola sentencia de exportación puede volver a ejecutar funciones no deterministas. Las vistas previas SQL muestran hasta 500 filas. Bases de hasta 80 MB; importaciones de hasta 10.000 filas y 100 columnas. Los BLOB se etiquetan en formatos tabulares y permanecen completos en SQLite.

Las reglas de negocio y la corrección semántica requieren revisión del autor. Las mediciones de escritorio, ventanas móviles y APK no equivalen por sí solas a una prueba en un teléfono físico.

## Referencias funcionales

Se consultaron [estructura de bases de Access](https://support.microsoft.com/en-us/access/learn-the-structure-of-an-access-database), [relaciones](https://support.microsoft.com/en-us/access/guide-to-table-relationships) y [consultas con parámetros](https://support.microsoft.com/en-us/access/use-parameters-in-queries-forms-and-reports) para contrastar funciones, sin copiar código propietario. Contratos técnicos: [PRAGMA de SQLite](https://www.sqlite.org/pragma.html) y [claves externas](https://www.sqlite.org/foreignkeys.html).

Autor: OscarD0823. BETA. Las pruebas de regresión están en el repositorio `auralis-nexus`, `tests/data-workbench.test.ts`.

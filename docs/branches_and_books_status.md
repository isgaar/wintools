# Estado de Ramas y Libros Trabajados (epub-generator & windows-scripts)

Este documento registra el inventario completo de ramas, libros traducidos, configuraciones de orquestador y mejoras de infraestructura distribuidas en el proyecto, permitiendo sincronizar y continuar el trabajo de forma automática desde cualquier equipo nuevo (servidor 24/7).

---

## 1. Inventario de Ramas en GitHub (`arodoo/epub-generator.git`)

| Rama | Propósito Principal | Libros / Idiomas Incluidos | Estado Remoto |
|---|---|---|---|
| **`wip/workstation-migration-handoff`** | **Rama activa de migración 24/7** | • **Dazai Lote 1 Español** (7 libros completos en `01translator/books-translated/`)<br>• **Dazai Portugués** (65 partes en `splitter/` y 6 configs JSON)<br>• Correcciones del orquestador y browser Gemini<br>• Prompts de limpieza y layout | Subida a GitHub (`origin`) |
| **`translations/dazai-osamu-pt`** | Rama dedicada para entregas en Portugués | • **Dazai Portugués** (65 partes traducidas en `splitter/` + 6 configs JSON)<br>• Commits limpios sin mezclar código del motor | Subida a GitHub (`origin`) |
| **`main`** | Rama troncal upstream (Arodi) | • Obras alemanas de Dazai (*Righteousness and Smiles*, *Regretful Parting*)<br>• Catálogo histórico (Sōseki, Lu Xun, Undset, Couto, Ewers, Woolf)<br>• Prompts base y metadatos | Subida a GitHub (`origin`) |
| **`feature/multi-language-epub-support`** | Funcionalidad multi-idioma y Oda Saku | • EPUBs y metadatos de Oda Sakunosuke (*Lady of Saturday*) | Subida a GitHub (`origin`) |
| **`hardening/e2e-translation-assets-100-wt`** | Reestructuración DDD del módulo | • Normalización de estructura de assets y configs | Subida a GitHub (`origin`) |

---

## 2. Detalle del Contenido por Rama

### A. Rama `wip/workstation-migration-handoff` (Recomendada para el equipo 24/7)

Esta rama reúne el estado de trabajo más reciente y completo para operar de forma continua sin depender de la máquina local.

#### 1. Libros en Español (Dazai Osamu - Lote 1)
Ubicación: `01translator/books-translated/japon/dazai-osamu/es/lote-1/`
- `the-criminal.txt` — *El criminal* (Obra #24)
- `decadent-protest.txt` — *Protesta decadente* (Obra #25)
- `gender-equality.txt` — *Igualdad de género* (Obra #26)
- `philosophy-of-the-multiheaded-snake.txt` — *Filosofía de la serpiente multicéfala* (Obra #27)
- `revolution.txt` — *Revolución* (Obra #28)
- `the-blueeyed-pilgrim.txt` — *El peregrino de ojos azules* (Obra #29)
- `bottomless-hell.txt` — *El infierno sin fondo* (Obra #30)

#### 2. Partes Traducidas al Portugués (Dazai Osamu - 65 partes)
Ubicación: `splitter/japon/dazai-osamu/*/pt/`
- `eight-views-of-tokyo/pt/` — partes `01.txt` a `05.txt` (5 partes)
- `new-hamlet/pt/` — partes `01.txt` a `37.txt` (37 partes)
- `on-the-intent-of-regretful-parting/pt/` — parte `01.txt` (1 parte)
- `romanesque/pt/` — partes `03.txt` a `08.txt` (6 partes)
- `the-phoenix/pt/` — partes `01.txt` a `14.txt` (14 partes)
- `the-sea/pt/` — parte `01.txt` (1 parte)
- `the-unrunning-thoroughbred/pt/` — parte `01.txt` (1 parte)

#### 3. Configuraciones de Orquestador JSON
Ubicación: `amazon_publisher/translator/orchestrator/configs/dazai-osamu/`
- `dazai-osamu-lote-1-pt.json`
- `dazai-osamu-lote-2-pt.json`
- `dazai-osamu-lote-3-pt.json`
- `dazai-osamu-lote-4-pt.json`
- `dazai-osamu-lote-5-pt.json`
- `dazai-osamu-pt.json`

#### 4. Motor de Traducción y Correcciones de Batch
- `amazon_publisher/translator/gem/gem_browser.py`: control de desconexiones y captura HTML ante cuota agotada.
- `amazon_publisher/translator/orchestrator/application/handlers/batch/batch_handler_translate.py`: diagnóstico de retorno del subproceso y timeout de 1 hora.
- `amazon_publisher/translator/infrastructure/browser_launcher.py`: aislamiento de sesión Brave con remote debugging.
- `amazon_publisher/translator/orchestrator/application/state.py`: serialización de estado atómico con bloqueo.
- `amazon_publisher/requirements.txt`: especificación de librerías del orquestador.
- `tools/punt_spacing/tests.py` & `tools/lt_setup.py`: suite de pruebas para espaciado tipográfico y rayas de diálogo.

#### 5. Prompts Especializados
Ubicación: `agents/prompts/`
- `remove-dazai-artifacts.prompt.md`: filtro de preámbulo generado por Gemini (autor/título redundantes en `part_01.txt`). Se ejecuta inmediatamente tras concatenar.
- `search-markers.prompt.md`: búsqueda semántica difusa mediante LLM cuando los regex estándar no detectan marcadores de capítulo.
- `book-layout.prompt.md`: maquetador maestro de estructura y alineación contra fuente original.

---

### B. Rama `translations/dazai-osamu-pt`

Diseñada para mantener un historial limpio de contribuciones específicas para el lote en portugués:
- Contiene exactamente las 65 partes en portugués listadas arriba.
- Contiene las 6 configuraciones JSON del orquestador.
- No contiene modificaciones en código de Python ni las traducciones del lote 1 en español.

---

### C. Rama `main` (Upstream)

Mantenida por Arodi con la versión base y publicaciones editoriales consolidadas:
- Obras en alemán de Osamu Dazai (*Righteousness and Smiles* y *Regretful Parting*).
- Formatos omnibus publicados en KDP, StreetLib y D2D (Sōseki, Lu Xun, Sigrid Undset, etc.).
- Metadatos globales y portadas.

---

## 3. Automatización desde `windows-scripts`

El directorio `windows-scripts` gestiona todo el ciclo de vida sin necesidad de modificar el repositorio de `epub-generator`:

### A. Clonado e Instalación Inicial (Equipo Nuevo)
Al ejecutar:
```cmd
setup_all.bat
```
Opción `[1]` o `[6]` detecta automáticamente si `epub-generator` existe en el directorio contiguo (`..\epub-generator`). Si no existe:
1. Clona `https://github.com/arodoo/epub-generator.git`.
2. Ofrece de forma interactiva seleccionar en qué rama posicionarse (`wip/workstation-migration-handoff`, `translations/dazai-osamu-pt` o `main`).
3. Instala Python 3.11, crea el `.venv` e instala todas las dependencias.

### B. Gestión de Ramas desde el Menú de `setup_all.bat`
- Selecciona la opción `[12]` para listar y cambiar de rama de forma segura con verificación previa (`git fetch` y `git checkout`).
- Selecciona la opción `[13]` para abrir este documento explicativo.

### C. Comandos CLI Directos
Puedes automatizar el cambio de rama directamente por línea de comandos:
```cmd
setup_all.bat --branch wip/workstation-migration-handoff
setup_all.bat --branch translations/dazai-osamu-pt
setup_all.bat --branches
```
O directamente mediante el gestor Python:
```cmd
python core/branch_manager.py list
python core/branch_manager.py switch wip/workstation-migration-handoff
```

---

## 4. Flujo Recomendado para el Servidor 24/7

1. En el nuevo equipo, clonar `windows-scripts`:
   ```bash
   git clone https://github.com/isgaar/wintools.git windows-scripts
   cd windows-scripts
   ```
2. Ejecutar el instalador completo:
   ```cmd
   setup_all.bat --all
   ```
3. Seleccionar la rama `wip/workstation-migration-handoff` cuando lo solicite (o ejecutar `setup_all.bat --branch wip/workstation-migration-handoff`).
4. Abrir una terminal con los alias activos y ejecutar el orquestador o la auditoría del lote:
   ```cmd
   orch amazon_publisher/translator/orchestrator/configs/dazai-osamu/dazai-osamu-lote-1-pt.json
   ```

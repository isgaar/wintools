# Windows Scripts (wintools) — epub-generator, Git & Gestor de Alias CMD

Esta carpeta contiene scripts independientes de Windows para automatizar la instalación de dependencias de `epub-generator`, instalar **Git para Windows** y configurar alias en CMD/PowerShell estilo Linux, **sin modificar ningún archivo del repositorio**.

---

## 📁 Estructura del Proyecto

```
windows-scripts/
├── setup_all.bat                      # Menú interactivo principal (todas las opciones)
├── agent.bat                          # Acceso directo al Agent Bridge
├── README.md                          # Documentación del repositorio
├── .gitignore                         # Exclusiones de Git
├── core/
│   ├── agent_hub.py                   # Orquestador del puente interactivo, control de pasos y seguridad
│   ├── configure_cmd_aliases.bat      # Inyector de macros y ejecutables globales en Antigravity IDE/bin
│   └── discord_tools.py               # Automatización Win32: enfoque, limpieza de buffer, pegado y envío en Discord
├── installers/
│   ├── install_epub_deps.bat          # Creador de .venv e instalador de dependencias de Python
│   └── install_git.bat                # Verificador e instalador silencioso de Git
├── docs/
│   └── audit_instructions.md          # Flujo oficial y reglas de Discord (#instrucciones-para-auditar)
└── context/
    └── latest_shift_diagnostic.md     # Snapshot del estado de obras en turno para ahorro de tokens
```

| Archivo | Ubicación | Descripción |
| :--- | :--- | :--- |
| **`setup_all.bat`** | Raíz | Menú interactivo con todas las opciones (Git, dependencias, alias, agent). |
| **`agent.bat`** | Raíz | Lanzador rápido del Agent Bridge para auditoría y control de pasos. |
| **`agent_hub.py`** | `core/` | Motor Python: control paso a paso, puente Discord y guardia de commits. |
| **`discord_tools.py`** | `core/` | Automatización de escritorio Win32: conexión a `winsta0\default`, pegado limpio y auto-envío en Discord. |
| **`configure_cmd_aliases.bat`** | `core/` | Registra macros persistentes en CMD y ejecutables globales (`agent`, `epub`, `ag`). |
| **`install_epub_deps.bat`** | `installers/` | Crea `.venv` e instala dependencias de `epub-generator`. |
| **`install_git.bat`** | `installers/` | Verifica y descarga Git para Windows. |
| **`audit_instructions.md`** | `docs/` | Flujo oficial de trabajo y reglas aprendidas de Discord. |
| **`latest_shift_diagnostic.md`** | `context/` | Snapshot del diagnóstico y tareas en turno para evitar relecturas y ahorrar tokens. |

---

## 🛡️ Agent Bridge (`agent.bat` / `agent`)

El script `agent` actúa como **puente de auditoría y orquestación interactiva** entre la sesión de trabajo y `epub-generator`, asegurando control total humano:

### Reglas Clave Integradas:
1. **Aprobación Obligatoria Paso a Paso**: Todo comando, auditoría o modificación ejecutada sobre `epub-generator` requiere confirmación explícita del usuario (`[s/N]`).
2. **Guardia Estricto de Commits**: **Ningún commit se realiza automáticamente**. Muestra el diff detallado y exige autorización explícita de Arodi (`ARODI`).
3. **Integración y Automatización con Discord (Servidor "epubs")**:
   - **`#instrucciones-para-auditar`**: Consulta las pautas de trabajo y lotes activos asignados por Arodi.
   - **`#issues`**: Canal oficial para reportar cualquier anomalía, fallo de pipeline o contradicción al triangular reportes.
   - **`#bitácora`**: Canal oficial para registrar entregas de obras/lotes procesados cuando cumplen el criterio de aceptación (**en lugar de crear ramas de Git separadas**).
   - **Pegado y Envío Automático (`agent paste` / `agent bitacora`)**:
     - Conexión directa a la estación de ventana interactiva (`winsta0\default`).
     - Limpieza automática de la caja de mensajes (`Ctrl+A` + `Backspace`) para evitar concatenaciones o duplicados.
     - Formato sobrio y natural (sin emojis) con Markdown nativo para Discord (`python` syntax highlighting).
     - Envío automático mediante simulación de <kbd>Enter</kbd>.
4. **Persistencia de Contexto**: Guarda el estado actual en `context/latest_shift_diagnostic.md` para ahorrar tokens y no recalcular el estado desde cero.

### Comandos de `agent`:
```cmd
agent               # Abre el menú interactivo con todas las opciones
agent discord       # Abre/enfoca Discord y muestra canales (#instrucciones-para-auditar, #issues, #bitácora)
agent instructions  # Muestra y registra instrucciones del canal #instrucciones-para-auditar
agent context       # Muestra el último snapshot del contexto guardado (ahorro de tokens)
agent status        # Verifica el estado de Git en epub-generator
agent diff          # Muestra el diff detallado de cambios pendientes
agent commit        # Flujo de commit seguro (inspección de diff + aprobación de Arodi)
agent audit         # Menú interactivo de herramientas de auditoría (Grammar / Sanity / Suite)
agent issue         # Generador guiado de reporte de inconsistencias para #issues
agent bitacora      # Registra formalmente una entrega en #bitácora tras cumplir criterio de aceptación
agent paste [file]  # Pega limpiamente y envía en automático el reporte en el canal #issues de Discord
agent run <comando> # Ejecuta cualquier comando con aprobación previa obligatoria
```

---

## ⚡ Cómo usar los scripts

### Opción 1: Menú interactivo (Doble clic)
Haz doble clic sobre [`setup_all.bat`](file:///c:/Users/Inicio/Proyectos/windows-scripts/setup_all.bat) y selecciona la opción deseada.

### Opción 2: Desde la consola CMD
```cmd
cd C:\Users\Inicio\Proyectos\windows-scripts
setup_all.bat
```
O directamente con flags:
```cmd
setup_all.bat --all             # Instala Git, Brave, dependencias y configura alias
setup_all.bat --brave           # Verifica o instala Brave Browser (requerido para Gemini)
setup_all.bat --deps            # Solo dependencias y entorno virtual
setup_all.bat --clean-locks     # Elimina bloqueos (.lock) huerfanos del orquestador
setup_all.bat --export-aliases  # Exporta todos los alias creados hacia el repositorio
setup_all.bat --list-aliases    # Muestra los alias configurados y sus rutas portables
setup_all.bat --git             # Solo verifica/instala Git
setup_all.bat --aliases         # Solo alias (aplica y sincroniza todos)
setup_all.bat --agent           # Inicia Agent Bridge directamente
```

---

## 🚀 Alias disponibles en CMD y PowerShell

Una vez configurado, puedes abrir **cualquier terminal (CMD o PowerShell)** y usar:

| Comando | Acción |
| :--- | :--- |
| **`orch <config>`** | Ejecuta directamente el orquestador de traducción de `epub-generator`. |
| **`unlock`** | Elimina bloqueos `.lock` huérfanos si un proceso previo fue interrumpido. |
| **`epub`** | Salta al directorio de `epub-generator`. |
| **`agent`** | Inicia el puente interactivo de auditoría y control de pasos. |
| **`ag .`** o **`ag`** | Abre la carpeta actual en **Antigravity IDE**. |
| **`add-alias <nombre> [ruta]`** | Registra cualquier carpeta como comando de acceso rápido. |
| **`ls`** o **`ll`** | Lista los archivos del directorio actual (estilo Linux). |
| **`clear`** | Limpia la consola (`cls`). |
| **`which <comando>`** | Muestra la ubicación de un ejecutable (`where.exe`). |

---

## ⚡ Configuración en un Segundo Equipo (Ahorro de Energía)

Para trasladar tareas pesadas o maratones de traducción a otro equipo:

1. **Clonar wintools / windows-scripts**:
   ```cmd
   git clone https://github.com/isgaar/wintools.git windows-scripts
   cd windows-scripts
   ```
2. **Ejecutar instalación completa**:
   ```cmd
   setup_all.bat --all
   ```
   *(Instala Git, Brave Browser, clona `epub-generator` automáticamente si no existe, crea `.venv` con todas las dependencias e inyecta los comandos globales).*
3. **Paso único en Brave Browser**:
   Abre Brave, entra a [Gemini](https://gemini.google.com) e inicia sesión con tu cuenta de Google (para que tus Gems estén disponibles).
4. **Lanzar maratón**:
   ```cmd
   orch amazon_publisher/translator/orchestrator/configs/dazai-osamu/dazai-osamu-pt.json
   ```

---

## 🔒 Integridad del Repositorio
Estos scripts operan externamente desde `windows-scripts/` para mantener limpio el entorno de producción.

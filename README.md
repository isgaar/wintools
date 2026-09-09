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
│   ├── agent_hub.py                   # Motor interactivo del agente y puente de seguridad
│   └── configure_cmd_aliases.bat      # Gestor de macros y comandos globales en el PATH
├── installers/
│   ├── install_epub_deps.bat          # Verificador de entorno, .venv y dependencias
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
3. **Integración con Discord (Servidor "epubs")**:
   - **`#instrucciones-para-auditar`**: Consulta las pautas de trabajo y lotes activos asignados por Arodi.
   - **`#issues`**: Canal oficial para reportar cualquier anomalía, fallo de pipeline o contradicción al triangular reportes. El asistente formatea el issue y lo copia automáticamente al portapapeles (`clip.exe`).
4. **Persistencia de Contexto**: Guarda el estado actual en `context/latest_shift_diagnostic.md` para ahorrar tokens y no recalcular el estado desde cero.

### Comandos de `agent`:
```cmd
agent               # Abre el menú interactivo con todas las opciones
agent discord       # Abre/enfoca Discord y muestra canales (#instrucciones-para-auditar, #issues)
agent instructions  # Muestra y registra instrucciones del canal #instrucciones-para-auditar
agent context       # Muestra el último snapshot del contexto guardado (ahorro de tokens)
agent status        # Verifica el estado de Git en epub-generator
agent diff          # Muestra el diff detallado de cambios pendientes
agent commit        # Flujo de commit seguro (inspección de diff + aprobación de Arodi)
agent audit         # Menú interactivo de herramientas de auditoría (Grammar / Sanity / Suite)
agent issue         # Generador guiado de reporte de inconsistencias para #issues
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
setup_all.bat --all       # Instala Git, dependencias y configura alias
setup_all.bat --agent     # Inicia Agent Bridge directamente
setup_all.bat --git       # Solo verifica/instala Git
setup_all.bat --deps      # Solo dependencias
setup_all.bat --aliases   # Solo alias
```

---

## 🚀 Alias disponibles en CMD (Estilo Linux)

Una vez configurado, puedes abrir **cualquier ventana de CMD** y usar:

| Comando | Acción |
| :--- | :--- |
| **`agent`** | Inicia el puente interactivo de auditoría y control de pasos. |
| **`ag .`** o **`ag`** | Abre la carpeta actual en **Antigravity IDE**. |
| **`antigravity-ide .`** | Comando completo original. |
| **`epub`** | Salta a `epub-generator` y lo abre automáticamente en el editor. |
| **`add-alias <nombre> [ruta]`** | Registra cualquier carpeta como alias para abrirla en Antigravity IDE. |
| **`ls`** o **`ll`** | Lista los archivos del directorio actual (estilo Linux). |
| **`clear`** | Limpia la consola (`cls`). |
| **`which <comando>`** | Muestra la ubicación de un ejecutable (`where.exe`). |
| **`alias nom=cmd`** | Crea un alias temporal en la sesión actual. |

---

## 🔒 Integridad del Repositorio
Estos scripts operan externamente desde `windows-scripts/`. Ningún archivo de código, documentación o configuración del repositorio `epub-generator` es modificado.

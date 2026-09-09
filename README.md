# Windows Scripts — epub-generator & Gestor de Alias CMD

Esta carpeta contiene scripts independientes de Windows para automatizar la instalación de dependencias de `epub-generator` y configurar alias en CMD/PowerShell estilo Linux, **sin modificar ningún archivo del repositorio**.

---

## 📁 Archivos Disponibles

| Script | Descripción |
| :--- | :--- |
| **`setup_all.bat`** | Menú interactivo con todas las opciones (o flags `--all`, `--deps`, `--aliases`). |
| **`install_epub_deps.bat`** | Instala Python (si no está), crea `.venv` e instala las dependencias de cada submódulo de `epub-generator`. |
| **`configurar_aliases_cmd.bat`** | Configura alias persistentes en CMD vía AutoRun del Registro y genera comandos globales en el PATH. |

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
setup_all.bat --all       # Instala dependencias y configura alias
setup_all.bat --deps      # Solo dependencias
setup_all.bat --aliases   # Solo alias
```

---

## 🚀 Alias disponibles en CMD (Estilo Linux)

Una vez configurado, puedes abrir **cualquier ventana de CMD** y usar:

| Comando | Acción |
| :--- | :--- |
| **`ag .`** o **`ag`** | Abre la carpeta actual en **Antigravity IDE**. |
| **`antigravity-ide .`** | Comando completo original. |
| **`epub`** | Salta a `epub-generator` y lo abre automáticamente en el editor. |
| **`add-alias <nombre> [ruta]`** | Registra cualquier carpeta como alias para abrirla en Antigravity IDE. |
| **`ls`** o **`ll`** | Lista los archivos del directorio actual (estilo Linux). |
| **`clear`** | Limpia la consola (`cls`). |
| **`which <comando>`** | Muestra la ubicación de un ejecutable (`where.exe`). |
| **`alias nom=cmd`** | Crea un alias temporal en la sesión actual. |

### Ejemplo de cómo agregar un alias para cualquier otra carpeta:
```cmd
add-alias miweb "C:\Users\Inicio\Proyectos\miweb"
```
A partir de ese momento, escribes `miweb` en cualquier CMD y se abrirá esa carpeta en Antigravity IDE.

---

## 🔒 Integridad del Repositorio
Estos scripts operan externamente desde `windows-scripts/`. Ningún archivo de código, documentación o configuración del repositorio `epub-generator` es modificado.

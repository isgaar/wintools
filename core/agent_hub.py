"""
Location: C:/Users/Inicio/Proyectos/windows-scripts/core/agent_hub.py
Function: Independent interactive bridge and safety orchestrator for epub-generator audits, Discord coordination and commit guard.
All Rights Reserved Arodi Emmanuel
"""

import sys
import os
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CORE_DIR = Path(__file__).resolve().parent
ROOT_DIR = CORE_DIR.parent
PROJECT_DIR = (ROOT_DIR / ".." / "epub-generator").resolve()
VENV_PYTHON = PROJECT_DIR / ".venv" / "Scripts" / "python.exe"
PYTHON_EXE = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable

COLOR_CYAN = "\033[96m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_MAGENTA = "\033[95m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"

def supports_color() -> bool:
    return sys.platform == "win32" or os.isatty(sys.stdout.fileno())

def cprint(text: str, color: str = COLOR_RESET) -> None:
    if supports_color():
        print(f"{color}{text}{COLOR_RESET}")
    else:
        print(text)

def print_header(title: str, subtitle: str = "") -> None:
    sep = "=" * 70
    cprint(sep, COLOR_CYAN)
    cprint(f"   {title.center(64)}", COLOR_BOLD + COLOR_CYAN)
    if subtitle:
        cprint(f"   {subtitle.center(64)}", COLOR_YELLOW)
    cprint(sep, COLOR_CYAN)
    print()

def open_discord(show_info: bool = True) -> None:
    try:
        subprocess.Popen(["cmd", "/c", "start", "discord:"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if show_info:
            cprint("[OK] Lanzando o enfocando ventana de Discord...", COLOR_GREEN)
    except Exception as e:
        cprint(f"[!] Error al invocar protocolo de Discord: {e}", COLOR_RED)

    if show_info:
        print()
        cprint("+--------------------------------------------------------------------+", COLOR_MAGENTA)
        cprint("|              CANALES CLAVE EN DISCORD (SERVIDOR: epubs)            |", COLOR_BOLD + COLOR_MAGENTA)
        cprint("+--------------------------------------------------------------------+", COLOR_MAGENTA)
        cprint("| [SERVIDOR] 'epubs'                                                 |", COLOR_CYAN)
        cprint("|                                                                    |", COLOR_CYAN)
        cprint("| [CANAL] #instrucciones-para-auditar                                |", COLOR_GREEN)
        cprint("|    * Directrices de trabajo, orden de prioridades y lotes.         |", COLOR_RESET)
        cprint("|    * En este canal se revisa lo que pone Arodi en cada turno.      |", COLOR_RESET)
        cprint("|                                                                    |", COLOR_CYAN)
        cprint("| [CANAL] #issues                                                    |", COLOR_RED)
        cprint("|    * Canal exclusivo para reportar inconsistencias o bloqueos.    |", COLOR_RESET)
        cprint("|    * Si hay fallo al triangular reportes o anomalias de auditoria, |", COLOR_RESET)
        cprint("|      escribe y reporta aqui inmediatamente.                        |", COLOR_RESET)
        cprint("+--------------------------------------------------------------------+", COLOR_MAGENTA)
        print()

def ask_user_approval(action_name: str, command_str: str = "", details: str = "", cwd: Path = PROJECT_DIR) -> bool:
    cprint("\n" + ("-" * 70), COLOR_YELLOW)
    cprint(" [CONTROL DE PASO] APROBACIÓN REQUERIDA DEL USUARIO FINAL", COLOR_BOLD + COLOR_YELLOW)
    cprint("-" * 70, COLOR_YELLOW)
    print(f" • Acción:      {action_name}")
    if command_str:
        print(f" • Comando:     {command_str}")
    print(f" • Directorio:  {cwd}")
    if details:
        print(f" • Detalle:     {details}")
    cprint("-" * 70, COLOR_YELLOW)
    
    try:
        resp = input(" ¿Aprobar y ejecutar este paso? [s/N]: ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print()
        return False
        
    if resp in ["s", "si", "y", "yes"]:
        cprint("[APROBADO] Ejecutando paso...\n", COLOR_GREEN)
        return True
    else:
        cprint("[CANCELADO] Paso no aprobado. No se realizó ninguna acción.", COLOR_RED)
        return False

def run_project_command(cmd_args: list[str] | str, action_name: str, details: str = "", auto_approve: bool = False) -> int:
    cmd_display = cmd_args if isinstance(cmd_args, str) else " ".join(cmd_args)
    if not auto_approve:
        if not ask_user_approval(action_name, cmd_display, details, cwd=PROJECT_DIR):
            return 1

    try:
        shell_mode = isinstance(cmd_args, str)
        res = subprocess.run(cmd_args, cwd=PROJECT_DIR, shell=shell_mode)
        return res.returncode
    except Exception as ex:
        cprint(f"[ERROR] Falló la ejecución: {ex}", COLOR_RED)
        return 1

def show_git_status() -> None:
    cprint("\n[GIT STATUS - epub-generator]", COLOR_BOLD + COLOR_CYAN)
    if not PROJECT_DIR.exists():
        cprint(f"[ERROR] No se encuentra el directorio {PROJECT_DIR}", COLOR_RED)
        return

    res = subprocess.run(["git", "status", "--short"], cwd=PROJECT_DIR, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.stdout.strip():
        print(res.stdout)
    else:
        cprint(" El árbol de trabajo está limpio (sin cambios pendientes).", COLOR_GREEN)

def show_git_diff() -> None:
    cprint("\n[GIT DIFF - epub-generator]", COLOR_BOLD + COLOR_CYAN)
    if not PROJECT_DIR.exists():
        cprint(f"[ERROR] No se encuentra el directorio {PROJECT_DIR}", COLOR_RED)
        return

    res = subprocess.run(["git", "diff", "--stat"], cwd=PROJECT_DIR, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if not res.stdout.strip():
        cprint(" No hay diferencias en archivos rastreados.", COLOR_GREEN)
        return

    cprint("Resumen de archivos modificados:", COLOR_YELLOW)
    print(res.stdout)

    try:
        ans = input("¿Mostrar diff detallado completo? [S/n]: ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        return

    if ans not in ["n", "no"]:
        print()
        subprocess.run(["git", "diff"], cwd=PROJECT_DIR)

def safe_commit_flow() -> None:
    print_header("GUARDIA DE COMMITS — CONTROL ESTRICTO DE ARODI", "REGLA: Ningún commit se hace sin revisión previa")
    show_git_status()
    show_git_diff()

    print()
    cprint("⚠️  ATENCIÓN: Se requiere confirmación explícita de revisión humana.", COLOR_BOLD + COLOR_YELLOW)
    cprint("    ¿Arodi ha visto y aprobado formalmente estos cambios?", COLOR_YELLOW)
    
    try:
        ans = input(" Escribe 'ARODI' para confirmar o presiona Enter para cancelar: ").strip()
    except (KeyboardInterrupt, EOFError):
        cprint("\n[CANCELADO] Proceso de commit abortado.", COLOR_RED)
        return

    if ans != "ARODI":
        cprint("[DENEGADO] Commit cancelado. No se permite realizar commit sin revisión y confirmación de Arodi.", COLOR_RED)
        return

    try:
        commit_msg = input(" Ingresa el mensaje del commit: ").strip()
    except (KeyboardInterrupt, EOFError):
        cprint("\n[CANCELADO] Proceso de commit abortado.", COLOR_RED)
        return

    if not commit_msg:
        cprint("[ERROR] El mensaje de commit no puede estar vacío.", COLOR_RED)
        return

    if ask_user_approval("Confirmar git add y git commit", f'git add -A && git commit -m "{commit_msg}"', "Confirmación final autorizada por Arodi"):
        subprocess.run(["git", "add", "-A"], cwd=PROJECT_DIR)
        res = subprocess.run(["git", "commit", "-m", commit_msg], cwd=PROJECT_DIR)
        if res.returncode == 0:
            cprint("\n[OK] Commit realizado exitosamente con la aprobación de Arodi.", COLOR_GREEN)
        else:
            cprint("\n[!] Falló el comando git commit.", COLOR_RED)

def copy_to_clipboard(text: str) -> bool:
    try:
        proc = subprocess.Popen(["clip"], stdin=subprocess.PIPE, text=True, encoding="utf-8")
        proc.communicate(text)
        return proc.returncode == 0
    except Exception:
        return False

def create_issue_flow() -> None:
    print_header("GENERADOR DE REPORTES PARA #issues (DISCORD)", "Triangulación de reportes y reporte de anomalías")
    cprint("Este asistente formatea un reporte estructurado y lo copia al portapapeles", COLOR_CYAN)
    cprint("para que puedas pegarlo directamente en el canal #issues del servidor 'epubs'.\n", COLOR_CYAN)

    try:
        obra = input(" 1. Obra y Autor (ej: Osamu Dazai - A Burglar in Spring): ").strip()
        parte = input(" 2. Archivo / Parte afectada (ej: splitter/.../es/part_01.txt): ").strip()
        
        print("\n Selecciona la categoría del issue:")
        print("  [1] Triangulación de reportes inconsistente (Grammar vs Sanity vs Markdown)")
        print("  [2] Falsos positivos severos en LanguageTool")
        print("  [3] Marcadores estructurales o formato roto")
        print("  [4] Error en ejecución de scripts / pipeline")
        print("  [5] Otro problema crítico")
        cat_opt = input(" Opción [1-5]: ").strip()

        categories = {
            "1": "Triangulación inconsistente de reportes",
            "2": "Falsos positivos de LanguageTool",
            "3": "Marcadores o formato roto",
            "4": "Error en scripts de ejecución",
            "5": "Problema general de auditoría"
        }
        categoria = categories.get(cat_opt, "Reporte de auditoría")

        print("\n 3. Explica el problema y qué reportes se contradicen:")
        print("    (Escribe el detalle y presiona Enter)")
        detalle = input("    > ").strip()

    except (KeyboardInterrupt, EOFError):
        cprint("\n[CANCELADO] Generación de reporte abortada.", COLOR_RED)
        return

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    timestamp_file = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_md = f"""🚨 **REPORTE DE ISSUE / TRIANGULACIÓN (epub-generator)**
📅 **Fecha**: {now_str}
👤 **Auditor**: Arodi / Agent Bridge
📚 **Obra / Autor**: {obra or 'No especificada'}
📄 **Archivo**: `{parte or 'N/A'}`
⚠️ **Categoría**: {categoria}

🔍 **Detalle del Problema / Contradicción**:
{detalle or 'Sin detalle adicional'}

🛑 **Estado**: En pausa esperando revisión en `#instrucciones-para-auditar`.
"""

    print("\n" + ("=" * 70))
    cprint("VISTA PREVIA DEL REPORTE PARA DISCORD:", COLOR_BOLD + COLOR_YELLOW)
    print("=" * 70)
    print(report_md)
    print("=" * 70)

    copied = copy_to_clipboard(report_md)
    if copied:
        cprint("✨ [OK] Reporte COPIADO al portapapeles de Windows.", COLOR_BOLD + COLOR_GREEN)
        cprint("   Puedes ir a Discord (#issues) y pegar con Ctrl+V.", COLOR_GREEN)
    else:
        cprint("[!] No se pudo copiar automáticamente. Puedes copiar el texto superior.", COLOR_YELLOW)

    # Guardar copia local en epub-generator/reports/issues/
    try:
        issues_dir = PROJECT_DIR / "reports" / "issues"
        issues_dir.mkdir(parents=True, exist_ok=True)
        report_path = issues_dir / f"issue_{timestamp_file}.md"
        report_path.write_text(report_md, encoding="utf-8")
        cprint(f"📁 Copia guardada localmente en: {report_path}", COLOR_CYAN)
    except Exception as ex:
        cprint(f"[!] No se pudo guardar la copia local: {ex}", COLOR_YELLOW)

    open_discord(show_info=False)

def audit_runner_flow() -> None:
    print_header("AUDITORÍA DE OBRAS / PARTES EN epub-generator", "Con control de pasos individual")
    
    print("Opciones de auditoría:")
    print(" [1] Ejecutar Grammar Checker sobre un archivo o directorio")
    print(" [2] Ejecutar Sanity Checker")
    print(" [3] Ejecutar Safe Join / Part Merger")
    print(" [4] Ejecutar Suite Completa (tools.audit_suite - 10 pasos)")
    print(" [5] Abrir terminal de Python en .venv")
    
    try:
        opt = input("\nSelecciona una opción [1-5]: ").strip()
    except (KeyboardInterrupt, EOFError):
        return

    if opt == "1":
        file_path = input("Ruta relativa o absoluta del archivo a auditar: ").strip()
        lang = input("Idioma (ej: es, pt, de, it) [es]: ").strip() or "es"
        if not file_path:
            cprint("[!] Ruta vacía.", COLOR_RED)
            return
        cmd = [PYTHON_EXE, "-m", "tools.grammar_checker", "-l", lang, file_path]
        run_project_command(cmd, f"Grammar Checker ({lang})", f"Verificación de gramática sobre {file_path}")

    elif opt == "2":
        file_path = input("Ruta del archivo para Sanity Check: ").strip()
        if not file_path:
            cprint("[!] Ruta vacía.", COLOR_RED)
            return
        cmd = [PYTHON_EXE, "-m", "tools.sanity_checker", file_path]
        run_project_command(cmd, "Sanity Checker", f"Chequeo de sanidad sobre {file_path}")

    elif opt == "3":
        cprint("Herramienta Safe Join de partes", COLOR_CYAN)
        cmd = [PYTHON_EXE, "tools/safe_join.py", "--help"]
        run_project_command(cmd, "Safe Join Helper", "Ver opciones de fusión segura de partes")

    elif opt == "4":
        cprint("Suite completa de auditoría (10 pasos automáticos)", COLOR_BOLD + COLOR_CYAN)
        cprint("Requiere libro fuente (--src), mergeado (--tgt) y partes (--src-parts, --tgt-parts)", COLOR_YELLOW)
        src = input("Ruta boock fuente (--src) [01translator/boocks/...]: ").strip()
        tgt = input("Ruta target mergeado (--tgt) [01translator/books-translated/...]: ").strip()
        src_lang = input("Idioma origen (--src-lang) [ja]: ").strip() or "ja"
        tgt_lang = input("Idioma destino (--tgt-lang) [es]: ").strip() or "es"
        book = input("Slug del libro (--book): ").strip()
        src_parts = input("Directorio partes fuente (--src-parts) [splitter/.../ja/]: ").strip()
        tgt_parts = input("Directorio partes destino (--tgt-parts) [splitter/.../es/]: ").strip()

        if not all([src, tgt, book, src_parts, tgt_parts]):
            cprint("[!] Faltan parámetros obligatorios.", COLOR_RED)
            return

        cmd = [
            PYTHON_EXE, "-m", "tools.audit_suite",
            "--src", src, "--tgt", tgt,
            "--src-lang", src_lang, "--tgt-lang", tgt_lang,
            "--book", book,
            "--src-parts", src_parts, "--tgt-parts", tgt_parts
        ]
        run_project_command(cmd, f"Suite de Auditoría Completa ({book})", "Ejecución de los 10 pasos automáticos")

    elif opt == "5":
        run_project_command([PYTHON_EXE], "Python Interactivo (.venv)", "Sesión interactiva")

def show_instructions_flow() -> None:
    print_header("INSTRUCCIONES PARA AUDITAR — REGLAS Y DISCORD", "Canal #instrucciones-para-auditar (epubs)")
    rules_file = ROOT_DIR / "docs" / "instrucciones_auditoria.md"
    if rules_file.exists():
        content = rules_file.read_text(encoding="utf-8", errors="replace")
        print(content)
    else:
        cprint("[!] No se encontró el archivo de instrucciones.", COLOR_RED)

    print()
    cprint("-" * 70, COLOR_CYAN)
    try:
        ans = input("¿Deseas registrar una nueva indicación de Discord (#instrucciones-para-auditar)? [s/N]: ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        return

    if ans in ["s", "si", "y", "yes"]:
        try:
            nueva_nota = input("\nEscribe o pega la indicación dada por Arodi:\n> ").strip()
        except (KeyboardInterrupt, EOFError):
            return

        if nueva_nota:
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            append_text = f"\n- **[{now_str}] (Arodi)**: {nueva_nota}\n"
            with open(rules_file, "a", encoding="utf-8") as f:
                f.write(append_text)
            cprint("\n[OK] Indicación guardada en instrucciones_auditoria.md", COLOR_GREEN)

def interactive_menu() -> None:
    while True:
        print_header("AGENT BRIDGE — epub-generator & Windows Scripts", "Puente interactivo de auditoría, control de pasos y Discord")
        cprint("Servidor Discord: 'epubs' | Canales: #instrucciones-para-auditar & #issues", COLOR_MAGENTA)
        print()
        print(" [1] 🎮 Abrir / Enfocar Discord (Servidor 'epubs')")
        print(" [2] 📜 Ver / Actualizar instrucciones de auditoría (#instrucciones-para-auditar)")
        print(" [3] 🔍 Ver estado de Git en epub-generator")
        print(" [4] 📄 Ver Diff detallado de cambios")
        print(" [5] 🛡️  Realizar Commit seguro (Aprobación estricta de Arodi)")
        print(" [6] 🛠️  Ejecutar Auditoría / Grammar / Suite (Paso a paso)")
        print(" [7] 🚨 Redactar y copiar reporte para canal #issues")
        print(" [8] ⚡ Ejecutar comando manual en epub-generator (con aprobación)")
        print(" [0] 🚪 Salir")
        print()

        try:
            choice = input(" Selecciona una opción [0-8]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if choice == "1":
            open_discord()
        elif choice == "2":
            show_instructions_flow()
        elif choice == "3":
            show_git_status()
        elif choice == "4":
            show_git_diff()
        elif choice == "5":
            safe_commit_flow()
        elif choice == "6":
            audit_runner_flow()
        elif choice == "7":
            create_issue_flow()
        elif choice == "8":
            cmd = input("Comando a ejecutar en epub-generator: ").strip()
            if cmd:
                run_project_command(cmd, "Comando manual", "Ejecución manual solicitada por el usuario")
        elif choice == "0":
            cprint("\nHasta luego.", COLOR_GREEN)
            break
        else:
            cprint("\n[!] Opción inválida.", COLOR_RED)

        try:
            input("\nPresiona Enter para continuar...")
        except (KeyboardInterrupt, EOFError):
            break

def main() -> None:
    args = sys.argv[1:]
    if not args:
        interactive_menu()
        return

    subcmd = args[0].lower()
    if subcmd in ["discord", "--discord"]:
        open_discord()
    elif subcmd in ["rules", "instructions", "instrucciones"]:
        show_instructions_flow()
    elif subcmd in ["status", "--status", "st"]:
        show_git_status()
    elif subcmd in ["diff", "--diff", "df"]:
        show_git_diff()
    elif subcmd in ["commit", "--commit", "ci"]:
        safe_commit_flow()
    elif subcmd in ["issue", "--issue", "report"]:
        create_issue_flow()
    elif subcmd in ["audit", "--audit"]:
        audit_runner_flow()
    elif subcmd in ["run", "--run"]:
        rest = " ".join(args[1:])
        if rest:
            run_project_command(rest, "Comando CLI", "Ejecutado vía 'agent run'")
        else:
            cprint("[!] Debes especificar el comando después de 'run'.", COLOR_RED)
    elif subcmd in ["help", "--help", "-h"]:
        print_header("AYUDA — AGENT BRIDGE (epub-generator)")
        print("Uso:")
        print("  agent              Abre el menú interactivo con todas las opciones.")
        print("  agent discord      Abre/enfoca Discord y muestra canales #instrucciones-para-auditar e #issues.")
        print("  agent instructions Muestra y registra instrucciones del canal #instrucciones-para-auditar.")
        print("  agent status       Muestra el estado de Git en epub-generator.")
        print("  agent diff         Muestra las diferencias pendientes.")
        print("  agent commit       Flujo de commit seguro (requiere aprobación obligatoria de Arodi).")
        print("  agent issue        Asistente guiado para redactar y copiar reportes a #issues.")
        print("  agent audit        Menú de auditoría (Grammar / Sanity checks con paso a paso).")
        print("  agent run <cmd>    Ejecuta un comando en epub-generator con confirmación previa.")
    else:
        cprint(f"[!] Subcomando desconocido: '{subcmd}'. Usa 'agent help' o 'agent' para el menú.", COLOR_RED)

if __name__ == "__main__":
    main()

"""
Location: C:/Users/Inicio/Proyectos/windows-scripts/core/branch_manager.py
Function: Branch inspector, switcher and documentation viewer for epub-generator from windows-scripts.
All Rights Reserved Arodi Emmanuel / Ismael (Agent Bridge)
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# Safe stdout encoding for Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CORE_DIR = Path(__file__).resolve().parent
ROOT_DIR = CORE_DIR.parent
PROJECT_DIR = (ROOT_DIR / ".." / "epub-generator").resolve()
DOCS_FILE = ROOT_DIR / "docs" / "branches_and_books_status.md"

COLOR_CYAN = "\033[96m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_MAGENTA = "\033[95m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"


def cprint(text: str, color: str = COLOR_RESET) -> None:
    if sys.platform == "win32" or os.isatty(sys.stdout.fileno()):
        print(f"{color}{text}{COLOR_RESET}")
    else:
        print(text)


BRANCH_DESCRIPTIONS = {
    "wip/workstation-migration-handoff": {
        "title": "Migración y Handoff 24/7 (Recomendada)",
        "content": (
            "• Dazai Lote 1 en Español (7 libros completos en 01translator/books-translated/)\n"
            "• Dazai Portugués (65 partes traducidas en splitter/ y 6 configs JSON)\n"
            "• Fixes del traductor Gemini (gem_browser, batch_handler, browser_launcher)\n"
            "• Prompts: remove-dazai-artifacts, search-markers, book-layout\n"
            "• Tests de puntuación y espaciado"
        ),
    },
    "translations/dazai-osamu-pt": {
        "title": "Traducciones PT Limpias (Dazai Osamu)",
        "content": (
            "• 65 partes traducidas en portugués (splitter/japon/dazai-osamu/*/pt/)\n"
            "• 6 archivos de configuración JSON del orquestador (lotes 1 al 5 y pt.json)\n"
            "• Historial limpio para entregas de portugués"
        ),
    },
    "main": {
        "title": "Rama Troncal Upstream (Arodi)",
        "content": (
            "• Obras en alemán de Dazai Osamu (Righteousness and Smiles, Regretful Parting)\n"
            "• Catálogo histórico de autores y metadatos globales\n"
            "• Código base de producción"
        ),
    },
    "feature/multi-language-epub-support": {
        "title": "Soporte Multi-Idioma y Oda Sakunosuke",
        "content": (
            "• EPUBs y metadatos de Oda Sakunosuke (Lady of Saturday)\n"
            "• Mejoras del generador multi-idioma"
        ),
    },
}


def run_git(args: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    target_cwd = cwd or PROJECT_DIR
    if not target_cwd.exists():
        return 1, "", f"Directorio no encontrado: {target_cwd}"
    try:
        r = subprocess.run(
            ["git"] + args,
            cwd=str(target_cwd),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except Exception as e:
        return 1, "", str(e)


def check_project_exists() -> bool:
    if not PROJECT_DIR.exists() or not (PROJECT_DIR / ".git").exists():
        cprint(f"[!] No se encontró el repositorio epub-generator en: {PROJECT_DIR}", COLOR_YELLOW)
        return False
    return True


def get_current_branch() -> str:
    rc, out, _ = run_git(["branch", "--show-current"])
    if rc == 0 and out:
        return out
    rc, out, _ = run_git(["rev-parse", "--short", "HEAD"])
    return out if rc == 0 else "desconocida"


def list_branches() -> None:
    if not check_project_exists():
        return

    current = get_current_branch()
    cprint("=" * 75, COLOR_CYAN)
    cprint("          ESTADO DE RAMAS Y LIBROS EN EPUB-GENERATOR", COLOR_BOLD + COLOR_CYAN)
    cprint("=" * 75, COLOR_CYAN)
    print()
    cprint(f"Rama activa actual: {COLOR_BOLD}{COLOR_GREEN}{current}{COLOR_RESET}")
    print()

    # Obtener ramas locales y remotas
    run_git(["fetch", "origin", "--quiet"])
    _, out, _ = run_git(["branch", "-a"])
    branches = set()
    for line in out.splitlines():
        line = line.strip().replace("*", "").strip()
        if "->" in line:
            continue
        if line.startswith("remotes/origin/"):
            line = line[len("remotes/origin/"):]
        branches.add(line)

    for b in sorted(branches):
        info = BRANCH_DESCRIPTIONS.get(b, {"title": "Rama adicional", "content": "• Sin descripción registrada"})
        prefix = f"{COLOR_BOLD}{COLOR_GREEN}▶ [ACTIVA] {b}{COLOR_RESET}" if b == current else f"{COLOR_BOLD}{COLOR_YELLOW}  {b}{COLOR_RESET}"
        print(f"{prefix} — {COLOR_MAGENTA}{info['title']}{COLOR_RESET}")
        for c_line in info["content"].splitlines():
            print(f"    {c_line}")
        print()

    cprint("=" * 75, COLOR_CYAN)
    cprint(f"Documentación detallada en: {DOCS_FILE}", COLOR_CYAN)


def switch_branch(target: str) -> bool:
    if not check_project_exists():
        return False

    cprint(f"Sincronizando y cambiando a la rama '{target}'...", COLOR_CYAN)
    run_git(["fetch", "origin"])

    rc, _, err = run_git(["checkout", target])
    if rc != 0:
        # Intentar crear tracking local si solo existe en remoto
        rc, _, err = run_git(["checkout", "-b", target, f"origin/{target}"])

    if rc == 0:
        cprint(f"[OK] Ahora estás en la rama: {target}", COLOR_BOLD + COLOR_GREEN)
        return True
    else:
        cprint(f"[ERROR] No se pudo cambiar a '{target}': {err}", COLOR_RED)
        return False


def show_docs() -> None:
    if DOCS_FILE.exists():
        content = DOCS_FILE.read_text(encoding="utf-8", errors="replace")
        print(content)
    else:
        cprint(f"[!] Archivo de documentación no encontrado: {DOCS_FILE}", COLOR_RED)


def interactive_menu() -> None:
    list_branches()
    print()
    print("Opciones de cambio rápido:")
    print(" [1] Cambiar a wip/workstation-migration-handoff (Recomendado 24/7)")
    print(" [2] Cambiar a translations/dazai-osamu-pt (Lote Portugués)")
    print(" [3] Cambiar a main (Upstream Arodi)")
    print(" [4] Ver documento completo de estado (.md)")
    print(" [5] Salir")
    print()
    choice = input("Selecciona una opción [1-5]: ").strip()

    if choice == "1":
        switch_branch("wip/workstation-migration-handoff")
    elif choice == "2":
        switch_branch("translations/dazai-osamu-pt")
    elif choice == "3":
        switch_branch("main")
    elif choice == "4":
        show_docs()
    elif choice == "5":
        return
    else:
        cprint("[!] Opción inválida.", COLOR_RED)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd in ("list", "--list", "-l"):
            list_branches()
        elif cmd in ("doc", "--doc", "docs", "--docs"):
            show_docs()
        elif cmd in ("switch", "--switch", "checkout", "-s") and len(sys.argv) > 2:
            switch_branch(sys.argv[2])
        elif cmd.startswith("wip/") or cmd.startswith("translations/") or cmd == "main":
            switch_branch(cmd)
        else:
            cprint(f"Uso: python branch_manager.py [list | doc | switch <rama>]", COLOR_YELLOW)
    else:
        interactive_menu()

"""
Location: C:/Users/Inicio/Proyectos/windows-scripts/core/alias_manager.py
Function: Portable cross-machine alias manager and exporter for CMD, PowerShell and PATH.
All Rights Reserved Arodi Emmanuel
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
BIN_DIR = ROOT_DIR / "bin"
ALIASES_DIR = ROOT_DIR / "aliases"
CONFIG_FILE = ALIASES_DIR / "custom_aliases.json"
AUTORUN_BAT = Path(os.path.expandvars(r"%USERPROFILE%\cmd_aliases.bat"))
IDE_BIN = Path(os.path.expandvars(r"%LOCALAPPDATA%\Programs\Antigravity IDE\bin"))

BUILTIN_COMMANDS = {
    "ag", "ag.", "agy", "antigravity", "antigravity-ide",
    "epub", "epub-generator", "orch", "orchestrator",
    "unlock", "agent", "alias", "ls", "ll", "clear", "which",
    "add-alias", "export-alias", "export-aliases", "sync-aliases"
}


def ensure_dirs() -> None:
    BIN_DIR.mkdir(parents=True, exist_ok=True)
    ALIASES_DIR.mkdir(parents=True, exist_ok=True)


def load_custom_aliases() -> dict[str, dict]:
    ensure_dirs()
    if not CONFIG_FILE.exists():
        return {}
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("aliases", {})
    except Exception as e:
        print(f"[!] Error leyendo {CONFIG_FILE}: {e}", file=sys.stderr)
        return {}


def save_custom_aliases(aliases: dict[str, dict]) -> None:
    ensure_dirs()
    payload = {
        "_description": "Alias personalizados portables sincronizados mediante windows-scripts",
        "aliases": aliases,
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def to_portable_target(target_path: Path) -> str:
    """Convert absolute path to a portable representation relative to ROOT_DIR parent or USERPROFILE."""
    target_path = target_path.resolve()
    parent_of_root = ROOT_DIR.parent.resolve()
    try:
        # e.g. C:/Users/.../Proyectos/miweb relative to C:/Users/.../Proyectos -> ../miweb
        rel = target_path.relative_to(parent_of_root)
        return f"..\\{rel}"
    except ValueError:
        pass

    user_profile = Path(os.path.expandvars(r"%USERPROFILE%")).resolve()
    try:
        rel = target_path.relative_to(user_profile)
        return f"%USERPROFILE%\\{rel}"
    except ValueError:
        pass

    return str(target_path)


def resolve_portable_target(target_str: str) -> Path:
    """Resolve portable representation to current machine's absolute Path."""
    if target_str.startswith("..\\") or target_str.startswith("../"):
        return (ROOT_DIR / target_str).resolve()
    if "%USERPROFILE%" in target_str.upper():
        expanded = os.path.expandvars(target_str)
        return Path(expanded).resolve()
    return Path(target_str).resolve()


def create_orch_cmd() -> None:
    content = (
        "@echo off\r\n"
        "setlocal\r\n"
        "set \"BIN_DIR=%~dp0\"\r\n"
        "set \"ROOT_DIR=%BIN_DIR%..\"\r\n"
        "set \"PROJECT_DIR=%ROOT_DIR%\\..\\epub-generator\"\r\n"
        "cd /d \"%PROJECT_DIR%\"\r\n"
        "if exist \".venv\\Scripts\\python.exe\" (\r\n"
        "    \".venv\\Scripts\\python.exe\" -m amazon_publisher.translator.orchestrator %*\r\n"
        ") else (\r\n"
        "    python -m amazon_publisher.translator.orchestrator %*\r\n"
        ")\r\n"
    )
    (BIN_DIR / "orch.cmd").write_text(content, encoding="utf-8")


def create_unlock_cmd() -> None:
    content = (
        "@echo off\r\n"
        "setlocal\r\n"
        "set \"BIN_DIR=%~dp0\"\r\n"
        "set \"ROOT_DIR=%BIN_DIR%..\"\r\n"
        "set \"STATE_DIR=%ROOT_DIR%\\..\\epub-generator\\amazon_publisher\\translator\\orchestrator\\state\"\r\n"
        "if exist \"%STATE_DIR%\" (\r\n"
        "    del /f /q \"%STATE_DIR%\\*.lock\" 2>nul\r\n"
        "    echo [OK] Archivos .lock eliminados de %STATE_DIR%\r\n"
        ") else (\r\n"
        "    echo [!] Carpeta de estado no encontrada: %STATE_DIR%\r\n"
        ")\r\n"
    )
    (BIN_DIR / "unlock.cmd").write_text(content, encoding="utf-8")


def create_epub_cmd() -> None:
    content = (
        "@echo off\r\n"
        "setlocal\r\n"
        "set \"BIN_DIR=%~dp0\"\r\n"
        "set \"ROOT_DIR=%BIN_DIR%..\"\r\n"
        "set \"PROJECT_DIR=%ROOT_DIR%\\..\\epub-generator\"\r\n"
        "cd /d \"%PROJECT_DIR%\"\r\n"
        "where.exe antigravity-ide >nul 2>&1\r\n"
        "if %ERRORLEVEL% EQU 0 (\r\n"
        "    call antigravity-ide . 2>nul\r\n"
        ") else (\r\n"
        "    explorer .\r\n"
        ")\r\n"
    )
    (BIN_DIR / "epub.cmd").write_text(content, encoding="utf-8")


def create_agent_cmd() -> None:
    content = (
        "@echo off\r\n"
        "call \"%~dp0..\\agent.bat\" %*\r\n"
    )
    (BIN_DIR / "agent.cmd").write_text(content, encoding="utf-8")


def create_ag_cmd() -> None:
    content = (
        "@echo off\r\n"
        "where.exe antigravity-ide >nul 2>&1\r\n"
        "if %ERRORLEVEL% EQU 0 (\r\n"
        "    if \"%~1\"==\"\" (\r\n"
        "        call antigravity-ide . 2>nul\r\n"
        "    ) else (\r\n"
        "        call antigravity-ide %* 2>nul\r\n"
        "    )\r\n"
        ") else (\r\n"
        "    if \"%~1\"==\"\" (\r\n"
        "        explorer .\r\n"
        "    ) else (\r\n"
        "        if exist \"%~1\" (\r\n"
        "            cd /d \"%~1\"\r\n"
        "        ) else (\r\n"
        "            explorer .\r\n"
        "        )\r\n"
        "    )\r\n"
        ")\r\n"
    )
    (BIN_DIR / "ag.cmd").write_text(content, encoding="utf-8")


def create_add_alias_cmd() -> None:
    content = (
        "@echo off\r\n"
        "setlocal\r\n"
        "set \"SCRIPT_DIR=%~dp0..\"\r\n"
        "set \"PY_CMD=python\"\r\n"
        "if exist \"%SCRIPT_DIR%\\..\\epub-generator\\.venv\\Scripts\\python.exe\" (\r\n"
        "    set \"PY_CMD=%SCRIPT_DIR%\\..\\epub-generator\\.venv\\Scripts\\python.exe\"\r\n"
        ")\r\n"
        "\"%PY_CMD%\" \"%SCRIPT_DIR%\\core\\alias_manager.py\" add %*\r\n"
    )
    (BIN_DIR / "add-alias.cmd").write_text(content, encoding="utf-8")


def create_export_alias_cmd() -> None:
    content = (
        "@echo off\r\n"
        "setlocal\r\n"
        "set \"SCRIPT_DIR=%~dp0..\"\r\n"
        "set \"PY_CMD=python\"\r\n"
        "if exist \"%SCRIPT_DIR%\\..\\epub-generator\\.venv\\Scripts\\python.exe\" (\r\n"
        "    set \"PY_CMD=%SCRIPT_DIR%\\..\\epub-generator\\.venv\\Scripts\\python.exe\"\r\n"
        ")\r\n"
        "\"%PY_CMD%\" \"%SCRIPT_DIR%\\core\\alias_manager.py\" export %*\r\n"
    )
    (BIN_DIR / "export-aliases.cmd").write_text(content, encoding="utf-8")


def create_custom_cmd(name: str, target_portable: str) -> None:
    content = (
        "@echo off\r\n"
        "setlocal\r\n"
        "set \"BIN_DIR=%~dp0\"\r\n"
        "set \"ROOT_DIR=%BIN_DIR%..\"\r\n"
        f"set \"PORTABLE_TARGET={target_portable}\"\r\n"
        "if \"%PORTABLE_TARGET:~0,3%\"==\"..\\\" (\r\n"
        "    set \"RESOLVED_TARGET=%ROOT_DIR%\\%PORTABLE_TARGET%\"\r\n"
        ") else (\r\n"
        "    set \"RESOLVED_TARGET=%PORTABLE_TARGET%\"\r\n"
        ")\r\n"
        "cd /d \"%RESOLVED_TARGET%\"\r\n"
        "where.exe antigravity-ide >nul 2>&1\r\n"
        "if %ERRORLEVEL% EQU 0 (\r\n"
        "    call antigravity-ide . 2>nul\r\n"
        ") else (\r\n"
        "    explorer .\r\n"
        ")\r\n"
    )
    (BIN_DIR / f"{name}.cmd").write_text(content, encoding="utf-8")


def add_bin_to_user_path() -> None:
    """Ensure windows-scripts/bin is in the user's PATH environment variable."""
    bin_str = str(BIN_DIR.resolve())
    ps_cmd = (
        f"$b = '{bin_str}'; "
        "$u = [Environment]::GetEnvironmentVariable('Path', 'User'); "
        "if ($u -notlike '*' + $b + '*') { "
        "    [Environment]::SetEnvironmentVariable('Path', ($u.TrimEnd(';') + ';' + $b), 'User') "
        "}"
    )
    try:
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=False, capture_output=True)
    except Exception:
        pass


def copy_to_ide_bin() -> None:
    """Sync all .cmd from windows-scripts/bin to Antigravity IDE bin if it exists."""
    if IDE_BIN.exists():
        for cmd_file in BIN_DIR.glob("*.cmd"):
            try:
                dest = IDE_BIN / cmd_file.name
                dest.write_text(cmd_file.read_text(encoding="utf-8"), encoding="utf-8")
            except Exception:
                pass


def update_autorun_bat(custom_aliases: dict[str, dict]) -> None:
    """Update %USERPROFILE%\cmd_aliases.bat with built-in and custom aliases."""
    project_dir = (ROOT_DIR / ".." / "epub-generator").resolve()
    lines = [
        "@echo off",
        ":: ====================================================================",
        ":: Macros y Alias estilo Linux para CMD (Sincronizados con windows-scripts)",
        ":: ====================================================================",
        "doskey ag=antigravity-ide $*",
        "doskey ag.=antigravity-ide .",
        "doskey agy=antigravity-ide $*",
        "doskey antigravity=antigravity-ide $*",
        f'doskey epub=cd /d "{project_dir}" $T antigravity-ide .',
        f'doskey epub-generator=cd /d "{project_dir}" $T antigravity-ide .',
        f'doskey orch=cd /d "{project_dir}" $T .venv\\Scripts\\python.exe -m amazon_publisher.translator.orchestrator $*',
        f'doskey orchestrator=cd /d "{project_dir}" $T .venv\\Scripts\\python.exe -m amazon_publisher.translator.orchestrator $*',
        f'doskey unlock=del /f /q "{project_dir}\\amazon_publisher\\translator\\orchestrator\\state\\*.lock" 2^>nul',
        f'doskey agent="{ROOT_DIR}\\agent.bat" $*',
        "doskey alias=doskey $*",
        "doskey ls=dir /b /o:gn $*",
        "doskey ll=dir /o:gn $*",
        "doskey clear=cls",
        "doskey which=where.exe $*",
    ]

    for name, item in custom_aliases.items():
        portable = item.get("portable", "")
        resolved = resolve_portable_target(portable)
        lines.append(f'doskey {name}=cd /d "{resolved}" $T antigravity-ide .')

    AUTORUN_BAT.write_text("\r\n".join(lines) + "\r\n", encoding="utf-8")

    # Ensure AutoRun in registry
    reg_cmd = [
        "reg", "add", r"HKCU\Software\Microsoft\Command Processor",
        "/v", "AutoRun", "/t", "REG_SZ", "/d", f'"{AUTORUN_BAT}"', "/f"
    ]
    try:
        subprocess.run(reg_cmd, check=False, capture_output=True)
    except Exception:
        pass


def update_powershell_profile(custom_aliases: dict[str, dict]) -> None:
    project_dir = (ROOT_DIR / ".." / "epub-generator").resolve()
    funcs = [
        f'function orch {{ Set-Location "{project_dir}"; & ".venv\\Scripts\\python.exe" -m amazon_publisher.translator.orchestrator $args }}',
        f'function unlock {{ Remove-Item -Path "{project_dir}\\amazon_publisher\\translator\\orchestrator\\state\\*.lock" -Force -ErrorAction SilentlyContinue; Write-Host "[OK] Locks removidos" }}',
        f'function epub {{ Set-Location "{project_dir}" }}',
        f'function agent {{ & "{ROOT_DIR}\\agent.bat" $args }}',
    ]
    for name, item in custom_aliases.items():
        resolved = resolve_portable_target(item.get("portable", ""))
        funcs.append(f'function {name} {{ Set-Location "{resolved}" }}')

    block = "\n".join(funcs)
    ps_cmd = (
        "$prof = $PROFILE; "
        "$dir = Split-Path -Parent $prof; "
        "if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }; "
        f"$block = '{block}'; "
        "if (Test-Path $prof) { "
        "    if ((Get-Content $prof -Raw) -notmatch 'orch') { "
        "        Add-Content -Path $prof -Value (\"`n\" + $block) "
        "    } "
        "} else { "
        "    Set-Content -Path $prof -Value $block -Encoding UTF8 "
        "}"
    )
    try:
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=False, capture_output=True)
    except Exception:
        pass


def apply_all() -> None:
    """Regenerate all launchers, CMD macros, PowerShell profile and PATH."""
    ensure_dirs()
    create_orch_cmd()
    create_unlock_cmd()
    create_epub_cmd()
    create_agent_cmd()
    create_ag_cmd()
    create_add_alias_cmd()
    create_export_alias_cmd()

    custom_aliases = load_custom_aliases()
    for name, item in custom_aliases.items():
        portable = item.get("portable", "")
        create_custom_cmd(name, portable)

    add_bin_to_user_path()
    copy_to_ide_bin()
    update_autorun_bat(custom_aliases)
    update_powershell_profile(custom_aliases)
    print(f"[OK] {len(custom_aliases)} alias personalizados aplicados exitosamente.")


def add_alias(name: str, target: str | None = None) -> None:
    ensure_dirs()
    name = name.strip().lower()
    if not name:
        print("[!] El nombre del alias no puede estar vacio.", file=sys.stderr)
        sys.exit(1)

    if not target or target.strip() == "":
        target_path = Path.cwd()
    else:
        target_path = Path(target.strip())
        if not target_path.is_absolute():
            target_path = (Path.cwd() / target_path).resolve()

    portable = to_portable_target(target_path)
    aliases = load_custom_aliases()
    aliases[name] = {
        "portable": portable,
        "original_path": str(target_path.resolve()),
    }
    save_custom_aliases(aliases)
    apply_all()
    print("=" * 68)
    print(f" [OK] Alias '{name}' creado y guardado en el repositorio!")
    print(f"      Ruta portable: {portable}")
    print(f"      Ruta actual:   {target_path}")
    print("=" * 68)
    print(f"Este alias ya queda guardado en {CONFIG_FILE.name} para exportar")
    print("a cualquier otro equipo con 'setup_all.bat --all' o 'setup_all.bat --aliases'!")
    print("=" * 68)


def export_aliases() -> None:
    """Scan existing CMD / IDE aliases on this computer and save into custom_aliases.json."""
    ensure_dirs()
    aliases = load_custom_aliases()
    found = 0

    # 1. Scan IDE_BIN if exists
    if IDE_BIN.exists():
        for cmd_file in IDE_BIN.glob("*.cmd"):
            name = cmd_file.stem.lower()
            if name in BUILTIN_COMMANDS:
                continue
            # Read script to find target directory
            text = cmd_file.read_text(encoding="utf-8", errors="ignore")
            for line in text.splitlines():
                line = line.strip()
                if line.lower().startswith("cd /d "):
                    raw_path = line[6:].strip().strip('"')
                    if raw_path and raw_path != "%RESOLVED_TARGET%":
                        p = Path(raw_path)
                        aliases[name] = {
                            "portable": to_portable_target(p),
                            "original_path": str(p),
                        }
                        found += 1
                    break

    save_custom_aliases(aliases)
    apply_all()
    print("=" * 68)
    print(f" [OK] Exportacion completada: {len(aliases)} alias registrados en el repositorio.")
    print(f"      Archivo: {CONFIG_FILE}")
    print(f"      Carpeta bin portable: {BIN_DIR}")
    print("=" * 68)


def list_aliases() -> None:
    custom = load_custom_aliases()
    print("=" * 68)
    print(" ALIAS DISPONIBLES EN ESTE EQUIPO (Y EXPORTABLES)")
    print("=" * 68)
    print("\nComandos de sistema y herramientas:")
    print("  orch <config>       -> Lanzador del orquestador de traduccion")
    print("  unlock              -> Limpiador de bloqueos (.lock) huerfanos")
    print("  epub                -> Carpeta raiz de epub-generator")
    print("  agent               -> Interfaz del Agent Bridge / auditorias")
    print("  ag [ruta]           -> Abrir en Antigravity IDE")
    print("  add-alias <nom> [p] -> Crear nuevo alias y guardarlo en el repo")
    print("  export-aliases      -> Exportar todos los alias al repositorio")

    if custom:
        print("\nAlias personalizados guardados en el repositorio:")
        for name, item in sorted(custom.items()):
            portable = item.get("portable", "")
            resolved = resolve_portable_target(portable)
            exists = "[OK]" if resolved.exists() else "[NO EXISTE AUN]"
            print(f"  {name:<16} -> {portable:<20} {exists} ({resolved})")
    else:
        print("\n(No hay alias personalizados adicionales creados todavia)")
    print("=" * 68)


def main() -> None:
    if len(sys.argv) < 2:
        list_aliases()
        return

    cmd = sys.argv[1].lower()
    if cmd in ("apply", "--apply"):
        apply_all()
    elif cmd in ("add", "--add"):
        if len(sys.argv) < 3:
            print("Uso: python alias_manager.py add <nombre> [ruta]", file=sys.stderr)
            sys.exit(1)
        name = sys.argv[2]
        target = sys.argv[3] if len(sys.argv) > 3 else None
        add_alias(name, target)
    elif cmd in ("export", "--export"):
        export_aliases()
    elif cmd in ("list", "--list"):
        list_aliases()
    else:
        # Default fallback: treat as add
        add_alias(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)


if __name__ == "__main__":
    main()

"""
Location: C:/Users/Inicio/Proyectos/windows-scripts/core/fix_antigravity_ide.py
Function: Previene la apertura de doble ventana en Antigravity IDE (VS Code) y
          restaura la visibilidad y persistencia del panel del agente y sus historiales.
All Rights Reserved Arodi Emmanuel
"""
from __future__ import annotations

import json
import os
import sqlite3
import sys
from pathlib import Path


def fix_antigravity_ide() -> bool:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        print("[!] No se encontró la variable de entorno APPDATA.", file=sys.stderr)
        return False

    ide_dir = Path(appdata) / "Antigravity IDE"
    user_dir = ide_dir / "User"
    settings_file = user_dir / "settings.json"
    workspace_storage = user_dir / "workspaceStorage"
    global_storage = user_dir / "globalStorage"
    storage_json = global_storage / "storage.json"

    print("=== APLICANDO CORRECCIÓN PARA ANTIGRAVITY IDE ===")
    user_dir.mkdir(parents=True, exist_ok=True)

    # 1. Configurar settings.json
    settings = {}
    if settings_file.exists():
        try:
            with open(settings_file, "r", encoding="utf-8-sig") as f:
                settings = json.load(f)
        except Exception as e:
            print(f"[!] Aviso al leer {settings_file}: {e}. Se creará uno limpio.")
            settings = {}

    target_settings = {
        "window.openWithoutArgumentsInNewWindow": "off",
        "window.restoreWindows": "one",
        "window.openFoldersInNewWindow": "off",
        "window.newWindowDimensions": "inherit",
        "workbench.editor.restoreViewState": True,
    }

    settings.update(target_settings)

    try:
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
        print(f"[OK] settings.json actualizado exitosamente en {settings_file}")
        print("     - Ventana única sin argumentos: 'off'")
        print("     - Restaurar último directorio: 'one'")
        print("     - Reutilizar ventana al abrir carpetas: 'off'")
    except Exception as e:
        print(f"[!] Error al escribir {settings_file}: {e}", file=sys.stderr)
        return False

    # 2. Desocultar panel de agente en workspaceStorage
    if workspace_storage.exists():
        vscdb_files = list(workspace_storage.glob("*/state.vscdb"))
        for vscdb in vscdb_files:
            try:
                conn = sqlite3.connect(vscdb)
                cur = conn.cursor()
                cur.execute(
                    "SELECT value FROM ItemTable WHERE key = 'antigravity.agentViewContainerId.state'"
                )
                row = cur.fetchone()
                if row:
                    try:
                        data = json.loads(row[0])
                        panel = data.get("antigravity.agentSidePanel", {})
                        if panel.get("isHidden") is True:
                            panel["isHidden"] = False
                            data["antigravity.agentSidePanel"] = panel
                            cur.execute(
                                "UPDATE ItemTable SET value = ? WHERE key = 'antigravity.agentViewContainerId.state'",
                                (json.dumps(data),),
                            )
                            conn.commit()
                            print(f"[OK] Panel del agente desocultado en: {vscdb.parent.name}")
                    except Exception:
                        pass
                conn.close()
            except Exception as e:
                print(f"[!] Aviso al inspeccionar {vscdb}: {e}")

    # 3. Limpiar storage.json de ventanas fantasma
    if storage_json.exists():
        try:
            with open(storage_json, "r", encoding="utf-8-sig") as f:
                storage_data = json.load(f)
            ws_state = storage_data.get("windowsState", {})
            if ws_state.get("openedWindows"):
                ws_state["openedWindows"] = []
                with open(storage_json, "w", encoding="utf-8") as f:
                    json.dump(storage_data, f, indent=4, ensure_ascii=False)
                print("[OK] Ventanas fantasma limpiadas en storage.json.")
        except Exception as e:
            print(f"[!] Aviso al limpiar storage.json: {e}")

    print("[EXITO] Corrección de Antigravity IDE aplicada correctamente.")
    return True


if __name__ == "__main__":
    success = fix_antigravity_ide()
    sys.exit(0 if success else 1)

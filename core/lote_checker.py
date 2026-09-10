"""
Location: C:/Users/Inicio/Proyectos/windows-scripts/core/lote_checker.py
Function: Lote auditor and translation status inspector for epub-generator without modifying Git repository.
All Rights Reserved Arodi Emmanuel / Ismael (Agent Bridge)
"""

import sys
import os
from pathlib import Path

# Safe stdout encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CORE_DIR = Path(__file__).resolve().parent
ROOT_DIR = CORE_DIR.parent
PROJECT_DIR = (ROOT_DIR / ".." / "epub-generator").resolve()

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

def inspect_lote(lote_num: int = 1) -> dict:
    lote_file = PROJECT_DIR / "TODO" / f"dazai-lote-{lote_num}.md"
    if not lote_file.exists():
        cprint(f"[ERROR] No se encontró el archivo {lote_file}", COLOR_RED)
        return {}

    splitter_base = PROJECT_DIR / "splitter" / "japon" / "dazai-osamu"
    boocks_base = PROJECT_DIR / "01translator" / "boocks" / "japon" / "dazai-osamu"
    translated_base = PROJECT_DIR / "01translator" / "books-translated" / "japon" / "dazai-osamu" / "es" / f"lote-{lote_num}"
    reports_base = PROJECT_DIR / "reports"
    bitacora_base = reports_base / "bitacora"

    lines = lote_file.read_text(encoding="utf-8", errors="replace").splitlines()
    items = []

    for line in lines:
        line_clean = line.strip()
        if not line_clean or line_clean.startswith("#"):
            continue
        parts = line_clean.split("\t")
        if len(parts) >= 3 and parts[0].isdigit():
            idx = int(parts[0])
            slug = parts[1].strip()
            title = parts[2].strip()

            # 1. Splitter check
            ja_dir = splitter_base / slug / "ja"
            es_dir = splitter_base / slug / "es"
            ja_parts = len([f for f in ja_dir.glob("part_*.txt")]) if ja_dir.exists() else 0
            es_parts = len([f for f in es_dir.glob("part_*.txt")]) if es_dir.exists() else 0

            # 2. Merged check
            merged_file = translated_base / f"{slug}.txt"
            merged_exists = merged_file.exists()
            merged_size = merged_file.stat().st_size if merged_exists else 0

            # 3. Boock source check
            boock_candidates = list(boocks_base.glob(f"{slug}*.txt")) if boocks_base.exists() else []
            boock_file = boock_candidates[0] if boock_candidates else None

            # 4. Audit & Bitacora check
            has_bitacora = False
            slug_normalized = slug.replace("-", "_")
            if bitacora_base.exists():
                for b_file in bitacora_base.glob("*.md"):
                    b_name = b_file.name.lower()
                    if slug in b_name or slug_normalized in b_name:
                        has_bitacora = True
                        break

            audit_dir = reports_base / "dazai-osamu" / slug
            has_audit = audit_dir.exists() and len(list(audit_dir.glob("*.txt"))) > 0

            items.append({
                "idx": idx,
                "slug": slug,
                "title": title,
                "ja_parts": ja_parts,
                "es_parts": es_parts,
                "trans_ok": ja_parts > 0 and ja_parts == es_parts,
                "merged": merged_exists,
                "size": merged_size,
                "boock": boock_file,
                "audited": has_audit or has_bitacora,
                "bitacora": has_bitacora,
            })

    return {
        "lote_num": lote_num,
        "total": len(items),
        "items": items,
        "translated_base": translated_base,
    }

def print_lote_report(data: dict) -> None:
    if not data:
        return
    lote_num = data["lote_num"]
    items = data["items"]

    sep = "=" * 80
    cprint(sep, COLOR_CYAN)
    cprint(f"   DIAGNÓSTICO COMPLETO: OSAMU DAZAI — LOTE {lote_num} (TODO/dazai-lote-{lote_num}.md)", COLOR_BOLD + COLOR_CYAN)
    cprint("   Modo Seguro: Solo inspección y orquestación sin tocar el repo de Arodi", COLOR_YELLOW)
    cprint(sep, COLOR_CYAN)
    print()

    cprint(f"{'#':<3} | {'Slug':<35} | {'JA/ES':<7} | {'Traducción':<11} | {'Merge':<8} | {'Auditoría'}", COLOR_BOLD)
    cprint("-" * 80, COLOR_CYAN)

    missing_trans = []
    missing_merge = []
    missing_audit = []
    all_ready = []

    for it in items:
        # Traduccion
        if it["trans_ok"]:
            trans_str = f"{COLOR_GREEN}100% OK{COLOR_RESET}"
        elif it["es_parts"] > 0:
            trans_str = f"{COLOR_YELLOW}{it['es_parts']}/{it['ja_parts']}{COLOR_RESET}"
            missing_trans.append(it)
        else:
            trans_str = f"{COLOR_RED}0/{it['ja_parts']}{COLOR_RESET}"
            missing_trans.append(it)

        # Merge
        if it["merged"]:
            merge_str = f"{COLOR_GREEN}LISTO{COLOR_RESET}"
        else:
            merge_str = f"{COLOR_YELLOW}PENDIENTE{COLOR_RESET}"
            missing_merge.append(it)

        # Auditoria
        if it["bitacora"]:
            audit_str = f"{COLOR_GREEN}ENTREGADO (#bitácora){COLOR_RESET}"
        elif it["audited"]:
            audit_str = f"{COLOR_CYAN}AUDITADO{COLOR_RESET}"
        else:
            audit_str = f"{COLOR_YELLOW}PENDIENTE{COLOR_RESET}"
            missing_audit.append(it)

        parts_ratio = f"{it['ja_parts']}/{it['es_parts']}"
        print(f"{it['idx']:<3} | {it['slug']:<35} | {parts_ratio:<7} | {trans_str:<20} | {merge_str:<17} | {audit_str}")

    cprint("-" * 80, COLOR_CYAN)
    print()
    cprint(f"📊 RESUMEN DEL LOTE {lote_num}:", COLOR_BOLD + COLOR_MAGENTA)
    print(f" • Total de obras en catálogo:    {data['total']}")
    print(f" • Traducción 100% completa:     {data['total'] - len(missing_trans)} / {data['total']}")
    print(f" • Traducciones faltantes:        {len(missing_trans)}")
    print(f" • Concatenadas en lote-{lote_num}:       {data['total'] - len(missing_merge)} / {data['total']}")
    print(f" • Pendientes de concatenación:   {len(missing_merge)}")
    print(f" • Pendientes de auditoría:       {len(missing_audit)}")
    print()

    if missing_trans:
        cprint("⚠️  OBRAS QUE REQUIEREN TRADUCCIÓN:", COLOR_BOLD + COLOR_RED)
        for m in missing_trans:
            print(f"   - #{m['idx']} {m['slug']} ({m['title']}): {m['es_parts']}/{m['ja_parts']} partes")
        print()
    else:
        cprint("✨ ¡TODAS las obras del Lote tienen su traducción al 100% en splitter/!", COLOR_BOLD + COLOR_GREEN)
        print()

    if missing_merge:
        cprint("📥 OBRAS LISTAS PARA CONCATENAR (Paso 2):", COLOR_BOLD + COLOR_YELLOW)
        for m in missing_merge:
            print(f"   - #{m['idx']} {m['slug']} ({m['title']}) [{m['es_parts']} partes]")
        print()

    if missing_audit:
        cprint(f"🔍 OBRAS PENDIENTES DE AUDITORÍA (Paso 3): {len(missing_audit)} obras", COLOR_BOLD + COLOR_CYAN)
        print()

if __name__ == "__main__":
    lote = 1
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        lote = int(sys.argv[1])
    data = inspect_lote(lote)
    print_lote_report(data)

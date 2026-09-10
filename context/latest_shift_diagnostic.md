# DIAGNÓSTICO DE TURNO Y CONTEXTO OPERATIVO — Agent Bridge (windows-scripts)
Fecha: 2026-09-09 17:47
Auditor: Arodi / Ismael (Agent Bridge)

---

### 1. Canales Oficiales en Servidor Discord 'epubs' y Reglas de Automatización

En el servidor de Discord **`epubs`**, los canales de trabajo son:
1. **`# en-turno`**: Backlog oficial de prioridades definido por Arodi (los 5 lotes de Osamu Dazai).
2. **`# instrucciones-para-aduitar`** (⚠️ **con la grafía exacta `aduitar`**):
   - Flujo de trabajo oficial (pasos 0 a 8) y reglas de calidad.
   - Regla 3.1: Prohibido aplicar cambios semánticos en lote.
   - Regla 3.2: En `06 dash_check` **SIEMPRE SE DEJA EL GUION DE LA IZQUIERDA** (corrigiendo en `splitter/` y luego re-concatenando).
   - Regla 3.3: Triangulación obligatoria con el idioma original japonés.
   - Regla 8: No asignar landscape a EPUBs.
3. **`# issues`**: Reportes de anomalías y contradicciones de reportes.
4. **`# bitácora`** (⚠️ **con tilde obligatoria en la *á***):
   - Canal oficial exclusivo para la publicación de entregas y archivos procesados (.txt).
   - Automatización: `discord_tools.py` utiliza obligatoriamente el Quick Switcher (`Ctrl+K`) con búsqueda canónica `# bitácora`. **Nunca** publicar entregas en `# general`.

---

### 2. Estado de Producción — LOTE 1 (`dazai-lote-1.md` - 30 obras)

* **Traducción**: **30 / 30 (100% completada en `splitter/`)**.
* **Concatenación (Paso 2)**: **30 / 30 (100% completada en `01translator/books-translated/japon/dazai-osamu/es/lote-1/`)**.
* **Bloque de Obras Entregadas en `# bitácora` (7 de 7 del turno actual completadas)**:
  - **#24 `the-criminal`**: Auditada (10/10 PASS), entregada y subida a `# bitácora`.
  - **#25 `decadent-protest`**: Auditada (10/10 PASS), entregada y subida a `# bitácora`.
  - **#26 `gender-equality`**: Auditada (10/10 PASS), entregada y subida a `# bitácora`.
  - **#27 `philosophy-of-the-multiheaded-snake`**: Auditada (10/10 PASS), entregada y subida a `# bitácora`.
  - **#28 `revolution`**: Auditada (10/10 PASS), entregada y subida a `# bitácora`.
  - **#29 `the-blueeyed-pilgrim`**: Corregida bajo Regla 3.2 en `part_01.txt`, re-mergeada, auditada (10/10 PASS), entregada y subida a `# bitácora`.
  - **#30 `bottomless-hell`**: Auditada (10/10 PASS), entregada y subida a `# bitácora`.

---

### 3. Obras 1 a 23 de Lote 1
* Las obras 1 a 23 ya se encuentran 100% traducidas y concatenadas en `01translator/books-translated/japon/dazai-osamu/es/lote-1/`.
* Si se requiere auditar el bloque 1 a 23 para generar bitácoras individuales, pueden pasarse por la suite de 10 pasos con `agent.bat audit`.
* Alternativamente, el lote 1 está listo a nivel consolidado para proceder con la maquetación (Paso 7 - `book-layout.prompt.md`) o avanzar al **Lote 2 (`dazai-lote-2.md`)**.

---

### 4. Seguridad de Repositorio
* **Cumplimiento estricto**: No se ha realizado ningún git commit ni branch en el repositorio de Arodi (`epub-generator`). Toda la memoria y herramientas del Agent Bridge residen en `windows-scripts` (`wintools`).

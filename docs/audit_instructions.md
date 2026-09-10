# INSTRUCCIONES PARA AUDITAR — epub-generator & Discord (#instrucciones-para-auditar)

Este documento registra el flujo operativo exacto aprendido por el **Agent Bridge** directamente desde los canales clave del servidor Discord **`epubs`**:
- **`#en-turno`**: Backlog oficial de lotes y prioridades de producción definidos por Arodi.
- **`#instrucciones-para-auditar`**: Directrices de trabajo, reglas de auditoría y calidad.
- **`#issues`**: Canal exclusivo de anomalías, falsos positivos y contradicciones de reportes.
- **`#bitácora`**: Entrega oficial y registro de obras que cumplen criterio de aceptación.

---

## 🎯 CANAL `#en-turno` — BACKLOG ACTIVO DE PRODUCCIÓN (Arodi)

Arodi asignó oficialmente los lotes prioritarios en `#en-turno`:
1. **`dazai-lote-1.md`**: 30 obras. (24 procesadas y entregadas; **6 pendientes**: #25 a #30).
2. **`dazai-lote-2.md`**: 30 obras (Top siguientes más famosas en estado [OK]).
3. **`dazai-lote-3.md`**: 30 obras (Novelas y relatos medianos, Tomo IV).
4. **`dazai-lote-4.md`**: 75 obras (Antología de relatos cortos, Tomo V).
5. **`dazai-lote-5.md`**: 75 obras (Antología de textos brevísimos y prefacios, Tomo VI).

---

## 📜 FLUJO OFICIAL DE TRABAJO EN DISCORD (#instrucciones-para-auditar)

```text
0.- Divide el siguiente libro <ruta_relativa> según las reglas de @agents/prompts/split-boock.prompt.md 
1.- Prepara el lote de traducción de splitter <ruta_relativa_de_el/los_libro/s> para los idiomas <idioma(s)>. 
1.1 Arranca el maratón de traducción infinito para <ruta_del_json_generado_en_el_punto_1> mediante @agents/workflows/translate-with-browser.txt, verifica que todo está en orden antes de comenzar.
2.- Concatena el siguiente libro <ruta_relativa_de_los_archivos_splitter> mediante @agents/prompts/concatenate-parts.prompt.md 
3.- Pásale la maquinaria de audición a <ruta_relativa_del_archivo_concatenado> @agents/prompts/audit-translation.prompt.md 
    3.1 No aceptes las sugerencias del checker para cuestiones semánticas ni en lote.
    3.2 En '06 dash_check' SIEMPRE se deja el guion de la izquierda.
    3.3 Pide triangulación e investigación a fondo de los errores reportados. Comparación de los parts traducidos con los part en el idioma original, etc. 
7.- Aplica el @agents/prompts/book-layout.prompt.md a: <ruta_relativa_del_archivo_concatenado> y valida coherencia en el TOC como un lector nativo.
#############
Cuando tengas todas las obras maquetadas y mergeadas en un solo .txt:
8.- Genera el epub de <ruta_relativa_del_archivo_concatenado_omnibus> @agents/prompts/generate-epub.prompt.md. NO le asignes un landscape (pues cuesta dinero).
```

---

## 🚨 REGLAS CRÍTICAS DE AUDITORÍA Y TRIANGULACIÓN

### 1. Regla 3.1: Prohibido aplicar cambios semánticos en lote
* **Nunca** aceptar sugerencias masivas o automatizadas de LanguageTool / checkers para cuestiones de estilo, elección de palabras o semántica literaria.
* Toda sugerencia semántica se analiza individualmente en contexto.

### 2. Regla 3.2: Resolución en `06 dash_check`
* Cuando el checker de guiones (`tools.dash_checker`) detecte secuencias dobles o múltiples (`--`, `– –`, `— -`, `––`, `—–`), la regla de resolución es estricta e invariable:
  👉 **SIEMPRE SE DEJA EL GUIÓN DE LA IZQUIERDA.**

### 3. Regla 3.3: Triangulación exhaustiva con el idioma original
* Si un reporte arroja un error o discrepancia, **no se asume el reporte a ciegas**.
* Es obligatorio realizar **triangulación**:
  * Abrir y comparar `splitter/.../{src_lang}/part_NN.txt` (fuente original, ej. japonés `ja`) con `splitter/.../{tgt_lang}/part_NN.txt` (traducción, ej. `es`).
  * Verificar si lo señalado es una omisión real, un calco, una adaptación válida o un falso positivo del verificador gramatical.
  * Si los reportes de las herramientas se contradicen (ej. Grammar Checker vs Sanity Checker vs Reglas Markdown) o hay un bloqueo, reportarlo de inmediato en el canal **`#issues`** usando `agent issue`.

### 4. Regla 8: Generación de EPUB / Maquetación
* En el paso final de maquetación con `generate-epub.prompt.md`:
  👉 **NUNCA asignar modo landscape** a los EPUBs (genera costes adicionales innecesarios).

### 5. Regla de Entrega y Criterio de Aceptación: Canal `# bitácora` (Arodi - 15:14)
* **Nombre exacto del canal**: **`# bitácora`** (con tilde obligatoria en la *á*).
* **Navegación segura**: `discord_tools` navega obligatoriamente usando el Quick Switcher (`Ctrl+K`) buscando `bitácora`. **Nunca** publicar entregas en `# general`.
* Cuando los archivos procesados cumplan satisfactoriamente el **criterio de aceptación** (auditoría completa, guiones corregidos bajo Regla 3.2, triangulación limpia y concatenación validada):
  * **NO crear una rama de Git** para que Arodi revise el merge.
  * **El registro formal de la entrega y el archivo procesado (.txt) se publican directamente en el canal `# bitácora`** del servidor Discord `epubs`.
  * El reporte en `#bitácora` debe detallar:
    - Obra, autor, idioma y lote.
    - Archivo final procesado (`01translator/books-translated/...`).
    - Estado de validación de la suite (pasos aprobados).
    - Métricas de aceptación: partes procesadas, líneas y caracteres.

---

## 🛡️ CONTROL HUMANO Y SEGURIDAD

* **Aprobación Obligatoria Paso a Paso**: Todo comando se detiene para pedir confirmación `[s/N]` al usuario.
* **Cero Commits No Autorizados**: No se ejecuta `git commit` hasta que Arodi examine el `git diff` y confirme con `ARODI`.
* **Fuente de Verdad**: Las correcciones NUNCA se aplican directamente sobre el archivo concatenado en `01translator/books-translated/`. Se corrigen en las partes de `splitter/` y luego se re-ejecuta la concatenación.
* **Entrega**: Toda entrega aceptada se reporta en `#bitácora`, no en ramas git separadas.

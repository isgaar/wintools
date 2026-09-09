# INSTRUCCIONES PARA AUDITAR — epub-generator & Discord (#instrucciones-para-auditar)

Este documento registra el flujo operativo exacto aprendido por el **Agent Bridge** directamente desde el canal **`#instrucciones-para-auditar`** del servidor Discord **`epubs`**.

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

---

## 🛡️ CONTROL HUMANO Y SEGURIDAD

* **Aprobación Obligatoria Paso a Paso**: Todo comando se detiene para pedir confirmación `[s/N]` al usuario.
* **Cero Commits No Autorizados**: No se ejecuta `git commit` hasta que Arodi examine el `git diff` y confirme con `ARODI`.
* **Fuente de Verdad**: Las correcciones NUNCA se aplican directamente sobre el archivo concatenado en `01translator/books-translated/`. Se corrigen en las partes de `splitter/` y luego se re-ejecuta la concatenación.

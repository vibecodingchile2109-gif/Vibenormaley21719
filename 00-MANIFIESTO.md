# Base de conocimiento "vibenorma" — manifiesto v3

Actualizado el 15-09-2026. Corpus depurado: solo normativa chilena de protección de datos y guías/doctrina de origen chileno o propio. Sin material de terceros (Data & Derechos) ni citas de jurisdicción extranjera.

## 1. Qué se sacó en esta pasada

- **Toda la capa `04-evidencia-y-metodologia/`** — carta Gantt, instrumento de levantamiento de tratamientos, matriz de brechas e bitácora. Todo eso era la metodología comercial de VibeCodingChile x **Data & Derechos**, un proyecto/cliente distinto de vibenorma. Se elimina completo, no quedan referencias.
- **`ficha-guia-aaip-clausulas-tidp.md`** — la Guía de implementación de cláusulas contractuales modelo era de la AAIP/DNPDP de **Argentina**. Se elimina para que ninguna cita de jurisdicción extranjera pueda colarse en una respuesta sobre obligaciones en Chile.

Verificado por grep: no queda ninguna mención a "Data & Derechos" ni a fuentes argentinas en el corpus. Las coincidencias de "datos"+"derechos" que aparecen ahora son solo texto legítimo de la ley (p. ej. "derechos del titular de datos").

## 2. Qué queda: tres capas, dos knowledge sources

| Capa | Carpeta | Contenido | Knowledge source |
|---|---|---|---|
| 1. Normativa primaria CL | `01-normativa-primaria/` | Ley 19.628 reformada por Ley 21.719 (79 arts.), Decreto 662/2025 (20 arts. + considerandos + firmas), disposiciones transitorias, plantilla oficial de política | `ks-normativa-cl` |
| 2. Guías chilenas | `02-guias-y-soft-law/` | 3 fichas: Derecho Informático (Academia Judicial), El nuevo sistema de protección de datos (Talca/Valparaíso), Guía de IA Generativa para Juezas y Jueces (Academia Judicial) | `ks-guias-cl` |
| 3. Doctrina propia | `03-doctrina-interna/` | Paper Gobernador IA + manual de gobernanza corporativa de IA | `ks-doctrina-interna` |

Las tres fichas que quedan en la capa 2 son de autoría chilena (Academia Judicial de Chile, académicas de la U. de Talca y U. de Valparaíso). Ya no hay riesgo de mezclar jurisdicciones.

El detalle artículo por artículo de la ley y el decreto sigue en `INDICE-NORMATIVO.md`.

## 3. Vectorización de la Ley 19.628 reformada y el Decreto 662

Estas dos normas son la columna vertebral y ya están fragmentadas para vectorizar directamente, un chunk por artículo:

- **Decreto 662/2025**: 22 archivos (`00-preambulo-considerandos.md`, 20 artículos, `99-firmas.md`).
- **Ley 19.628 reformada**: 79 archivos, uno por artículo (incluye los "bis", "ter", "quáter", etc. como archivos separados porque son unidades citables independientes).

Cada archivo trae en el front matter: `norma`, `articulo`, `epigrafe`, `titulo`, `parrafo` (cuando aplica), `introducido_por` (qué numeral del art. primero de la Ley 21.719 lo incorporó), `vigencia`, `fuente` y `cita_sugerida`. Para subir a Azure AI Search / Foundry:

1. Sube las dos carpetas (`decreto-662/` y `ley-19628-reformada/`) completas a Blob Storage, cada una en su propio contenedor o prefijo.
2. En la knowledge source, indexa el campo `articulo` y `epigrafe` como metadata filtrable — así el agente puede filtrar por artículo exacto además de recuperar por similitud semántica.
3. No fusiones los 79+20 archivos en uno solo: el chunking por artículo es lo que permite que las citas salgan exactas y que el "esfuerzo de razonamiento" pueda recuperar 3-5 artículos específicos en vez de un bloque gigante de la ley completa.

## 4. La trampa de citación (sigue vigente, corrígela en las instrucciones)

La Ley 21.719 casi no tiene articulado propio: su artículo primero **reforma la Ley 19.628**, y esa reforma es donde vive el 99% del contenido sustantivo (bases de licitud, derechos ARCOP, delegado, sanciones). Por eso el corpus fragmentado se llama `ley-19628-reformada/` y no `ley-21719/`: es la nomenclatura jurídicamente correcta.

`ley-21719/` solo contiene lo que es genuinamente propio de esa ley: los artículos segundo y tercero (modificaciones a otras leyes) y las disposiciones transitorias.

El paper interno (capa 3) cita "Art. 12 Ley 21.719", "Art. 14 bis Ley 21.719" — cítalos bien: son de la Ley 19.628 reformada. Las instrucciones de recuperación de abajo compensan esto en tiempo de consulta, pero conviene corregirlo en el paper mismo si lo vas a mostrar a clientes.

## 5. Vigencia

Ley 21.719 publicada 13-DIC-2024, vigencia diferida al **01-DIC-2026**, última modificación 05-FEB-2026 (Ley 21.806). Hoy, 15-SEP-2026, todavía no rige. Las instrucciones de respuesta obligan a fechar las obligaciones en vez de hablar en presente absoluto.

## 6. Configuración en Foundry

- **Esfuerzo de razonamiento: Medio** (5 fuentes, 5 subconsultas, búsqueda iterativa, 10.000 tokens). Con la ley fragmentada en 79 piezas, la iteración es necesaria para preguntas que cruzan varios artículos.
- **Modelo de finalización:** gpt-4.1 para producción; gpt-4.1-mini si el costo aprieta.
- **Modo de salida:** Síntesis de respuestas.
- **Identidad administrada** del servicio de búsqueda con rol Cognitive Services User sobre el recurso de Foundry.

### Instrucciones de recuperación

```
Motor de recuperación de un asistente de cumplimiento en protección de datos
personales de Chile y gobernanza de IA.

Fuentes disponibles:
- ks-normativa-cl: Ley 19.628 reformada por Ley 21.719 (arts. 1 a 55), Decreto
  662/2025 (arts. 1 a 20), disposiciones transitorias, plantilla oficial de
  política de tratamiento. Toda de jurisdicción chilena.
- ks-guias-cl: guías y material docente de la Academia Judicial de Chile y
  académicas chilenas sobre protección de datos e IA generativa.
- ks-doctrina-interna: arquitectura y metodología propia de VibeCodingChile
  (Gobernador IA, CheckWizard, NORMA).

Selección:
- Obligaciones, plazos, requisitos, sanciones, derechos del titular, delegado,
  certificación: SIEMPRE ks-normativa-cl primero.
- Buenas prácticas de uso de IA, estándares de conducta, HITL: agrega ks-guias-cl.
- "Cómo lo hacemos", arquitectura técnica, Gobernador IA: ks-doctrina-interna.
- Preguntas de implementación: consulta las tres, fragmentos normativos primero.

Planificación:
- Conserva literalmente ley, decreto, artículo, letra y numeral.
- Si la consulta dice "art. N de la Ley 21.719", busca TAMBIÉN "art. N de la Ley
  19.628": la 21.719 reforma la 19.628 y esa es la numeración vigente para el
  articulado sustantivo (arts. 1 a 55). Solo los arts. segundo, tercero y las
  disposiciones transitorias son propios de la Ley 21.719.
- Expande lenguaje coloquial: "DPO" -> delegado de protección de datos; "multas"
  -> arts. 34 bis, 34 ter, 34 quáter y 35; "RAT" -> registro de actividades de
  tratamiento (art. 3 d) Decreto 662); "EIPD" -> art. 15 ter; "brecha" -> art. 14
  sexies; "ARCOP" -> arts. 5 a 9.
```

### Responder las instrucciones

```
Responde en español de Chile, tono técnico-jurídico, directo, sin relleno.

Jerarquía de fuentes:
1. Ley 19.628 reformada y Decreto 662/2025: única base para afirmar qué exige la
   norma. Cita siempre con el campo cita_sugerida del fragmento.
2. Guías de la Academia Judicial y doctrina académica chilena: buenas prácticas
   e interpretación, nunca como fuente de una obligación.
3. Doctrina y metodología interna (Gobernador IA): preséntala como criterio
   propio de VibeCodingChile, nunca como norma.

Reglas estrictas:
- Nunca cites un artículo sustantivo "de la Ley 21.719" (arts. 1 a 55 son de la
  Ley 19.628 reformada). Solo los arts. segundo, tercero y transitorios son de
  la 21.719 propiamente.
- Toda fuente citada es chilena. Si detectas contenido de otra jurisdicción,
  adviértelo y no lo uses para fundamentar una obligación en Chile.
- Vigencia: la ley entra en vigor el 01-DIC-2026. No hables en presente
  absoluto de obligaciones que aún no rigen.
- Distingue "deberá" de "podrá": el modelo de prevención es voluntario (art. 1
  Decreto 662); el delegado es obligatorio dentro de él (art. 6).
- Si no hay respaldo en las fuentes: "No encuentro respaldo en las fuentes
  cargadas". Nunca completar con conocimiento general.

Formato:
1. Respuesta directa, 2-3 frases.
2. Fundamento normativo en viñetas, cada una con su cita.
3. "Implicancia práctica" cuando aplique.
4. Cierre de una línea: orientación informativa, no asesoría legal.
```

## 7. Pendientes

1. Ley 21.663 de Ciberseguridad — no cargada, y el manual de gobernanza la invoca.
2. EU AI Act (texto público) si vas a mantener el cruce comparado del paper — fragmentar igual que la ley chilena.
3. Set de evaluación (≈20 preguntas con artículo esperado) para medir si un cambio de instrucciones mejora o empeora las respuestas.

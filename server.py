"""
Servidor MCP — vibenorma
Expone el corpus normativo de Ley 19.628 (reformada por Ley 21.719) y Decreto 662
como herramientas de búsqueda y recuperación exacta, en vez de dejar que el modelo
"recuerde" la ley de memoria.

Ejecutar en local (stdio, para Claude Desktop / Claude Code):
    python server.py

Ejecutar como servidor remoto (streamable-http, para Foundry / conectores de claude.ai):
    MCP_TRANSPORT=streamable-http MCP_PORT=8787 python server.py

Ver README.md para instrucciones de conexión.
"""

import os
import re
import unicodedata
from pathlib import Path
from typing import Optional

import yaml
from mcp.server.fastmcp import FastMCP

KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"

mcp = FastMCP(
    "vibenorma",
    instructions=(
        "Servidor de conocimiento normativo chileno de protección de datos personales "
        "(Ley 19.628 reformada por la Ley 21.719, y su Decreto 662). "
        "Antes de responder cualquier pregunta legal, llama primero a buscar_normativa "
        "o lee obtener_manifiesto para conocer las reglas de citación del corpus. "
        "Nunca cites un artículo sin haberlo recuperado con estas herramientas."
    ),
)


# ---------- Carga del corpus ----------

def _parse_frontmatter(text: str):
    """Separa el YAML front matter (entre --- ---) del cuerpo del documento.
    Si el YAML estricto falla (valores con ':' sin comillas, frecuentes en
    el campo 'fuente' de este corpus), cae a un parser línea por línea de
    'clave: resto de la línea', suficiente para este formato."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not m:
        return {}, text
    raw_meta, body = m.group(1), m.group(2).strip()
    try:
        meta = yaml.safe_load(raw_meta) or {}
        if not isinstance(meta, dict):
            raise yaml.YAMLError("frontmatter no es un mapeo")
    except yaml.YAMLError:
        meta = {}
        for line in raw_meta.split("\n"):
            if ":" not in line:
                continue
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return meta, body


def _confiabilidad(meta: dict) -> str:
    """Clasifica cada documento según cuánto peso normativo tiene, a partir del
    propio front matter que ya trae el corpus (ver 00-MANIFIESTO.md)."""
    jerarquia = (meta.get("jerarquia") or "").lower()
    tipo = (meta.get("tipo") or "").lower()
    tipo_registro = (meta.get("tipo_registro") or "").lower()
    if jerarquia in ("ley", "reglamento"):
        return "normativa_oficial"
    if "documento interno" in tipo:
        return "documento_interno_no_citable"
    if "ficha de fuente" in tipo_registro:
        return "doctrina_de_terceros_no_reproducida"
    return "sin_clasificar"


def _load_corpus():
    docs = []
    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta, body = _parse_frontmatter(text)
        docs.append({
            "archivo": path.name,
            "meta": meta,
            "body": body,
            "confiabilidad": _confiabilidad(meta),
        })
    return docs


_CORPUS = _load_corpus()


def _normalize(s: str) -> str:
    s = s.lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s


def _tokenize(s: str):
    return re.findall(r"[a-z0-9]+", _normalize(s))


# ---------- Herramientas ----------

_CONFIABILIDAD_PESO = {
    "normativa_oficial": 1.6,
    "doctrina_de_terceros_no_reproducida": 1.0,
    "documento_interno_no_citable": 0.55,
    "sin_clasificar": 1.0,
}

# Expansión mínima de sinónimos/abreviaturas frecuentes en consultas coloquiales,
# para que "pyme" o "arcop" encuentren el texto legal aunque la ley use otras
# palabras ("micro, pequeñas y medianas empresas"; los derechos uno por uno).
_SINONIMOS = {
    "pyme": ["micro", "pequenas", "medianas", "empresas"],
    "pymes": ["micro", "pequenas", "medianas", "empresas"],
    "arcop": ["acceso", "rectificacion", "cancelacion", "oposicion", "portabilidad", "bloqueo"],
    "multa": ["sancion", "sanciones", "infraccion", "infracciones"],
    "multas": ["sancion", "sanciones", "infraccion", "infracciones"],
}


def _expand(tokens):
    expandido = set(tokens)
    for t in tokens:
        expandido.update(_SINONIMOS.get(t, []))
    return expandido


@mcp.tool()
def buscar_normativa(consulta: str, jerarquia: Optional[str] = None, top_k: int = 5) -> str:
    """Busca en el corpus (Ley 19.628 reformada, Decreto 662, disposiciones
    transitorias, guías chilenas y doctrina interna) los documentos más relevantes
    para una consulta en lenguaje natural. Úsala SIEMPRE antes de afirmar qué dice
    la ley — no respondas de memoria.

    Args:
        consulta: pregunta o tema a buscar, en español, lenguaje natural.
        jerarquia: filtro opcional exacto o parcial (ej. "ley", "reglamento").
        top_k: cuántos resultados devolver como máximo (por defecto 5).
    """
    tokens = _expand(_tokenize(consulta))
    if not tokens:
        return "Consulta vacía."

    resultados = []
    for doc in _CORPUS:
        if jerarquia and jerarquia.lower() not in (doc["meta"].get("jerarquia") or "").lower():
            continue
        meta_tokens = _tokenize(" ".join(str(v) for v in doc["meta"].values()))
        body_tokens = _tokenize(doc["body"])
        if not body_tokens:
            continue
        meta_hits = sum(meta_tokens.count(t) for t in tokens)
        body_hits = sum(body_tokens.count(t) for t in tokens)
        # frecuencia relativa en el cuerpo, para que un artículo corto y preciso
        # no quede enterrado bajo un documento largo que solo menciona el tema de paso
        body_tf = body_hits / len(body_tokens)
        score = (meta_hits * 8) + (body_tf * 400) + (1 if body_hits else 0)
        score *= _CONFIABILIDAD_PESO.get(doc["confiabilidad"], 1.0)
        if score > 0:
            resultados.append((score, doc))

    resultados.sort(key=lambda x: x[0], reverse=True)
    resultados = resultados[:max(1, top_k)]

    if not resultados:
        return (
            f"Sin resultados para \"{consulta}\". No inventes una respuesta: dile al "
            "usuario que no encontraste el fundamento exacto en el corpus."
        )

    salida = [f"{len(resultados)} resultado(s) para \"{consulta}\":\n"]
    for score, doc in resultados:
        meta = doc["meta"]
        fragmento = doc["body"][:400].replace("\n", " ").strip()
        bloque = [
            f"### {meta.get('cita_sugerida', doc['archivo'])}",
            f"- archivo: {doc['archivo']}",
            f"- jerarquía: {meta.get('jerarquia', meta.get('tipo', '—'))}",
            f"- epígrafe/sección: {meta.get('epigrafe', meta.get('seccion', '—'))}",
            f"- vigencia: {meta.get('vigencia', '—')}",
            f"- confiabilidad: {doc['confiabilidad']}",
        ]
        if meta.get("advertencia"):
            bloque.append(f"- ADVERTENCIA: {meta['advertencia']}")
        if meta.get("regla_de_uso"):
            bloque.append(f"- regla de uso: {meta['regla_de_uso']}")
        bloque.append(f"- fragmento: {fragmento}…")
        salida.append("\n".join(bloque))

    salida.append(
        "\nPara el texto completo de cualquiera de estos resultados, llama a "
        "obtener_documento(archivo)."
    )
    return "\n\n".join(salida)


@mcp.tool()
def obtener_documento(archivo: str) -> str:
    """Devuelve el texto completo y los metadatos de un documento exacto del
    corpus, por su nombre de archivo (tal como lo entrega buscar_normativa o
    listar_indice).

    Args:
        archivo: nombre de archivo, ej. "art-08-designacion-del-delegado.md".
    """
    for doc in _CORPUS:
        if doc["archivo"] == archivo:
            meta = doc["meta"]
            cabecera = "\n".join(f"{k}: {v}" for k, v in meta.items())
            return f"---\n{cabecera}\n---\n\n{doc['body']}"
    disponibles = ", ".join(d["archivo"] for d in _CORPUS if archivo.split(".")[0] in d["archivo"])
    return (
        f"No existe el archivo \"{archivo}\" en el corpus."
        + (f" ¿Quisiste decir alguno de estos?: {disponibles}" if disponibles else "")
    )


@mcp.tool()
def listar_indice(jerarquia: Optional[str] = None, contiene: Optional[str] = None) -> str:
    """Lista el índice del corpus (archivo, artículo/sección, epígrafe, jerarquía)
    para explorar sin conocer el nombre exacto del archivo.

    Args:
        jerarquia: filtro opcional, ej. "ley", "reglamento", "documento interno".
        contiene: filtro opcional de texto libre sobre el epígrafe/sección.
    """
    filas = []
    for doc in _CORPUS:
        meta = doc["meta"]
        j = (meta.get("jerarquia") or meta.get("tipo") or "")
        if jerarquia and jerarquia.lower() not in j.lower():
            continue
        etiqueta = meta.get("epigrafe") or meta.get("seccion") or meta.get("obra") or ""
        if contiene and _normalize(contiene) not in _normalize(etiqueta):
            continue
        ref = meta.get("articulo") or meta.get("seccion") or "—"
        filas.append(f"- [{doc['archivo']}] {ref} — {etiqueta} ({j or 'sin jerarquía'})")

    if not filas:
        return "Sin coincidencias para ese filtro."
    return f"{len(filas)} documento(s):\n" + "\n".join(filas)


@mcp.tool()
def obtener_manifiesto() -> str:
    """Devuelve el manifiesto del corpus: qué contiene, cómo está organizado,
    y muy importante, la 'trampa de citación' (por qué casi todo el contenido
    sustantivo vive en la Ley 19.628 reformada y no en artículos propios de la
    Ley 21.719). Léelo antes de responder preguntas normativas complejas."""
    for doc in _CORPUS:
        if doc["archivo"] == "00-MANIFIESTO.md":
            return doc["body"]
    return "Manifiesto no encontrado en el corpus."


# ---------- Recurso (acceso directo por URI, alternativa a obtener_documento) ----------

@mcp.resource("vibenorma://{archivo}")
def recurso_documento(archivo: str) -> str:
    """Expone cada documento del corpus como recurso direccionable por URI."""
    for doc in _CORPUS:
        if doc["archivo"] == archivo:
            return doc["body"]
    return f"No existe el archivo {archivo} en el corpus."


if __name__ == "__main__":
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    if transport == "stdio":
        mcp.run()
    else:
        host = os.environ.get("MCP_HOST", "0.0.0.0")
        port = int(os.environ.get("MCP_PORT", "8787"))
        mcp.run(transport=transport, host=host, port=port)

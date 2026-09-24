# MCP vibenorma

Servidor MCP que expone tu corpus normativo (Ley 19.628 reformada por la Ley
21.719, Decreto 662, disposiciones transitorias, guías chilenas y doctrina
interna — 111 documentos) como herramientas de búsqueda y recuperación exacta.
Esto es la pieza que hace real "no solo entendemos la ley, la vectorizamos":
cualquier cliente MCP (Claude, un agente de Foundry, Copilot) consulta este
servidor artículo por artículo en vez de citar de memoria.

## Qué trae

| Archivo | Para qué |
|---|---|
| `server.py` | El servidor. 4 herramientas + 1 recurso, sin dependencias pesadas. |
| `knowledge/` | Los 111 documentos de tu corpus, tal como los subiste (con un ajuste: ver abajo). |
| `requirements.txt` | `mcp` + `pyyaml`. |
| `claude_desktop_config.ejemplo.json` | Plantilla para conectarlo a Claude Desktop. |

**Un archivo lo corregí**: en tu zip, el Artículo 1 del **Decreto 662** y el
Artículo 1 de la **Ley 19.628** compartían el mismo nombre de archivo
(`art-01-objeto-y-ambito-de-aplicacion.md`) — uno estaba en la carpeta plana y
el otro anidado en una ruta de export (`mnt/user-data/outputs/kb-vibenorma/...`).
Sin darme cuenta lo habría perdido al aplanar la carpeta, así que lo separé
como `decreto-art-01-objeto-y-ambito-de-aplicacion.md`. Si vuelves a exportar
este corpus desde tu pipeline original, conviene que la carpeta del decreto y
la de la ley nunca compartan nombres de archivo.

## Las 4 herramientas

- **`buscar_normativa(consulta, jerarquia=None, top_k=5)`** — búsqueda por
  palabras clave con expansión mínima de sinónimos (ej. "pyme" también
  encuentra "micro, pequeñas y medianas empresas"; "ARCOP" encuentra cada
  derecho por separado). Pondera fuerte los metadatos (epígrafe, artículo) y
  penaliza los documentos marcados como `documento_interno_no_citable` frente
  a la normativa oficial, para que un paper propio no le gane en relevancia a
  un artículo real de la ley.
- **`obtener_documento(archivo)`** — texto completo y metadatos exactos de un
  archivo, para citar sin parafrasear.
- **`listar_indice(jerarquia=None, contiene=None)`** — para explorar el
  corpus sin conocer el nombre del archivo.
- **`obtener_manifiesto()`** — devuelve tu `00-MANIFIESTO.md` completo,
  incluida la "trampa de citación" que ya documentaste (que casi todo el
  contenido sustantivo vive en la Ley 19.628 reformada, no en artículos
  propios de la Ley 21.719).

Nota sobre el motor de búsqueda: es búsqueda por palabras clave con algo de
sinonimia a mano, no embeddings — no tiene la profundidad semántica de un
vector store real. Para eso sigue en pie lo de `FOUNDRY-SETUP.md`: sube estos
mismos 111 archivos a un vector store de Foundry cuando quieras esa capa. Este
servidor funciona bien igual como fuente confiable y con citas exactas mientras
tanto, y como respaldo barato aunque tengas el vector store.

## Cómo correrlo

```bash
cd mcp-vibenorma
pip install -r requirements.txt
python server.py
```

Por defecto usa transporte `stdio` (para clientes locales). Para exponerlo
como servidor remoto:

```bash
MCP_TRANSPORT=streamable-http MCP_PORT=8787 python server.py
```

## Conectarlo — 3 rutas

### 1. Claude Desktop / Claude Code (local, sin hosting, funciona hoy)
Copia `claude_desktop_config.ejemplo.json` a la ubicación real de config de
Claude Desktop (o agrega su bloque `vibenorma` a tu config existente),
reemplazando la ruta por la absoluta a `server.py` en tu máquina. Reinicia
Claude Desktop. Para Claude Code: `claude mcp add vibenorma -- python
/RUTA/A/server.py`.

### 2. Conectores remotos de claude.ai (necesita hosting)
Los conectores personalizados de la versión web de Claude requieren una URL
pública. Despliega este servidor con `MCP_TRANSPORT=streamable-http` en
cualquier hosting que corra Python (Azure App Service, un contenedor, Fly.io,
Render), y agrégalo en Configuración → Conectores con esa URL.

### 3. Agente de Foundry (necesita hosting)
Azure AI Foundry Agent Service soporta herramientas MCP de forma nativa. Una
vez desplegado el servidor con transporte HTTP, en el código del agente
(Agent Framework):

```python
from agent_framework.foundry import FoundryChatClient
from azure.identity.aio import AzureCliCredential

async with AzureCliCredential() as credential:
    client = FoundryChatClient(credential=credential)
    vibenorma_tool = client.get_mcp_tool(
        name="vibenorma",
        url="https://TU-SERVIDOR-DESPLEGADO/mcp",
    )
    # agrégalo a las tools del agente junto con las de plugin.json
```

Si tu instancia de Foundry ya tiene la opción "Herramientas → agregar servidor
MCP" en el constructor sin código (como el panel que se ve en tus capturas),
pruébala primero ahí directamente con la misma URL — es más simple que el
camino por código si está disponible en tu versión.

## Seguridad

Este servidor no tiene autenticación — piénsalo como de solo lectura sobre
contenido que ya es público (la ley) más tus propios documentos internos. Si
lo despliegas remoto y no quieres que cualquiera con la URL lo consulte,
agrega un bearer token simple delante (un proxy o middleware ASGI) antes de
compartir la URL fuera de tu equipo.

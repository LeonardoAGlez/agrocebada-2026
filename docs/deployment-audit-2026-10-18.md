# Auditoría de despliegue — 18 de octubre de 2026

El dashboard funciona en el entorno local preparado, pero no está listo para publicarse sin ajustes. La primera candidata gratuita es Streamlit Community Cloud, condicionada a resolver portabilidad, instalación y consumo de memoria, y a probar la URL final. Render gratuito tiene poco margen para la memoria observada. Vercel y Cloudflare requieren evaluar adaptaciones adicionales.

## Resultados comprobados

- Windows y Python 3.12.14, con dependencias existentes. No se reinstalaron dependencias desde cero.
- Ambos modelos cargan y exportan las 59 predicciones. La integración reproduce las predicciones guardadas y métricas desde 138 predicciones OOF. Evidencia: artifacts/integration-check.json.
- Suite existente: 22 pruebas aprobadas; 3 errores de preparación por permisos de directorios temporales. Reintentar dentro del proyecto encontró la misma restricción. No se declara la suite completa aprobada.
- AppTest adicional: 13 comprobaciones sin errores ni excepciones de aplicación; incluye tres vistas, cálculo y explicación con ambos modelos. Evidencia: tmp/deployment-ui-audit.json.
- Memoria RSS: inferencia aislada con ambos modelos, aproximadamente 201 MiB. La prueba de interfaz pasó de 634 MiB inicialmente a un pico de 1406 MiB tras interacciones repetidas. Incluye el entorno de pruebas: no es una medición de producción Linux ni demuestra por sí sola una fuga. Requiere medición del servidor y concurrencia.
- Código, configuración, datos procesados y artefactos para consulta suman aproximadamente 9.67 MiB, excluyendo dependencias Python. Los datos procesados ocupan 8.48 MiB. Los originales e históricos no son necesarios para consultar.
- No se hizo construcción Linux: Docker está instalado pero su servicio no está disponible. No se probaron URL pública, HTTPS ni concurrencia real.

## Bloqueos

1. Rutas de Windows: data/processed/feature-configs.json contiene nueve rutas con barras invertidas. modeling.py:231 las concatena directamente con ROOT; fallarán en Linux. Normalizar las rutas y comprobar reproducción.
2. Entorno exacto: inference.py:14 exige coincidencia de versiones, incluida Python 3.12.14. Seleccionar Python 3.12 o instalar las dependencias amplias de pyproject.toml no garantiza que cargue. Verificar el entorno del proveedor sin desactivar controles de integridad ni reentrenar al iniciar.
3. Instalación: app.py importa agrocebada desde src/. El proyecto usa instalación editable; common.py:8 calcula la raíz desde la ubicación del módulo. Una instalación convencional puede desplazar la raíz de recursos. Preservar una instalación editable con pip install --no-deps -e . o resolver explícitamente el acceso a recursos. requirements.lock no es un archivo autodetectado por Community Cloud: preparar requirements.txt que instale las versiones fijadas y el paquete local, o una construcción explícita equivalente.
4. Servidor: .streamlit/config.toml:5 fija 127.0.0.1 y puerto 8501. Para Render se necesita 0.0.0.0 y el puerto del proveedor. Puede sobreescribirse en el arranque.
5. ZIP anterior: dist/agrocebada-local-2025-10-31.zip contiene un modelo distinto. Hash del ZIP: ea6f83ae81603486a7a7b278834f9f64e6731584285b0a05facfb0e95082fae0. Hash actual: 8ee63e3b1d07ec5e9be0fd98dcc9bb0bc7091c934a34a9eb5bbd642847f80313. Preparar el despliegue desde los archivos actuales.
6. Memoria y repositorio: comprobar memoria del servidor y varias sesiones. La carpeta actual no contiene repositorio Git; Community Cloud requiere acceso mediante GitHub. Publicar un paquete pequeño con todos los recursos actuales necesarios, excluyendo entorno virtual, dependencias Node, experimentos e históricos.

Cambiar módulos en src/agrocebada cambia code_hash(). Cualquier corrección allí exige reconciliar la integridad mediante un procedimiento trazable y verificar que no cambia la inferencia; editar el código y publicar el contrato anterior puede bloquear la carga.

## Plataformas

| Plataforma | Dictamen para esta versión |
| --- | --- |
| Streamlit Community Cloud | Primera candidata gratuita por compatibilidad de framework; requiere GitHub, instalación reproducible, validación de Python y memoria. Consultar recursos efectivos en la cuenta. Hiberna tras 12 horas sin tráfico. |
| Render gratuito | Servidor Python compatible, pero 512 MB RAM. No recomendado sin optimizar y medir. Duerme tras 15 minutos sin tráfico; las escrituras locales se pierden al reiniciar. |
| Vercel | Sin configuración ni adaptación del servidor Streamlit. La beta de WebSockets de junio de 2026 documenta Node.js; no certifica compatibilidad directa con esta app Python. No recomendado para la entrega de hoy. |
| Cloudflare | Workers Python usa Pyodide/WebAssembly; requiere evaluar bibliotecas geoespaciales y adaptar el servidor. No recomendado para alojar esta versión hoy. |

La recomendación es una inferencia de compatibilidad y de mediciones locales; no garantiza capacidad del proveedor.

## Orden para cerrar

1. Crear copia mínima actual y corregir rutas portables.
2. Resolver instalación y Python sin debilitar la integridad del modelo.
3. Comprobar arranque y reproducción de ambos modelos en destino.
4. Medir memoria del servidor y varias sesiones; optimizar las cargas/copias si es necesario.
5. Publicar y comprobar desde una sesión nueva las tres vistas, predicción, explicación y descargas; probar acceso de evaluadores y arranque tras hibernar.

No se modificó el código de aplicación ni modelos o contratos. Las pruebas existentes de inferencia actualizaron comprobaciones y exportación oficial independiente. No se publicó ni entrenó.

## Fuentes oficiales

- [Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud)
- [Dependencias](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies)
- [Recursos de la cuenta](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-account/workspace-settings)
- [Hibernación](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app)
- [Planes Render](https://render.com/docs/compute-plans)
- [Render gratuito](https://render.com/docs/free)
- [Beta WebSockets Vercel](https://vercel.com/changelog/websocket-support-is-now-in-public-beta)
- [Python Workers Cloudflare](https://developers.cloudflare.com/workers/languages/python/how-python-workers-work/)

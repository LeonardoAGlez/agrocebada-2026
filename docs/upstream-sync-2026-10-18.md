# Sincronización de la versión del colega para Community Cloud

Fecha: 18 de octubre de 2026.
Origen: https://github.com/Elypsoon/Reto-Cebada, rama cambios-experimentos-2026-10-17, commit 89b2f67 (SHA completo registrado en artifacts/upstream-cloud-compatibility.json).
Destino: https://github.com/LeonardoAGlez/agrocebada-2026, rama main.

## Incorporado

- Artefacto activo R08 (AdaptiveEADBundle), sus 59 estimaciones oficiales, intervalos adaptativos por estado, OOF y métricas reportadas por el origen.
- Modelo oficial independiente y la nueva lógica de intervalos no negativos.
- Código, documentación, registros, resultados y pruebas de estratificacion-pyr-20261018 y fisiologia-siniestros-20261018. Las investigaciones adicionales permanecen como evidencia; no se promueve automáticamente otro modelo.
- Documentación y utilidades nuevas del checkout original. Los originales voluminosos y copias históricas permanecen en el proyecto local y en el origen.

## Adaptación para Streamlit

Se conservan requirements.txt, instalación editable, Python 3.12, pines exactos de bibliotecas, rutas POSIX, escucha en 0.0.0.0, diagnóstico de versiones y lectura satelital selectiva. El requisito de Python 3.12 debe seleccionarse en Advanced settings de Streamlit; cambiar el archivo de dependencias no cambia el intérprete de un despliegue existente.

Los contratos externos y metadatos embebidos se reconcilian con los cambios limitados de compatibilidad. El origen tenía un hash embebido anterior en uno de los modelos; se registra su valor antes de reconciliarlo. No se reentrena ningún estimador. Las predicciones y todos los intervalos de las 197 parcelas se comparan exactamente con una referencia obtenida del checkout de origen antes de la adaptación; ambas rutas coinciden exactamente. Las 59 estimaciones e intervalos también coinciden con los CSV guardados del origen dentro de 1e-10.

La consulta R08 informa que usa resultados precalculados y no muestra la sensibilidad del modelo base como si explicara el ensamble completo. Se distingue la validación estratificada de R08 de referencias evaluadas espacialmente; los números se conservan como fueron recibidos.

## Verificación

La comprobación automática Cloud readiness instala desde cero en Ubuntu/Python 3.12 y ejecuta el diagnóstico de artefactos, pruebas del dashboard y pruebas de las dos nuevas investigaciones. Consultar el resultado asociado al último commit de main antes de entregar la URL.

El respaldo local de los modelos de origen y sus 197 predicciones está en artifacts/versions/upstream-sync-89b2f67 (excluido de Git). El historial anterior del repositorio de despliegue conserva la versión previa. El rediseño visual queda pendiente.

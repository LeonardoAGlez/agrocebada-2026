# AgroCebada 2026

Dashboard Streamlit de consulta retrospectiva del rendimiento de 197 parcelas de cebada de Hidalgo, Tlaxcala y Puebla, campaña 2025. Incluye modelos guardados, 138 predicciones de validación fuera de pliegue y descarga de las 59 predicciones oficiales.

## Desplegar en Streamlit Community Cloud

- Repositorio: `LeonardoAGlez/agrocebada-2026`
- Rama: `main`
- Archivo principal: `app.py`
- Advanced settings → Python: **3.12**
- Dependencias: `requirements.txt` instala las versiones de `requirements.lock` y el paquete local editable.
- No requiere claves API ni reentrenamiento para consultar.

La configuración permite escuchar en la interfaz del servidor. El proveedor gestiona HTTPS y la URL. Si el código fuente es privado, conceder a Streamlit acceso a este repositorio. Configurar el acceso de la aplicación para que los evaluadores puedan abrirla.

La versión actual incorpora el **Ensamble Adaptativo R08** de la rama `cambios-experimentos-2026-10-17` del proyecto original. R08 consulta estimaciones precalculadas para las parcelas oficiales e intervalos adaptativos por estado. La ruta «Solo datos del reto» conserva su modelo independiente.

La comprobación **Cloud readiness** de GitHub Actions instala desde cero en Ubuntu/Python 3.12 y verifica modelos y pruebas. Consultar su resultado antes de entregar la URL.

## Ejecutar localmente

Con Python 3.12 y un entorno virtual activo:

```sh
python -m pip install -r requirements.txt
python -m agrocebada.cli verify
python -m streamlit run app.py
```

Para ejecutar las pruebas:

```sh
python -m pytest -q
```

## Integridad y portabilidad

Las rutas de las tablas son relativas con separadores POSIX. Las versiones de las bibliotecas del modelo se verifican exactamente; se permiten actualizaciones de parche de Python dentro de la misma versión menor 3.12. Los hashes de código, datos y modelo siguen siendo obligatorios. La actualización desde el commit `89b2f67` conserva exactamente predicciones e intervalos de las 197 parcelas de la versión de origen en ambos modelos, sin volver a entrenar; registro en `artifacts/upstream-cloud-compatibility.json`. La migración anterior permanece documentada en `artifacts/cloud-compatibility.json`.

Las investigaciones `estratificacion-pyr-20261018` y `fisiologia-siniestros-20261018` se incluyen en `experiments/`, con código, pruebas, registros y resultados. Las investigaciones posteriores no sustituyen automáticamente al artefacto R08 activo. R08 se reporta bajo validación estratificada; algunas referencias proceden de esquemas espaciales distintos. La interfaz indica esa diferencia y no atribuye al ensamble la explicación de su modelo base.

El dashboard lee únicamente las columnas y observaciones de la parcela y sensor consultados para reducir las copias de datos en memoria. La memoria real y la concurrencia deben comprobarse en el servicio alojado.

## Archivos y procedencia

Este repositorio contiene el código, las pruebas, datos procesados, fuentes externas verificadas, artefactos actuales y documentación. Los originales voluminosos, entornos locales, experimentos y versiones históricas se conservan en el proyecto local y se excluyen del repositorio de despliegue.

Origen del proyecto y los datos del reto: [Elypsoon/Reto-Cebada](https://github.com/Elypsoon/Reto-Cebada). Para regenerar datos desde los originales, consultar `docs/local-reproduction.md` y restaurar el conjunto original en `Reto-Cebada/DataSet`. La inferencia del dashboard no necesita esos originales. No utilizar ZIP anteriores de `dist` como versión actual.

Integrantes: Leonardo Alvarez Gonzalez, Ángel de Jesús Elvis Gutiérrez Pacheco y Diego Cannata Cárdenas. Documentación y aportaciones en `docs/`; informe, bibliografía y anexos en `output/pdf/`.

Los resultados son retrospectivos de 2025. No validan campañas futuras, predicción anterior a cosecha ni decisiones crediticias. Las etiquetas del test oculto no se conocen.

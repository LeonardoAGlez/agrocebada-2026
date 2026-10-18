# Preparación para Streamlit Community Cloud

Corrección del 18 de octubre de 2026.

## Cambios

- Rutas POSIX relativas en la configuración y en futuras preparaciones de datos.
- requirements.txt instala requirements.lock y el paquete editable; Python 3.12.
- Se permiten parches de Python 3.12; bibliotecas y hashes siguen verificándose exactamente.
- Servidor accesible en 0.0.0.0; Git conserva los bytes de datos y normaliza código a LF.
- Lectura satelital limitada a parcela, sensor y columnas consultadas, sin cambiar valores.
- Repositorio privado de despliegue: https://github.com/LeonardoAGlez/agrocebada-2026

## Verificación local

- 28 pruebas aprobadas, 4 avisos de deprecación de la multiplicación de transformaciones ráster.
- Predicciones e intervalos de las 197 parcelas exactamente iguales antes y después, en ambos modelos; sin reentrenamiento.
- 13 pasos de consulta, cálculo, explicación y navegación sin errores de aplicación.
- Pico RSS de la misma prueba AppTest en Windows: 1405.7 MiB antes, 286.1 MiB después. No es garantía de capacidad concurrente ni medición del servidor de producción.
- Integridad y migración: artifacts/cloud-compatibility.json. Prueba de interfaz: artifacts/cloud-ui-check.json.

El respaldo local completo anterior está en artifacts/versions/cloud-portability-2026-10-18; está excluido del repositorio de despliegue. La serialización del modelo cambió únicamente para reconciliar metadatos de versión de código, con igualdad exacta de predicciones comprobada.

## Desplegar

En https://share.streamlit.io crear aplicación desde el repositorio LeonardoAGlez/agrocebada-2026, rama main, archivo app.py. En Advanced settings seleccionar Python 3.12. Autorizar acceso al repositorio privado y configurar el acceso de los evaluadores a la aplicación. No requiere secretos API.

El flujo Cloud readiness de GitHub Actions instala y verifica en Ubuntu desde cero. Revisar su resultado antes de publicar la URL. La configuración del despliegue público y la comprobación de la URL siguen siendo pasos posteriores a preparar y subir el repositorio.

Los originales voluminosos del reto y versiones anteriores permanecen en la computadora; el repositorio conserva la procedencia y las fuentes procesadas necesarias. El ZIP anterior de dist no representa esta versión.

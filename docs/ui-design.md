# Diseño Campo editorial — AgroCebada

Dirección visual: interfaz clara inspirada en el segundo referente aportado por el usuario, combinada con un explorador geográfico oscuro inspirado en el primero. Paleta marfil, verde profundo, salvia y cebada; tipografía editorial en la cabecera, navegación lateral y tarjetas de indicadores.

## Implementación

- Tema nativo de Streamlit y CSS acotado a clases propias y contenedores con claves estables. Sin fuentes, mapas base o bibliotecas de animación externas.
- Logotipo original y trama topográfica decorativa en SVG autocontenido; los polígonos y puntos del mapa son datos oficiales, sin geografía sintética añadida.
- Entradas suaves y estados de interacción; revelado por desplazamiento mediante animation-timeline:view() cuando el navegador lo soporta. Con prefers-reduced-motion se desactivan animaciones y transiciones.
- Vista móvil con indicadores en dos columnas y paneles apilados. Comprobación visual a 390 px sin desbordamiento horizontal.
- Mapa oscuro, control para centrar en la parcela, estimación R08 destacada, intervalos y descargas nativas. En Validación, gráfico observado/estimado con predicciones fuera de pliegue.
- La presentación vive en dashboard_ui.py y ui_assets/dashboard.css. No se modificaron módulos científicos, modelos o contratos. Se conserva la lectura satelital selectiva para limitar memoria.

## Verificación

Antes del rediseño se confirmó en la aplicación publicada el modelo Ensamble Adaptativo R08 y la versión 01fe16367c. La suite del proyecto y las dos nuevas investigaciones incluye una prueba adicional de navegación entre las tres vistas y consulta en ambos modelos. La comprobación Cloud readiness valida main en Linux.

La propuesta utiliza el alojamiento gratuito actual de Streamlit Community Cloud. El movimiento es decorativo y progresivo: la información y los controles siguen disponibles cuando no hay soporte para animaciones de scroll.

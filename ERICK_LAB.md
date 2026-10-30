# SignalBoard · Erick Quio

**Dashboard oscuro de métricas operativas construido con Plotly Dash.**
Fork de [plotly/dash](https://github.com/plotly/dash), conservando su licencia MIT.
La demo es una adaptación local, no una contribución aceptada por upstream.

## Experiencia

- Tres servicios de ejemplo: API, Workers y Agents.
- Dos métricas: latencia media y solicitudes.
- Selección reactiva, gráfico interactivo y cambio respecto al primer día.
- Diseño oscuro adaptable, con acentos cian y violeta.

Los valores son **sintéticos y estáticos**. No representan servicios reales ni
monitorización en vivo. Cada serie tiene siete días.

## Ejecutar

Desde la raíz del fork, con Python 3.12 y `uv`:

```bash
uv run --no-project --with-requirements erick_requirements.txt python erick_signalboard.py
```

Abre `http://127.0.0.1:8050`. No requiere claves ni servicios externos.

## Verificación

```bash
uv run --no-project --with-requirements erick_requirements.txt python -m pytest test_erick_signalboard.py -q
```

Verificado con Dash 4.5.0 y Plotly 7.1.0: las seis combinaciones de servicio/métrica,
el documento y layout HTTP, y un callback real mediante el cliente de pruebas Flask.
No se ejecutó la suite completa del framework ni una prueba visual con Selenium.

## Personalizar

Modifica `SERIES` y `METRICS` en `erick_signalboard.py`. Los datos y la función
`build_figure` están separados del layout para facilitar la adaptación.
Una siguiente mejora sería conectar un origen de telemetría y añadir rangos de fechas.

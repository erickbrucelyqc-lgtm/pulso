"""SignalBoard: synthetic service metrics, with no external telemetry."""

import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html

SERIES = {
    "API": {
        "latency": [140, 135, 152, 128, 119, 123, 112],
        "requests": [820, 910, 870, 1030, 1100, 1210, 1300],
    },
    "Workers": {
        "latency": [320, 310, 290, 305, 275, 268, 250],
        "requests": [120, 155, 180, 190, 230, 250, 310],
    },
    "Agents": {
        "latency": [950, 880, 920, 850, 790, 810, 760],
        "requests": [40, 51, 48, 62, 74, 88, 105],
    },
}
METRICS = {"latency": "Latencia media (ms)", "requests": "Solicitudes"}


def build_figure(service, metric):
    if service not in SERIES or metric not in METRICS:
        raise ValueError("Servicio o métrica desconocidos.")
    values = SERIES[service][metric]
    figure = go.Figure(
        go.Scatter(
            x=list(range(1, 8)),
            y=values,
            mode="lines+markers",
            fill="tozeroy",
            line={"color": "#22D3EE", "width": 3},
            marker={"size": 9},
            name=service,
        )
    )
    figure.update_layout(
        template="plotly_dark",
        title=f"{service} / {METRICS[metric]}",
        paper_bgcolor="#0D1117",
        plot_bgcolor="#161B22",
        xaxis_title="Día de la muestra",
        yaxis_title=METRICS[metric],
        margin={"l": 60, "r": 30, "t": 60, "b": 55},
    )
    difference = values[-1] - values[0]
    summary = f"Último valor: {values[-1]:,} · Cambio desde el día 1: {difference:+,}"
    return figure, summary


app = Dash(__name__, title="SignalBoard | Erick Quio")
app.layout = html.Main(
    [
        html.P(
            "ERICK QUIO / OBSERVABILITY LAB",
            style={"color": "#22D3EE", "letterSpacing": "0.15em"},
        ),
        html.H1("SignalBoard", style={"fontSize": "3rem", "marginBottom": "0.3rem"}),
        html.P(
            "Métricas operativas que se entienden. Datos sintéticos, no monitorización en vivo."
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Servicio", htmlFor="service"),
                        dcc.Dropdown(
                            list(SERIES),
                            "API",
                            id="service",
                            clearable=False,
                            style={"color": "#111827"},
                        ),
                    ],
                    style={"flex": "1", "minWidth": "220px"},
                ),
                html.Div(
                    [
                        html.Label("Métrica", htmlFor="metric"),
                        dcc.Dropdown(
                            [
                                {"label": label, "value": key}
                                for key, label in METRICS.items()
                            ],
                            "latency",
                            id="metric",
                            clearable=False,
                            style={"color": "#111827"},
                        ),
                    ],
                    style={"flex": "1", "minWidth": "220px"},
                ),
            ],
            style={"display": "flex", "gap": "1rem", "flexWrap": "wrap"},
        ),
        html.P(id="summary", style={"color": "#A78BFA", "fontSize": "1.2rem"}),
        dcc.Graph(id="signal", config={"displaylogo": False}),
        html.Footer(
            "Demo independiente construida con Plotly Dash · 3 servicios · 2 métricas"
        ),
    ],
    style={
        "background": "#0D1117",
        "color": "#E6EDF3",
        "padding": "2rem",
        "minHeight": "100vh",
        "fontFamily": "system-ui, sans-serif",
    },
)


@app.callback(
    Output("signal", "figure"),
    Output("summary", "children"),
    Input("service", "value"),
    Input("metric", "value"),
)
def update(service, metric):
    return build_figure(service, metric)


if __name__ == "__main__":
    app.run(debug=False)

import pytest
from erick_signalboard import SERIES, app, build_figure


def test_all_service_metric_combinations():
    for service, metrics in SERIES.items():
        for metric, values in metrics.items():
            figure, summary = build_figure(service, metric)
            assert list(figure.data[0].y) == values
            assert str(values[-1]) in summary.replace(",", "")
    with pytest.raises(ValueError):
        build_figure("unknown", "latency")


def test_layout_and_callback_over_http():
    client = app.server.test_client()
    assert client.get("/").status_code == 200
    assert client.get("/_dash-layout").status_code == 200
    output = next(iter(app.callback_map))
    response = client.post(
        "/_dash-update-component",
        json={
            "output": output,
            "outputs": [
                {"id": "signal", "property": "figure"},
                {"id": "summary", "property": "children"},
            ],
            "inputs": [
                {"id": "service", "property": "value", "value": "Agents"},
                {"id": "metric", "property": "value", "value": "requests"},
            ],
            "state": [],
            "changedPropIds": ["service.value"],
        },
    )
    assert response.status_code == 200
    assert "105" in response.get_json()["response"]["summary"]["children"]

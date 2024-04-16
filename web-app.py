import dash
from dash import html
from gov_uk_dashboards.components.plotly import banners

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div(
    [
        html.Div(
            className="banner",
            children=[
                html.Div(
                    className="logo-container",
                    children=html.Img(
                        src=app.get_asset_url("crown-logo.png"),
                        style={"height": "60px", "margin-right": "10px"},
                    ),
                ),
                html.Div("Digital Drafters", className="app-title"),
            ],
        ),
        html.Div(className="ribbon"),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)

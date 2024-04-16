import argparse
import dash
from dash import html, callback, Output, Input, dash_table
import xml.etree.ElementTree as ET
from dash import dcc
import os
import json
import pandas as pd
import time

with open("./assets/sample-notes.json", "r") as f:
    data = json.load(f)
    data = {outer_key: inner_dict for outer_key, inner_dict in data.items()}
    df = pd.DataFrame.from_dict(data, orient="index")


parser = argparse.ArgumentParser(description="Run the web app in demo mode.")
parser.add_argument("--demo", action="store_true", help="Run the app in demo mode.")
args = parser.parse_args()

if args.demo:
    os.environ["DEMO_MODE"] = "1"

external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=GDS+Transport:wght@400;700&display=swap"
]

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=external_stylesheets,
)

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
        html.Br(),
        html.Br(),
        html.H1(
            "Welcome to Digital Drafters!",
            style={"textAlign": "center", "font-family": "Arial"},
        ),
        html.Br(),
        html.H2(
            "The UK Goverment's Legislation Drafting Tool",
            style={"textAlign": "center", "font-family": "Arial"},
        ),
        html.Br(),
        html.Br(),
        dcc.Tabs(
            id="tabs",
            children=[
                dcc.Tab(
                    label="Explanatory Note Generation",
                    value="tab-1",
                    children=html.Div(id="tab-content-1"),
                    style={"textAlign": "center", "font-family": "Arial"},
                ),
                dcc.Tab(
                    label="Legislation Generation",
                    value="tab-2",
                    children=html.Div(id="tab-content-2"),
                    style={"textAlign": "center", "font-family": "Arial"},
                ),
            ],
        ),
    ]
)


@callback(Output("tab-content-1", "children"), [Input("tabs", "value")])
def render_content(tab):
    if (tab == "tab-1") & (os.environ.get("DEMO_MODE") == "1"):

        return html.Div(
            style={
                "fontFamily": "GDS Transport, Arial, sans-serif",
                "backgroundColor": "#F3F2F1",
                "color": "#0B0C0C",
                "padding": "20px",
                "textAlign": "center",
            },
            children=[
                html.H1(
                    "Enter URL of the Legislation",
                    style={"marginBottom": "20px", "color": "#000000"},
                ),
                dcc.Input(
                    id="url-input",
                    type="text",
                    placeholder="Enter URL",
                    style={
                        "marginBottom": "20px",
                        "padding": "8px",
                        "width": "50%",
                        "border": "1px solid #000000",
                    },
                ),
                html.Button(
                    "Submit",
                    id="submit-button",
                    n_clicks=0,
                    style={
                        "marginBottom": "20px",
                        "backgroundColor": "#000000",
                        "color": "#FFFFFF",
                        "border": "none",
                        "padding": "10px 20px",
                        "cursor": "pointer",
                    },
                ),
                html.Div(id="output-table", style={"marginBottom": "20px"}),
            ],
        )
    elif tab == "tab-1":
        return html.Div("Not Implemented")


@callback(Output("tab-content-2", "children"), [Input("tabs", "value")])
def render_content(tab):
    if (tab == "tab-2") & (os.environ.get("DEMO_MODE") == "1"):

        return html.Div(
            className="pdf-container",
            children=[
                html.ObjectEl(
                    data="assets/samplepdf.pdf",
                    type="application/pdf",
                    style={"width": "800px", "height": "600px"},
                ),
            ],
        )

    elif tab == "tab-2":
        return html.Div("This is Tab 2")


@app.callback(
    dash.dependencies.Output("output-table", "children"),
    [dash.dependencies.Input("submit-button", "n_clicks")],
)
def update_output(n_clicks):
    if n_clicks > 0:
        # Create DataTable
        table = dash_table.DataTable(
            id="table",
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("records"),
            style_cell={
                "textAlign": "center",
                "minWidth": "100px",
                "maxWidth": "300px",
                "whiteSpace": "normal",
            },  # Center align the cells in the table
        )

        time.sleep(1)

        return table
    else:
        return None


if __name__ == "__main__":
    app.run_server(debug=True)

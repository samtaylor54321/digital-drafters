import argparse
import dash
from dash import html, callback, Output, Input, dash_table
from dash import dcc
import os
import json
import pandas as pd
import time
from src.explanation_app import get_summary, get_line_by_line_summary

with open("./assets/sample-line-by-line.json", "r") as f:
    data = json.load(f)
    data = {outer_key: inner_dict for outer_key, inner_dict in data.items()}
    df = pd.DataFrame.from_dict(data, orient="index")

with open("./assets/sample-summary.txt", "r") as f:
    text = f.read()

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
                html.Br(),
                html.Div(id="output-text"),
                html.Br(),
                html.Div(id="output-table", style={"marginBottom": "20px"}),
            ],
        )
    elif tab == "tab-1":
        return html.Div("Not Implemented")


@callback(Output("tab-content-2", "children"), [Input("tabs", "value")])
def render_content(tab):
    if (tab == "tab-2") & (os.environ.get("DEMO_MODE") == "1"):

        return html.Div(
            style={
                "fontFamily": "GDS Transport, Arial, sans-serif",
                "color": "#0B0C0C",
                "padding": "20px",
                "textAlign": "center",
            },
            children=[
                html.H1(
                    "Enter URL of the Policy Instructions",
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
                    "Upload File",
                    id="upload-button",
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
                html.Br(),
                html.Div(
                    id="output-pdf",
                    className="pdf-container",
                ),
                html.Br(),
            ],
        )

        # return

    elif tab == "tab-2":
        return html.Div("This is Tab 2")


@app.callback(
    dash.dependencies.Output("output-text", "children"),
    [
        dash.dependencies.Input("submit-button", "n_clicks"),
        dash.dependencies.Input("input-url", "value"),
    ],
)
def update_output_text(n_clicks, value):
    if os.environ.get("DEMO_MODE") == "1":
        if n_clicks > 0:
            content = html.Div(
                [
                    html.H3("Overall Summary", style={"marginBottom": "20px"}),
                    html.Br(),
                    dcc.Markdown(f"```\n{text}\n```"),
                ]
            )
            time.sleep(1)

            return content
        else:
            return None
    else:
        if n_clicks > 0:
            text = get_summary(value)

            content = html.Div(
                [
                    html.H3("Overall Summary", style={"marginBottom": "20px"}),
                    html.Br(),
                    dcc.Markdown(f"```\n{text}\n```"),
                ]
            )

            return content
        else:
            return None


@app.callback(
    dash.dependencies.Output("output-table", "children"),
    [
        dash.dependencies.Input("submit-button", "n_clicks"),
        dash.dependencies.Input("input-url", "value"),
    ],
)
def update_output_table(n_clicks, value):
    if os.environ.get("DEMO_MODE") == "1":
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

            table = html.Div([html.H3("Line by Line Summary"), html.Br(), table])

            time.sleep(1)

            return table
        else:
            return None
    else:
        if n_clicks > 0:
            new_df = get_line_by_line_summary(value)

            table = dash_table.DataTable(
                id="table",
                columns=[{"name": i, "id": i} for i in new_df.columns],
                data=new_df.to_dict("records"),
                style_cell={
                    "textAlign": "center",
                    "minWidth": "100px",
                    "maxWidth": "300px",
                    "whiteSpace": "normal",
                },  # Center align the cells in the table
            )

            table = html.Div([html.H3("Line by Line Summary"), html.Br(), table])

            return table
        else:
            return None


@app.callback(
    dash.dependencies.Output("output-pdf", "children"),
    [dash.dependencies.Input("upload-button", "n_clicks")],
)
def update_output_pdf(n_clicks):
    if n_clicks > 0:
        time.sleep(5)

        return (
            html.ObjectEl(
                data="assets/sample-legislation.pdf",
                type="application/pdf",
                style={"width": "800px", "height": "600px"},
            ),
        )
    else:
        return None


if __name__ == "__main__":
    app.run_server(debug=True)

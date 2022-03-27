import dash
from dash import dcc, html, dash_table, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv("Amazon.csv")


external_stylesheets = [dbc.themes.LUX]

dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash_app.server

# create datatable function from dataframe
def create_table(dataframe, max_rows=10):

    # round the values to 2 decimal places
    dataframe = dataframe.round(2)

    # Convert the High, Low, Open, Close, Adj Close columns to dollar values
    dataframe["High"] = dataframe["High"].map("${:,.2f}".format)
    dataframe["Low"] = dataframe["Low"].map("${:,.2f}".format)
    dataframe["Open"] = dataframe["Open"].map("${:,.2f}".format)
    dataframe["Close"] = dataframe["Close"].map("${:,.2f}".format)
    dataframe["Adj Close"] = dataframe["Adj Close"].map("${:,.2f}".format)

    # Sort dataframe by newest date first:
    dataframe = dataframe.sort_values(by="Date", ascending=False)

    table = dash_table.DataTable(
        data=dataframe.to_dict("records"),
        columns=[{"name": i, "id": i} for i in dataframe.columns],
        style_table={"overflowX": "scroll"},
        # style_cell={"textAlign": "center"},
        style_header={"backgroundColor": "white", "fontWeight": "bold"},
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
        ],
        style_as_list_view=True,
        style_cell={
            "height": "auto",
            "minWidth": "0px",
            "maxWidth": "180px",
            "width": "180px",
            "whiteSpace": "normal",
        },
        fixed_rows={"headers": True, "data": 0},
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
    )

    return table


def create_candlestick(df):
    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
        )
    )

    return fig


dash_app.layout = html.Div(
    [
        dcc.Store(id="memory", data=df.to_dict("records")),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.H1("Amazon Dashboard", className="display-3"),
                            className="mb-2",
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.H6(children="Visualising the Amazon Stock Price"),
                            className="mb-4",
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                html.H3(
                                    children="Latest Update",
                                    className="text-center text-light bg-dark",
                                ),
                                body=True,
                                color="dark",
                            ),
                            className="mb-4",
                        )
                    ]
                ),
                dcc.RadioItems(
                    id="table_type",
                    options=[],
                    value="Condensed table",
                    labelStyle={"display": "inline-block"},
                ),
                html.Div(id="table-output"),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                html.H3(
                                    children="Candlestick Chart",
                                    className="text-center text-light bg-dark",
                                ),
                                body=True,
                                color="dark",
                            ),
                            className="mt-4 mb-5",
                        )
                    ]
                ),
                html.Div(id="candlestick-output"),
            ]
        ),
    ]
)


@callback(
    Output("table-output", "children"),
    Output("candlestick-output", "children"),
    Input("memory", "data"),
)
def update_page(data):
    if data is None:
        return html.Div(), html.Div()
    else:
        dataframe = pd.DataFrame.from_dict(data)
        return create_table(dataframe), dcc.Graph(figure=create_candlestick(dataframe))


if __name__ == "__main__":
    dash_app.run_server(host="127.0.0.1", debug=True)

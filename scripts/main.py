#Punkt wejścia do aplikacji

import dash
from dash import html


app = dash.Dash(__name__)

app.layout = html.Div([
    html.P("Hello world")
    ])

if __name__ == "__main__":
    app.run(debug=True)

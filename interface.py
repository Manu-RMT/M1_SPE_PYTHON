from dash import Dash, dash_table,html,dcc
import pandas as pd


app = Dash(__name__)
app.layout = html.Div(children=[
    # Titre
    html.H1(children="Interface Python", style={"fontSize": "48px", "color": "red", "text-align": "center"}),
    
    html.Br(),
    
    html.Label('Barre de recherhce'),
    dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'],
                  ['Montréal', 'San Francisco'],
                  multi=True),
    html.Br(),
    

    ], style={'padding': '2rem', 'flex': 1})



if __name__ == '__main__':
    app.run_server(debug=False)
    

from dash import Dash, dash_table,html,dcc,Input, Output, State
import pandas as pd
import Projet as pr 

app = Dash(__name__)
app.layout = html.Div(children=[
    # Titre
    html.H1(children="Interface Python", style={"fontSize": "48px", "color": "red", "text-align": "center"}),
    
    html.Br(),
    html.Div([
        html.Label('Barre de recherche'),
        dcc.Input(id="search", type="text", placeholder="Saisissez un mot", style= {'margin': '2rem'}),
        html.Button('Submit', id='submit-val',n_clicks=0),
        html.Div(id='container-button-basic',
                 children='Enter a value and press submit',style={'padding':'1rem 0rem'})     
        ]
        ,style = {"fontSize": "20px",'text-align':'center'}
        
        )
   
    
    
    ], style={'padding': '2rem', 'flex': 1})



@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('search', 'value')
)
    
def update_output(n_clicks, value):
    if value is not None:        
        nb_contain_word,nb_nocontain_word = pr.main(value)
        return (html.P('{} documents contiennent le mot {}'.format(nb_contain_word,value)),
                html.Br(),
                '{} documents ne contiennent pas le mot {}'.format(nb_nocontain_word,value))
          

if __name__ == '__main__':
    app.run_server(debug=False)
    

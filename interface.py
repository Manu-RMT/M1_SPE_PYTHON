from dash import Dash, dash_table,html,dcc,Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import Projet as pr 


def load_data(path_file :str):
     return pd.read_csv(path_file,sep=';')
 
cc = load_data('corpus.csv')
       
app = Dash(__name__)

    
def generate_table(df):
    return (
           dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        tooltip_data=[
            {
                column: {'value': str(value), 'type': 'markdown'}
                for column, value in row.items()
            } for row in df.to_dict('records')
        ],
    
        # Overflow into ellipsis
        style_cell={
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 0,
            'padding': '1rem',
            "text-align": "center"
        },
        tooltip_delay=0,
        tooltip_duration=None
        )
    )


app.title = "Football WORD"
app.layout = html.Div(children=[
    # Titre
    html.H1(children="Interface Python", style={"fontSize": "48px", "color": "red", "text-align": "center"}),
    
    html.Br(),
    html.Div([
        html.Label('Barre de recherche'),
        dcc.Input(id="search", type="text", placeholder="Saisissez un mot", style= {'margin': '2rem'}),
        html.Button('Submit', id='submit-val',n_clicks=0),
        html.Div(id='container-button-basic',
                 children='Entrez une valeur et appuyer sur SUBMIT',style={'padding':'1rem 0rem'})     
        ]
        ,style = {"fontSize": "20px",'text-align':'center'}
        
        ),
        
        html.Div('Quentin MONTALAND & Manuel RAMANITRA M1 Informatique ',style={"font-weight":"bold","position":'relative', "bottom":0, "left":0, "right":0, "padding": "1rem", "fontSize": "16px", "color": "black", "text-align": "center"})
    
    ], style={'padding': '2rem', 'flex': 1},
    )

@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('search', 'value')
)
    
def update_output(n_clicks, value):
    value = value.split(" ")
    value = list(filter(any, value))
    
    if len(value) > 0 :  # value is not None          
        nb_contain_word,nb_nocontain_word, contain_value = pr.main(value)
        print(contain_value)
        value = " ou ".join(value)
        return (html.Div('{} documents contiennent le mot {}'.format(nb_contain_word,value)),
                html.Br(),
                '{} documents ne contiennent pas le mot {}'.format(nb_nocontain_word,value),
                html.Br(),
                html.Div(children=[
                    html.H4(children='Tableau des documents ',style={"text-align":"left"}),
                    generate_table(contain_value)]),
              ) 
    

    
if __name__ == '__main__':
    app.run_server(debug=False)
    

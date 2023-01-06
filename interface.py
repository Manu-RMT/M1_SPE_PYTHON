from dash import Dash, dash_table,html,dcc,Input, Output, State
import Projet as pr 

# initialisation de DAah       
app = Dash(__name__)

#genère le tableau des documents obtenu avec le mot saisie    
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
        page_size=20,
        tooltip_delay=0,
        tooltip_duration=None
        )
    )


# permet l'affichage de tous les elements
app.title = "Football Documents"
app.layout = html.Div(children=[
    # Titre
    html.H1(children="Exploration de documents de football", style={"fontSize": "48px", "color": "red", "text-align": "center"}),
    
    html.Br(),
    html.Div([
        html.Label('Barre de recherche'),
        dcc.Input(id="search", type="text", placeholder="Saisir un mot/des mot(s)-clé(s)", style= {'margin': '2rem','width':"22%"}),
        html.Button('Rechercher', id='submit-val',n_clicks=0),
        html.Div(id='container-button-basic',
                 children='Entrez une valeur et appuyer sur SUBMIT',style={'padding':'1rem 0rem'})     
        ]
        ,style = {"fontSize": "20px",'text-align':'center'}
        
        ),
        
        html.Div('Quentin MONTALAND & Manuel RAMANITRA M1 Informatique ',style={"font-weight":"bold","position":'relative', "bottom":0, 
                                                                                "left":0, "right":0, "padding": "1rem", "fontSize": "16px", 
                                                                                "color": "black", "text-align": "center"})
    
    ], style={'padding': '2rem', 'flex': 1},
    )

# permet l'actualisation du mot
@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('search', 'value')
)

#gère la mise à jour des mots saisies + affiche les elements après la barre de recherche    
def update_output(n_clicks, value):
    value = value.lower()
    value = value.split(" ") # séparation des mots clés
    value = list(filter(any, value)) # supprime les espaces inutiles
    
    if len(value) > 0 :  # value is not None          
        nb_contain_word, nb_nocontain_word, contain_value, taille_vocab, top20_tf, top20_idf = pr.main(value)
        value = " ou ".join(value)
        return (html.Div('{} documents contiennent le mot {} et constituent le corpus value '.format(nb_contain_word,value), 
                         style={"text-align":"left"}),
                html.Br(),
                html.Div('{} documents ne contiennent pas le mot {}  et constituent le corpus novalue'.format(nb_nocontain_word,value),
                         style={"text-align":"left"}),
                html.Br(),
                html.Div(taille_vocab,style={"text-align":"left"}),
                html.Br(),
                html.Div(top20_tf,style={"margin-top":"2rem","text-align":"left"}),
                html.Br(),
                html.Div(top20_idf,style={"text-align":"left"}),
                html.Br(),
                html.Div(children=[
                    html.H4(children='Tableau du corpus value ',style={"text-align":"left"}),
                    generate_table(contain_value)]),
              ) 
    

 # lance le serveur   
if __name__ == '__main__':
        app.run_server(debug=False)
    

#step 1
from dash import Dash, Input, Output, State, html, dcc, dash_table, callback
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc


df = pd.read_csv('aac_shelter_outcomes.csv')

app = Dash(__name__, external_stylesheets =[dbc.themes.BOOTSTRAP])

fig = px.histogram(df, x="animal_type")

email_input = dbc.Row([
        dbc.Label("Email"
                , html_for="example-email-row"
                , width=2),
        dbc.Col(dbc.Input(
                type="email"
                , id="example-email-row"
                , placeholder="Enter email"
            ),width=10,
        )],className="mb-3"
)

user_input = dbc.Row([
        dbc.Label("Password", html_for="example-name-row", width=2),
        dbc.Col(
            dbc.Input(
                type="text"
                , id="example-name-row"
                , placeholder="Enter name"
                , maxLength = 80
            ),width=10
        )], className="mb-3"
)

message = dbc.Row([
        dbc.Label("Message", html_for="example-message-row", width=2)
        ,dbc.Col(
            dbc.Textarea(id = "example-message-row"
                , className="mb-3"
                , placeholder="Enter message"
                , required = True)
            , width=10)
        ], className="mb-3")

def contact_form():
    markdown = ''' # Send a message if you have a comment, question, or concern. Thank you!'''   
    form = html.Div([ dbc.Container([
            dcc.Markdown(markdown)
            , html.Br()
            , dbc.Card(
                dbc.CardBody([
                     dbc.Form([email_input
                        , user_input
                        , message])
                ,html.Div(id = 'div-button', children = [
                    dbc.Button('Submit'
                    , color = 'primary'
                    , id='button-submit'
                    , n_clicks=0)
                ]) #end div
                ])#end cardbody
            )#end card
            , html.Br()
            , html.Br()
        ])
        ])
    return form

app.layout = html.Div([
    html.H1(
        children='Animal Shelter Stats',
        style={
            'textAlign': 'center',
            'color': 'blue'
        }
    )
    , html.Br()
    , html.H5('Animal Types')
    , dcc.Graph(id='ani-type',
        figure=fig
    )
    , html.H5('Animal Type')
    , dcc.Dropdown(id = 'ani-type-drop',
                    options=[{'label': i, 'value': i} 
                    for i in sorted(set(df['animal_type']))],
                    multi=True
                )
    , html.Br()
    , html.H5('Breeds')
    , dcc.Graph(id='breeds-graph')
    , contact_form()


])
    


@app.callback(
    Output('breeds-graph', 'figure'),
    Input('ani-type-drop', 'value'))
def update_figure(anitype):
    filtered_df = df['breed'].loc[df['animal_type'].isin(anitype)]

    fig = px.histogram(filtered_df, x="breed")

    return fig

@app.callback(Output('div-button', 'children'),
     Input("button-submit", 'n_clicks')
     ,Input("example-email-row", 'value')
     ,Input("example-name-row", 'value')
     ,Input("example-message-row", 'value')
    )
def submit_message(n, email, name, message):
    
    port = 465  # For SSL
    sender_email = email
    receiver_email = '<your email address here>'
      
    # Create a secure SSL context
    context = ssl.create_default_context()       
    
    if n > 0:
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login("<you email address here>", '<you email password here>')
            server.sendmail(sender_email, receiver_email, message)
            server.quit()
        return [html.P("Message Sent")]
    else:
        return[dbc.Button('Submit', color = 'primary', id='button-submit', n_clicks=0)]


#step 4
if __name__ == "__main__":
     app.run_server(debug = True)

# Benjamin Rösch, 20.11.2020
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

# Manually import csv data tables
# exported fields: station_name,delay,departure_time,destination

# S8
df = pd.read_csv('Dashboard/S8FlughafenMünchen5k.csv')

# exported fields: station_name,delay,departure_time,destination

df = pd.DataFrame({
    "Station": df['station_name'], "Verspätung": df['delay'], "Abfahrtszeit": df["departure_time"],
    "Endstation": df["destination"]
})

avgdelaynumber = len(df[df['Verspätung'] != 0]) / len(df)
avgdelay = round(sum(df['Verspätung']) / len(df), 2)

app.layout = html.Div(children=[

    html.H1(children='S-Bahn München Verspätungen',
            style={'textAlign': 'center',
                   #   'color': colors['text']
                   }),

    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'S6 nach Ebersberg', 'value': 'Ebersberg'},
            {'label': 'S6 nach Tutzing ', 'value': 'Tutzing'},
            {'label': 'S8 nach Herrsching', 'value': 'Herrsching'},
            {'label': 'S8 nach Flughafen München', 'value': 'Flughafen München'}],
        placeholder="Select a S-Bahn line"),
    html.Div([dcc.Dropdown(
        id='dropdown_start',
        options=[
            {'label': 'Herrsching', 'value': 'Herrsching'}
        ],
        placeholder="From"),

        dcc.Dropdown(
            id='dropdown_end',
            options=[
                {'label': 'Neugilching', 'value': 'Neugilching'},
                {'label': 'Seefeld-Hechendorf', 'value': 'Seefeld-Hechendorf'},
                {'label': 'Steinebach', 'value': 'Steinebach'},
                {'label': 'Weßling', 'value': 'Weßling'},
                {'label': 'Neugilching', 'value': 'Neugilching'},
                {'label': 'Gilching-Argelsried', 'value': 'Gilching-Argelsried'},
                {'label': 'Geisenbrunn', 'value': 'Geisenbrunn'},
                {'label': 'Germering-Unterpfaffenhofen', 'value': 'Germering-Unterpfaffenhofen'},
                {'label': 'Harthaus', 'value': 'Harthaus'},
                {'label': 'Freiham', 'value': 'Freiham'},
                {'label': 'Neuaubing', 'value': 'Neuaubing'},

            ],
            placeholder="To",
            value='Herrsching'),

    ],
        # style={'columnCount': 2
    ),

    html.Div([
        html.P(json_entry)
        for json_entry in ['', '']
    ]),

    html.Div(children=str(str(int(round(avgdelaynumber * 100))) + '% of S-Bahns delayed in total on this line. '),
             style={
                 # 'textAlign': 'center',
                 # 'color': colors['text']

             }),

    html.Div(children=str(str(((avgdelay))) + ' minutes average delay on this line.'), style={
        # 'textAlign': 'center',
        # 'color': colors['text']

    }),
    dcc.Graph(id='graph'),

])


@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_figure(value):
    dff = df[df['Endstation'].eq(value)]

    # Set order for stations
    if value == 'Flughafen München':
        order = ['Herrsching', 'Seefeld-Hechendorf', 'Steinebach', 'Weßling', 'Neugilching', 'Gilching-Argelsried',
                 'Geisenbrunn',
                 'Germering-Unterpfaffenhofen', 'Harthaus', 'Freiham', 'Neuaubing',
                 'Westkreuz', 'Pasing', 'Laim', 'Hirschgarten', 'Donnersbergerbrücke', 'Hackerbrücke', 'Hauptbahnhof',
                 'Karlsplatz',
                 'Marienplatz', 'Isartor', 'Rosenheimer Platz', 'Ostbahnhof München', 'Leuchtenbergring', 'Daglfing',
                 'Englschalking', 'Johanneskirchen', 'Unterföhring', 'Ismaning', 'Hallbergmoos',
                 'Flughafen Besucherpark']

        dff['Station'] = pd.Categorical(dff['Station'], order)
        dff.sort_values(by=['Station'], inplace=True)

        dff = dff.groupby('Station').mean().reset_index()

    # Make plot
    fig = px.bar(dff, x="Station", y="Verspätung", title="Durchschnittliche Verspätung in Minuten")

    fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=0.6)
    return fig


if __name__ == '__main__':
    app.run_server()

# Usefull code:
# import datetime
# make list with datetimes-format departures from list with departures:
# timel = [ datetime.datetime.strptime(i,'%Y-%m-%d %H:%M:%S') for i in l]

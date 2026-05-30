import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# 1. Φόρτωση του συγχωνευμένου αρχείου δεδομένων που φτιάξαμε
df = pd.read_csv('merged_urban_data.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Αρχικοποίηση της εφαρμογής Dash
app = dash.Dash(__name__)
app.title = "Kozani Smart City Dashboard"

# 2. Διάταξη της σελίδας (Layout)
app.layout = html.Div(style={'fontFamily': 'Segoe UI, sans-serif', 'padding': '20px', 'backgroundColor': '#f8f9fa'},
                      children=[

                          # Τίτλος Dashboard
                          html.Div(style={'textAlign': 'center', 'marginBottom': '30px', 'padding': '10px',
                                          'backgroundColor': '#2b5c8f', 'color': 'white', 'borderRadius': '5px'},
                                   children=[
                                       html.H1("Αστική Κινητικότητα & Τοπικές Εκδηλώσεις - Κοζάνη 2025"),
                                       html.P(
                                           "Διερεύνηση συσχετίσεων και μοτίβων μετακίνησης βάσει της Ροής Εργασιών Οπτικοποίησης")
                                   ]),

                          # Ενότητα Φίλτρων (Dropdowns)
                          html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px',
                                          'justifyContent': 'center'}, children=[
                              html.Div(style={'width': '40%', 'padding': '10px', 'backgroundColor': 'white',
                                              'borderRadius': '5px', 'boxShadow': '0px 2px 4px rgba(0,0,0,0.1)'},
                                       children=[
                                           html.Label("Επιλέξτε Τύπο Ημέρας:",
                                                      style={'fontWeight': 'bold', 'color': '#333'}),
                                           dcc.Dropdown(
                                               id='daytype-dropdown',
                                               options=[{'label': 'Όλες οι Ημέρες', 'value': 'All'}] +
                                                       [{'label': t, 'value': t} for t in df['DayType'].unique()],
                                               value='All',
                                               clearable=False
                                           )
                                       ]),
                              html.Div(style={'width': '40%', 'padding': '10px', 'backgroundColor': 'white',
                                              'borderRadius': '5px', 'boxShadow': '0px 2px 4px rgba(0,0,0,0.1)'},
                                       children=[
                                           html.Label("Κατάσταση Αργίας:",
                                                      style={'fontWeight': 'bold', 'color': '#333'}),
                                           dcc.Dropdown(
                                               id='holiday-dropdown',
                                               options=[
                                                   {'label': 'Όλες', 'value': 'All'},
                                                   {'label': 'Αργία', 'value': 1},
                                                   {'label': 'Εργάσιμη', 'value': 0}
                                               ],
                                               value='All',
                                               clearable=False
                                           )
                                       ])
                          ]),

                          # Ενότητα Γραφημάτων
                          html.Div(style={'display': 'flex', 'flexDirection': 'column', 'gap': '20px'}, children=[

                              # Γράφημα 1: Χρονοσειρά / Τάση
                              html.Div(style={'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '5px',
                                              'boxShadow': '0px 2px 4px rgba(0,0,0,0.1)'}, children=[
                                  dcc.Graph(id='trend-plot')
                              ]),

                              # Γράφημα 2: Διάγραμμα Διασποράς (Συσχέτιση)
                              html.Div(style={'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '5px',
                                              'boxShadow': '0px 2px 4px rgba(0,0,0,0.1)'}, children=[
                                  dcc.Graph(id='scatter-plot')
                              ])
                          ])
                      ])


# 3. Συναρτήσεις Callbacks για τη Δυναμική Αλληλεπίδραση
@app.callback(
    [Output('trend-plot', 'figure'),
     Output('scatter-plot', 'figure')],
    [Input('daytype-dropdown', 'center' if False else 'value'),
     Input('holiday-dropdown', 'value')]
)
def update_graphs(selected_daytype, selected_holiday):
    # Αντίγραφο του dataframe για φιλτράρισμα
    filtered_df = df.copy()

    # Εφαρμογή φίλτρου DayType
    if selected_daytype != 'All':
        filtered_df = filtered_df[filtered_df['DayType'] == selected_daytype]

    # Εφαρμογή φίλτρου IsHoliday
    if selected_holiday != 'All':
        filtered_df = filtered_df[filtered_df['IsHoliday'] == int(selected_holiday)]

    # Γράφημα Τάσης: Όγκος Κυκλοφορίας και Custom Score
    fig_trend = px.line(
        filtered_df,
        x='Date',
        y='TrafficCount',
        title='Διακύμανση Όγκου Κυκλοφορίας στο Επιλεγμένο Πλαίσιο',
        labels={'TrafficCount': 'Όγκος Κυκλοφορίας', 'Date': 'Ημερομηνία'},
        template='plotly_white'
    )
    fig_trend.update_traces(line_color='#2b5c8f')

    # Διάγραμμα Διασποράς: Αναμενόμενη Συμμετοχή (Attendance) vs Πληρότητα Parking
    fig_scatter = px.scatter(
        filtered_df,
        x='Attendance',
        y='ParkingOccupancy',
        color='EventType',
        size='TransportStrainIndex',
        title='Συσχέτιση Συμμετοχής σε Εκδηλώσεις & Πληρότητας Parking',
        labels={'Attendance': 'Συμμετοχή στην Εκδήλωση', 'ParkingOccupancy': 'Πληρότητα Parking (%)'},
        hover_data=['EventName', 'Date', 'PT_Preference_Score'],  # Details-on-demand
        template='plotly_white'
    )

    return fig_trend, fig_scatter


# Εκκίνηση του server
if __name__ == '__main__':
    app.run(debug=True)
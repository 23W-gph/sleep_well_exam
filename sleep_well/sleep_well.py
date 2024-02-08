import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


# Group by 'Occupation', 'Quality of Sleep', and 'Sleep Duration'
df = (pd.read_csv('sleep_well.csv')).groupby(['Occupation', 'Quality of Sleep', 'Sleep Duration']).size().reset_index(name='Count')

app = dash.Dash(__name__)

app.layout = html.Div([
    # Page header
    html.H2("Sleep as a pillar of brain health", style={'textAlign': 'center'}),

     # Detailed text
    html.P("""
        Background: Sleep is a complex process affecting the whole body and is an essential part of physical and mental health and wellbeing. 
        Sleep, alongside diet and physical activity, has been described as one of the three pillars of health and a "fundamental building block" 
        for achieving and maintaining good health.
    """),
    html.P("""
        Problem: When quality, quantity and consistency of sleep are insufficient or compromised, an individual's sleep health will be poor or 
        suboptimal, being more likely to experience negative health and wellbeing consequences associated with poor sleep.
    """),
    html.P("""
        Goal: To improve population sleep health, to reduce preventable risk factors by examining the relationship between the subjective quality 
        of sleep and different modifiable factors.
    """),
    html.P("""
        This dynamic visualization provides information about perceived quality of sleep related to 2 factors: ocupation and quantity of sleep.
    """),


    html.P("Select a Quality of Sleep from the dropdown box to display the plot of Occupation vs. Sleep Duration.", style={'textAlign': 'center', 'font-weight':'bold'}),
    
    # Dropdown for selecting 'Quality of Sleep'
    dcc.Dropdown(
        id='quality-sleep-dropdown',
        options=[{'label': i, 'value': i} for i in sorted(df['Quality of Sleep'].unique())],
        value=sorted(df['Quality of Sleep'].unique())[0],  # Default selection
        style={'width': '30%', 'margin': 'auto'}  # Center the dropdown
    ),
    
    dcc.Graph(id='occupation-sleep-duration-plot')
], style={'padding': '20px', 'maxWidth': '800px', 'margin': 'auto'})

@app.callback(
    Output('occupation-sleep-duration-plot', 'figure'),
    [Input('quality-sleep-dropdown', 'value')]
)
def update_graph(selected_quality):
    # Filter the DataFrame based on the selected 'Quality of Sleep'
    filtered_df = df[df['Quality of Sleep'] == selected_quality]


    # Use a scatter plot to show individual data points
    fig = px.scatter(filtered_df, x='Occupation', y='Sleep Duration',
                     title=f'Sleep Duration for Quality of Sleep: {selected_quality}',
                     hover_data=['Occupation', 'Sleep Duration', 'Count'])

    # Optional: Customize the plot appearance
    fig.update_traces(marker=dict(size=10),  # Adjust marker size
                      selector=dict(mode='markers'))  # Ensure only markers are shown
    fig.update_xaxes(categoryorder='total descending')  # Sort categories by descending order of appearance
    fig.update_yaxes(title_text='Sleep Duration, h')


    return fig

if __name__ == '__main__':
    app.run_server(debug=True)



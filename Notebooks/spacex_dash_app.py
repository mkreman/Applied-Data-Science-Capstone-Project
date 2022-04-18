# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=['All Sites'] + spacex_df['Launch Site'].unique().tolist(),
                                             placeholder='Please select a launch site',
                                             value='All Sites'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the
                                # site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value')])
def update_pie_graph(site_dropdown):
    if site_dropdown == 'All Sites':
        data = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(data, names='Launch Site', hole=0.3,
                     title='Total Success Launches By all sites')
    else:
        data = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        fig = px.pie(data, names='class', hole=0.3,
                     title=f'Total Success Launches for site {site_dropdown}')
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def update_scatter_graph(site_dropdown, payload_slider):
    if site_dropdown == 'All Sites':
        data = spacex_df
    else:
        data = spacex_df[spacex_df['Launch Site'] == site_dropdown]

    low, high = payload_slider
    mask = (data['Payload Mass (kg)'] > low) & (data['Payload Mass (kg)'] < high)
    fig = px.scatter(data[mask],
                     x='Payload Mass (kg)',
                     y='class',
                     color='Booster Version',
                     size='Payload Mass (kg)',
                     hover_data=['Payload Mass (kg)'])
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Since the provided CSV is corrupted, I'll create sample HR data
def create_sample_hr_data():
    departments = ['HR', 'Finance', 'Engineering', 'Marketing', 'Sales']
    positions = ['Manager', 'Associate', 'Director', 'VP', 'Intern']
    locations = ['New York', 'London', 'Tokyo', 'San Francisco', 'Berlin']
    
    data = {
        'Employee_ID': range(1, 101),
        'Name': [f'Employee {i}' for i in range(1, 101)],
        'Department': np.random.choice(departments, 100),
        'Position': np.random.choice(positions, 100),
        'Salary': np.random.randint(40000, 150000, 100),
        'Age': np.random.randint(22, 65, 100),
        'Tenure': np.random.randint(1, 15, 100),
        'Location': np.random.choice(locations, 100),
        'Gender': np.random.choice(['Male', 'Female'], 100),
        'Performance_Rating': np.random.randint(1, 6, 100),
        'Engagement_Score': np.random.randint(1, 101, 100)
    }
    return pd.DataFrame(data)

df = create_sample_hr_data()

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("HR Analytics Dashboard", style={'textAlign': 'center'}),
    
    # Filters
    html.Div([
        html.Div([
            html.Label("Select Department:"),
            dcc.Dropdown(
                id='dept-filter',
                options=[{'label': dept, 'value': dept} for dept in df['Department'].unique()],
                value=None,
                multi=True,
                placeholder="All Departments"
            )
        ], style={'width': '30%', 'display': 'inline-block', 'margin': '10px'}),
        
        html.Div([
            html.Label("Select Position:"),
            dcc.Dropdown(
                id='position-filter',
                options=[{'label': pos, 'value': pos} for pos in df['Position'].unique()],
                value=None,
                multi=True,
                placeholder="All Positions"
            )
        ], style={'width': '30%', 'display': 'inline-block', 'margin': '10px'}),
        
        html.Div([
            html.Label("Select Location:"),
            dcc.Dropdown(
                id='location-filter',
                options=[{'label': loc, 'value': loc} for loc in df['Location'].unique()],
                value=None,
                multi=True,
                placeholder="All Locations"
            )
        ], style={'width': '30%', 'display': 'inline-block', 'margin': '10px'})
    ]),
    
    # Charts Row 1
    html.Div([
        html.Div([
            dcc.Graph(id='salary-distribution')
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='age-tenure-scatter')
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ]),
    
    # Charts Row 2
    html.Div([
        html.Div([
            dcc.Graph(id='dept-position-heatmap')
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='performance-gender-bar')
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ]),
    
    # Charts Row 3
    html.Div([
        html.Div([
            dcc.Graph(id='engagement-location-box')
        ], style={'width': '100%'})
    ]),
    
    # Data table
    html.Div([
        html.H3("Employee Data"),
        html.Div(id='data-table')
    ])
])

# Callbacks for interactivity
@app.callback(
    [Output('salary-distribution', 'figure'),
     Output('age-tenure-scatter', 'figure'),
     Output('dept-position-heatmap', 'figure'),
     Output('performance-gender-bar', 'figure'),
     Output('engagement-location-box', 'figure'),
     Output('data-table', 'children')],
    [Input('dept-filter', 'value'),
     Input('position-filter', 'value'),
     Input('location-filter', 'value')]
)
def update_dashboard(selected_depts, selected_positions, selected_locations):
    # Filter data based on selections
    filtered_df = df.copy()
    
    if selected_depts:
        if isinstance(selected_depts, str):
            selected_depts = [selected_depts]
        filtered_df = filtered_df[filtered_df['Department'].isin(selected_depts)]
    
    if selected_positions:
        if isinstance(selected_positions, str):
            selected_positions = [selected_positions]
        filtered_df = filtered_df[filtered_df['Position'].isin(selected_positions)]
    
    if selected_locations:
        if isinstance(selected_locations, str):
            selected_locations = [selected_locations]
        filtered_df = filtered_df[filtered_df['Location'].isin(selected_locations)]
    
    # Create figures
    salary_fig = px.histogram(
        filtered_df, 
        x='Salary', 
        color='Department', 
        title='Salary Distribution by Department',
        nbins=20
    )
    
    scatter_fig = px.scatter(
        filtered_df,
        x='Age',
        y='Tenure',
        color='Position',
        size='Salary',
        hover_name='Name',
        title='Age vs Tenure (Size by Salary)'
    )
    
    heatmap_fig = px.density_heatmap(
        filtered_df,
        x='Department',
        y='Position',
        z='Salary',
        histfunc='avg',
        title='Average Salary by Department and Position'
    )
    
    performance_fig = px.bar(
        filtered_df.groupby(['Gender', 'Performance_Rating']).size().reset_index(name='Count'),
        x='Performance_Rating',
        y='Count',
        color='Gender',
        barmode='group',
        title='Performance Rating Distribution by Gender'
    )
    
    engagement_fig = px.box(
        filtered_df,
        x='Location',
        y='Engagement_Score',
        color='Department',
        title='Engagement Score by Location and Department'
    )
    
    # Create data table
    table = dash.dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in filtered_df.columns],
        data=filtered_df.to_dict('records'),
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={
            'height': 'auto',
            'minWidth': '80px', 'width': '120px', 'maxWidth': '180px',
            'whiteSpace': 'normal'
        }
    )
    
    return salary_fig, scatter_fig, heatmap_fig, performance_fig, engagement_fig, table

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
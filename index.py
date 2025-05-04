from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from flask import Flask

# Use a small static dataset instead of generating one
df = {
    'Department': ['HR', 'Finance', 'Engineering', 'Marketing', 'Sales'] * 5,
    'Salary': [50000, 60000, 70000, 55000, 65000] * 5,
    'Age': [30, 35, 28, 40, 32] * 5
}

server = Flask(__name__)
app = Dash(__name__, server=server)

# Simplified layout with fewer components
app.layout = html.Div([
    html.H1("HR Analytics Dashboard (Simplified)", style={'textAlign': 'center'}),
    
    # Just one chart
    dcc.Graph(id='salary-chart', figure=px.bar(df, x='Department', y='Salary', title='Salary by Department'))
])

# Export the server for Vercel
application = app.server

if __name__ == '__main__':
    app.run_server(debug=True)

import dash
import dash_core_components as dcc 
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np
from kinetic_models import cj_analytical_edge_concentration
from convert_units import convert_pressure
from calculate_moles import get_rhom

app = dash.Dash()
app.layout = html.Div([
    html.H1(children = 'Edge Pressure (bar) vs Time (hours)',
            style = {
                'textAlign':'center'
            }
    ),
    dcc.Graph(
        id = 'rig_pressure'
    ),
    html.Label('Time (hours):'),
    dcc.Slider(
        id = 'max_time',
        min = 1, 
        max = 10*60*60, 
        value = 5*60*60,
        step = 60*60,
        marks = {
            1 : '0 hours',
            10*60*60 : '10 hours'
        }
    ),
    html.Div(id='time_output'),
    html.Label('Permeability (m2):'),
    dcc.Slider(
        id = 'permeability',
        min = 15, 
        max = 25, 
        value = 22,
        step = 1,
        marks = {
            15 : '5e-15',
            25 : '5e-25'
        }
    ),
    html.Div(id='permeability_output'),
    html.Label('Adsorption uptake:'),
    dcc.Slider(
        id = 'adsorption_uptake',
        min = 0.001, 
        max = 1, 
        value = .5,
        step = 0.1,
        marks = {
            0.001 : '0',
            1 : '1'
        }
    ),
    html.Div(id='adsorptionuptake_output'),
    html.Label('Particle radius (m):'),
    dcc.Slider(
        id = 'particle_radius',
        min = 0.1, 
        max = 5, 
        value = 2,
        step = 0.1,
        marks = {
            0.1 : '0 cm',
            5 : '5 cm'
        }
    ),
    html.Div(id='particleradius_output'),
    html.Label('Initial Pressure (bar):'),
    dcc.Slider(
        id = 'initial_pressure',
        min = 0.001, 
        max = 10, 
        value = 1,
        step = 1,
        marks = {
            0.001 : '0 bar',
            10 : '10 bar'
        }
    ),
    html.Div(id='initialpressure_output'),
    html.Label('Charge Pressure (bar):'),
    dcc.Slider(
        id = 'charge_pressure',
        min = 0.001, 
        max = 10, 
        value = 5,
        step = 1,
        marks = {
            0.001 : '0 bar',
            10 : '10 bar'
        }
    ),
    html.Div(id='chargepressure_output')
])


#-------
@app.callback(
    dash.dependencies.Output('time_output', 'children'),
    [dash.dependencies.Input('max_time', 'value')])
def update_output(value):
    return '{:.2f} hours'.format(round(value/60/60,2))

#-------
@app.callback(
    dash.dependencies.Output('permeability_output', 'children'),
    [dash.dependencies.Input('permeability', 'value')])
def update_output(value):
    return '5e-{:d} m2'.format(round(value,0))

#-------
@app.callback(
    dash.dependencies.Output('initialpressure_output', 'children'),
    [dash.dependencies.Input('initial_pressure', 'value')])
def update_output(value):
    return '{:.2f} bars'.format(round(value,2))

#-------
@app.callback(
    dash.dependencies.Output('chargepressure_output', 'children'),
    [dash.dependencies.Input('charge_pressure', 'value')])
def update_output(value):
    return '{:.2f} bars'.format(round(value,2))

#-------
@app.callback(
    dash.dependencies.Output('adsorptionuptake_output', 'children'),
    [dash.dependencies.Input('adsorption_uptake', 'value')])
def update_output(value):
    return '{:.3f} no units'.format(round(value,2))

#-------
@app.callback(
    dash.dependencies.Output('particleradius_output', 'children'),
    [dash.dependencies.Input('particle_radius', 'value')])
def update_output(value):
    return '{:.2f} cms'.format(round(value,2))

#--------------
@app.callback(
    Output('rig_pressure', 'figure'),
    [Input('max_time', 'value'),
     Input('permeability', 'value'),
     Input('initial_pressure', 'value'),
     Input('charge_pressure', 'value'),
     Input('adsorption_uptake', 'value'),
     Input('particle_radius', 'value')])
def update_graph(max_time, permeability, initial_pressure, charge_pressure, adsorption_uptake, particle_radius):
    
    Vr = 5.91e-5 # m3 
    Vs = 3.44e-5 # m3
    R = 8.314 # m3⋅Pa/(K⋅mol)
    T = 318 # K
    M = 1.51e-2 # kg
    Vgb = 3.71e-4 # m3/kg
    phi = 5.08e-2 # no units
    Vc = 2.88e-5 # m3
    mu = 1.17e-5 #Pa s

    max_t = max_time # seconds
    k = 5/10**(permeability) # m2
    P_i = initial_pressure # bars
    P_c = charge_pressure # bars
    Ka = adsorption_uptake # no units
    R_a = particle_radius/100 # meters
    n = 20 # no units

    rho_i = get_rhom(convert_pressure(P_i,'bar_a','Pa_a'),T,'methane')
    rho_c = get_rhom(convert_pressure(P_c,'bar_a','Pa_a'),T,'methane')
    rho_c0 = (rho_c*Vr + rho_i*Vc)/(Vr+Vc)

    Kc = Vc/(Vgb*M*(phi+(1-phi)*Ka))

    K = (k*rho_c0*R*T)/(mu*(phi+(1-phi)*Ka))

    time = np.linspace(0.1,max_t,100)
    time_hours = time/(60*60)
    edge_concentration = cj_analytical_edge_concentration(time,rho_c0,rho_i,Kc,K,R_a,n)
    edge_pressure = convert_pressure(edge_concentration*R*T,'Pa_a','bar_g')

    return {
        'data' : [
            go.Scatter(
                x = time_hours,
                y = edge_pressure
            )
        ]
    }

if __name__ == '__main__':
    app.run_server(port = 4051)
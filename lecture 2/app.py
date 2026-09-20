import json
from pathlib import Path
import pandas as pd
from dash import Dash, html, dcc, dash_table, Input, Output
import plotly.graph_objects as go

ROOT=Path(__file__).parent; DATA=ROOT/'leases.json'
def data():
    return pd.DataFrame(json.loads(DATA.read_text())) if DATA.exists() else pd.DataFrame()
def money(v): return f'${v:,.0f}'
def percent(v): return 'N/A' if pd.isna(v) else f'{v:.2f}%'
app=Dash(__name__,title='LeBuBu Portfolio OS')
app.layout=html.Div(className='shell',children=[
 html.Div(className='top',children=[html.Div([html.Span('✦ ',className='pink'),html.Span('LeBuBu',className='logo'),html.Span(' / PORTFOLIO OS',className='eyebrow')]),html.Span('LEASE INTELLIGENCE · LIVE',className='status')]),
 html.Div(className='hero',children=[html.Div([html.Div('YOUR REAL ESTATE,',className='kicker'),html.H1('pretty in pink.')]),html.Div('AI-extracted lease intelligence\nfor your next smart move.',className='tagline')]),
 html.Div(id='metrics',className='metrics'),html.Div(className='grid',children=[html.Div(className='panel',children=[html.Div(['PROPERTY MAP',html.Span(' ALL ASSETS',className='pink-label')],className='panel-title'),dcc.Graph(id='map',config={'displayModeBar':False})]),html.Div(className='panel',children=[html.Div(['CASH FLOW',html.Span(' ANNUAL NOI',className='pink-label')],className='panel-title'),dcc.Graph(id='cash',config={'displayModeBar':False})])]),
 html.Div(className='panel table',children=[html.Div('ASSET REGISTER',className='panel-title'),dash_table.DataTable(id='table',page_size=10,sort_action='native')]),dcc.Interval(id='refresh',interval=3000,n_intervals=0)])
@app.callback(Output('metrics','children'),Output('map','figure'),Output('cash','figure'),Output('table','data'),Output('table','columns'),Input('refresh','n_intervals'))
def update(_):
    df=data()
    if df.empty: df=pd.DataFrame([{'property_name':'Add your leases','address':'No JSON records yet','annual_rent':0,'annual_noi':0,'latitude':40.71,'longitude':-74.0,'tenant':'—'}])
    for c in ['annual_rent','annual_noi','latitude','longitude','cap_rate']:
        df[c]=pd.to_numeric(df.get(c,0),errors='coerce').fillna(0)
    # The lease PDFs provide rent, but not property expenses or purchase prices.
    # Use rent as a clearly conservative NOI proxy until those fields are supplied.
    df['noi_display']=df['annual_noi'].where(df['annual_noi'].gt(0),df['annual_rent'])
    cap_values=df.loc[df.cap_rate.gt(0),'cap_rate']
    avg_cap=cap_values.mean() if not cap_values.empty else pd.NA
    city_coords={'New Haven':(41.3083,-72.9279),'Hamden':(41.3959,-72.8968),'Milford':(41.2307,-73.0640),'Branford':(41.2795,-72.8151)}
    for i,row in df.iterrows():
        if not df.at[i,'latitude'] and row.get('city') in city_coords:
            df.at[i,'latitude'],df.at[i,'longitude']=city_coords[row['city']]
    cards=[('ANNUAL NOI*',money(df.noi_display.sum())),('GROSS RENT',money(df.annual_rent.sum())),('AVG CAP RATE',percent(avg_cap)),('ASSETS TRACKED',str(len(df)))]
    fig=go.Figure(go.Scattermap(lat=df.latitude,lon=df.longitude,mode='markers+text',text=df.property_name,textposition='top center',marker={'size':16,'color':'#ff4fa3'})); fig.update_layout(map_style='carto-darkmatter',map_zoom=3,map_center={'lat':39,'lon':-96},height=390,margin=dict(l=0,r=0,t=0,b=0),paper_bgcolor='#151219',font_color='#f8e9f2')
    cash=go.Figure(go.Bar(x=df.property_name,y=df.noi_display,marker_color='#ff4fa3')); cash.update_layout(height=390,margin=dict(l=35,r=15,t=15,b=90),paper_bgcolor='#151219',plot_bgcolor='#151219',font_color='#f8e9f2',yaxis={'gridcolor':'#332630','tickprefix':'$','tickformat':',.0s'},xaxis={'tickangle':-35})
    cols=[c for c in ['property_name','address','tenant','property_type','annual_rent','annual_noi','lease_end'] if c in df]; view=df[cols].fillna('').copy()
    for c in ['annual_rent','annual_noi']:
        if c in view: view[c]=pd.to_numeric(view[c],errors='coerce').fillna(0).map(money)
    return [html.Div([html.Div(k,className='metric-label'),html.Div(v,className='metric-value')],className='metric') for k,v in cards],fig,cash,view.to_dict('records'),[{'name':c.replace('_',' ').upper(),'id':c} for c in cols]
if __name__=='__main__': app.run(debug=True,port=8050)

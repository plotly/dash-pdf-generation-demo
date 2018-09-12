import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import base64
import json
import os
import requests

app = dash.Dash(__name__)
server = app.server

with open('snapshot.pdf', 'rb') as f:
    pdf = f.read()


app.layout = html.Div([
    html.Label('Website URL'),
    dcc.Input(
        id='website',
        value='https://dash.plot.ly'
    ),

    html.Div(html.B('CSS Selector')),
    html.Div('''
        Wait until an element targeted by this selector appears
        before taking a snapshot. These are standard CSS query selectors.
    '''),
    dcc.Input(
        id='wait_selector',
        value='#wait-for-layout'
    ),

    html.Button(id='run', children='Snapshot', n_clicks=0),

    html.Div(id='output'),

])


@app.callback(Output('output', 'children'),
              [Input('run', 'n_clicks')],
              [State('website', 'value'),
               State('wait_selector', 'value')])
def snapshot_page(n_clicks, url, wait_selector):
    if n_clicks == 0:
        return ''
    payload = {
        'url': url,
        'pdf_options': {
            'pageSize': 'Letter',
            'marginsType': 1
        },
        'wait_selector': wait_selector
    }

    res = requests.post(
        '{}/v2/dash-apps/image'.format(
            os.environ.get('PLOTLY_BASE_URL', '# ENTER PLOTLY BASE URL #')
        ),
        headers={
            'plotly-client-platform': 'dash',
            'content-type': 'application/json',
        },
        auth=(
            os.environ.get('PLOTLY_USERNAME', '# ENTER USERNAME #'),
            os.environ.get('PLOTLY_API_KEY', '# ENTER API KEY #'),
        ),
        data=json.dumps(payload)
    )
    if res.status_code == 200:
        return html.A(
            'Download',
            href='data:application/pdf;base64,{}'.format(
                base64.b64encode(res.content).decode('utf-8')
            ),
            download='dash.pdf',
            target='_blank'
        )

    return html.Pre('Status: {}\nResponse: {}'.format(
        res.status_code, res.content
    ))


if __name__ == '__main__':
    app.run_server(debug=True)

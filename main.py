from app import app
from dash import html
import dash_bootstrap_components as dbc
from callbacks.data_handler import *
from callbacks.summary import *
from callbacks.inclusion_plots import *
from callbacks.dpsi_plots import *
from callbacks.supplementary_plots import *
from layouts import header, sidebar,viewer


app.layout = html.Div(
    [
        # Header
        html.Div(
                    [
                        header.header
                    ],
                    id='header',
                    className='sticky-top'
                ),
        # Main
        dbc.Container(
            [
                dbc.Row(
                    [
                        # Sidebar panel
                        dbc.Col(
                            [
                               sidebar.sidebar
                            ],
                            lg=4, md=4, sm=1,
                            id='sidebar',
                        ),
                        # Viewer panel
                        dbc.Col(
                            [
                                viewer.viewer
                            ],
                            lg=7, md=7, sm=1,
                            id='viewer',
                        )
                    ],
                ),
            ],
            fluid=True,
            id='contents'
        )
    ])

if __name__ == '__main__':
    app.run_server(debug=True)

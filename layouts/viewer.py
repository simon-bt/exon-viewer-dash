from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

viewer = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dmc.Group(
                                    [
                                        dmc.Group(
                                            [
                                                # Microexons summary card
                                                dmc.Paper(
                                                    children=[
                                                        html.H3('Microexons'),
                                                        html.Div(
                                                            [
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            [
                                                                                html.H4(id='regulated-mic'),
                                                                                html.P('Regulated')
                                                                            ]
                                                                        ),
                                                                        dbc.Col(
                                                                            [
                                                                                html.H4(id='unregulated-mic'),
                                                                                html.P('Unregulated')
                                                                            ]
                                                                        ),
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                    shadow="md",
                                                    radius="md",
                                                    p="md",
                                                    class_name='card mt-4'
                                                ),
                                                # Long Exon summary card
                                                dmc.Paper(
                                                    children=[
                                                        html.H3('Long Exons'),
                                                        html.Div(
                                                            [
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            [
                                                                                html.H4(id='regulated-long'),
                                                                                html.P('Regulated')
                                                                            ]
                                                                        ),
                                                                        dbc.Col(
                                                                            [
                                                                                html.H4(id='unregulated-long'),
                                                                                html.P('Unregulated')
                                                                            ]
                                                                        ),
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                    shadow="md",
                                                    radius="md",
                                                    p="md",
                                                    class_name='card mt-4'
                                                ),
                                            ],
                                            direction='column',
                                            position='center',
                                            spacing='md'
                                        ),
                                        # Pie chart
                                        dcc.Graph(id='pie-chart',
                                                  style={'width': '350px',
                                                         'height': '350px'}
                                                  )
                                    ],
                                    direction='row',
                                    position='center',
                                    spacing='xl'
                                ),
                            ], lg=12
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dcc.Tabs(
                            [
                                # Inclusion plots tab
                                dcc.Tab(className='sidebar-tab',
                                        label='Inclusion Plots',
                                        children=[
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.H3('Inclusion [PSI] plots'),
                                                                    dmc.Space(h='lg'),
                                                                    dcc.Markdown(
                                                                        """
                                                                        **PSI Scatter** plot compares inclusion profiles between Sample A
                                                                        (starting inclusion) and Sample B for all exons with coverage and other
                                                                        parameteres specified in the _compare_ module of vast-tools. Exons that pass
                                                                        selected \u0394PSI threshold are highlighted. Exons above the diagonal
                                                                        are more included in Sample B; exons below the diagonal are more excluded.
                
                                                                        **PSI Violin** plot displays side-to-side PSI distributions in Sample A
                                                                        (starting inclusion, left side) and Sample B (right side) for regulated
                                                                        exons under selected \u0394PSI threshold.
                                                                        """
                                                                    )
                                                                ]
                                                            ),
                                                        ], lg=5
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dmc.Group(
                                                                [
                                                                    dcc.Dropdown(
                                                                        id='select-psi-plot',
                                                                        options=['PSI Scatter', 'PSI Violin'],
                                                                        value='PSI Scatter',
                                                                        style={'width': '250px'}
                                                                    ),
                                                                    dcc.Graph(id='psi-plot',
                                                                              style={'width': '450px',
                                                                                     'height': '450px'}
                                                                              )
                                                                ],
                                                                direction='column',
                                                                align='center',
                                                                spacing='xs'
                                                            )
                                                        ], lg=6
                                                    )
                                                ]
                                            )
                                        ]
                                        ),
                                # dPSI plots tab
                                dcc.Tab(className='sidebar-tab',
                                        label='\u0394PSI Plots',
                                        children=[
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.H3('Change in inclusion [\u0394PSI] plots'),
                                                                    dmc.Space(h='lg'),
                                                                    dcc.Markdown(
                                                                        """
                                                                        **\u0394PSI Distribution** plot displays distributions for Microexons and
                                                                        Long Exons in your data.
                                                                        
                                                                        **\u0394PSI-Exon Length** plot looks at the relationship between exonic length
                                                                        and change in inclusion. Select maximum exon length to narrow down or broaden
                                                                        the scope.
                                                                        """
                                                                    )
                                                                ]
                                                            ),
                                                        ], lg=5
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dmc.Group(
                                                                [
                                                                    dcc.Dropdown(
                                                                        id='select-dpsi-plot',
                                                                        options=['\u0394PSI Distribution',
                                                                                 '\u0394PSI-Exon Length'],
                                                                        value='\u0394PSI Distribution',
                                                                        style={'width': '250px'}
                                                                    ),
                                                                    dcc.Graph(id='dpsi-plot',
                                                                              style={'width': '450px',
                                                                                     'height': '450px'}
                                                                              )
                                                                ],
                                                                direction='column',
                                                                align='center',
                                                                spacing='xs'
                                                            )
                                                        ], lg=6
                                                    )
                                                ]
                                            )
                                        ]
                                        ),
                                # Supplementary plots tab
                                dcc.Tab(className='sidebar-tab',
                                        label='Supplementary Plots',
                                        children=[
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.H3('Change in inclusion [\u0394PSI] plots'),
                                                                    dmc.Space(h='lg'),
                                                                    dcc.Markdown(
                                                                        """
                                                                         **Impact on ORF** plot provides information about the predicted impact of
                                                                         exons on open reading frame for exons regulated under selected  \u0394PSI
                                                                         threshold.
                                                                        """
                                                                    )
                                                                ]
                                                            ),
                                                        ], lg=5
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dmc.Group(
                                                                [
                                                                    dcc.Dropdown(
                                                                        id='select-supplementary-plot',
                                                                        options=['Impact on ORF',
                                                                                 'Other'],
                                                                        value='Impact on ORF',
                                                                        style={'width': '250px'}
                                                                    ),
                                                                    dcc.Graph(id='supplementary-plot',
                                                                              style={'width': '450px',
                                                                                     'height': '450px'}
                                                                              )
                                                                ],
                                                                direction='column',
                                                                align='center',
                                                                spacing='xs'
                                                            )
                                                        ], lg=6
                                                    )
                                                ]
                                            )
                                        ]
                                        )
                            ],
                        )
                    ], className='mt-4'
                )
            ]
        ),
    ],
    className='mb-4',
)

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

sidebar = html.Div(
    [
        dcc.Tabs(
            [
                # Home Tab
                dcc.Tab(className='sidebar-tab',
                        label='Home',
                        children=[
                            html.Div(
                                [
                                    # Intro
                                    dbc.Row(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Markdown(
                                                        '''

                                                    **ExonViewer** makes it fast and easy to explore alternative splicing profile of exons 
                                                    quantified from RNA-sequencing data using vast-tools software. 

                                                    With a few clicks, generate report-ready figures that summarise your experiment and download
                                                    processed data for your records! 

                                                    **ExonViewer** currently supports four species:

                                                    * Homo sapiens (_VastDB v. hg38_)
                                                    * Mus musculus (_VastDB v. mm10_)
                                                    * Rattus norvegicus (_VastDB v. rn6_)
                                                    * Danio rerio  (_VastDB v. danRer10_)

                                                    Data available from [VastDB, v3](https://vastdb.crg.eu/wiki/Downloads).

                                                        '''
                                                    ),
                                                ],
                                                className='mt-4'
                                            )
                                        ]
                                    ),
                                    # Links
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                dmc.Group(
                                                    [
                                                        # GitHub link - ExonViewer
                                                        html.Div(
                                                            [
                                                                dcc.Link(
                                                                    dmc.Group(
                                                                        [
                                                                            html.I(
                                                                                className='fa fa-brands fa-github icon'),
                                                                            html.Span('ExonViewer',
                                                                                      className='icon-text'),
                                                                        ],
                                                                        align='center',
                                                                        position='center',
                                                                        spacing='xs',
                                                                        direction='column'
                                                                    ),
                                                                    target='_blank',
                                                                    href='https://github.com/simon-bt/exon-viewer-dash',
                                                                    style={'textDecoration': 'none'},
                                                                )
                                                            ],
                                                            className='connect-link'
                                                        ),

                                                        # GitHub link - vast-tools
                                                        html.Div(
                                                            [
                                                                dcc.Link(
                                                                    dmc.Group(
                                                                        [
                                                                            html.I(
                                                                                className='fa fa-brands fa-github icon'),
                                                                            html.Span('vast-tools',
                                                                                      className='icon-text'),
                                                                        ],
                                                                        align='center',
                                                                        position='center',
                                                                        spacing='xs',
                                                                        direction='column'
                                                                    ),
                                                                    target='_blank',
                                                                    href='https://github.com/vastgroup/vast-tools',
                                                                    style={'textDecoration': 'none'},
                                                                ),
                                                            ],
                                                            className='connect-link'
                                                        ),
                                                        # VastDB link
                                                        html.Div(
                                                            [
                                                                dcc.Link(
                                                                    dmc.Group(
                                                                        [
                                                                            html.I(
                                                                                className='fa fa-solid fa-globe icon'),
                                                                            html.Span('VastDB', className='icon-text'),
                                                                        ],
                                                                        align='center',
                                                                        position='center',
                                                                        spacing='xs',
                                                                        direction='column'
                                                                    ),
                                                                    target='_blank',
                                                                    href='https://vastdb.crg.eu/wiki/Main_Page',
                                                                    style={'textDecoration': 'none'},
                                                                )
                                                            ],
                                                            className='connect-link'
                                                        )
                                                    ],
                                                    align='center',
                                                    position='center',
                                                    direction='row',
                                                    spacing='xs'
                                                )
                                            ),
                                        ],
                                        className='mt-4'
                                    )
                                ],
                                className='tab-content'
                            )
                        ]
                        ),
                # How-To Tab
                dcc.Tab(className='sidebar-tab',
                        label='How-To',
                        children=[
                            html.Div(
                                [
                                    dcc.Markdown(
                                        '''
                                        1. Generate input table using _vast-tools compare_ module.

                                        ```
                                        vast-tools compare INCLUSION_LEVELS_FULL-root.tab  
                                        -a [SAMPLE_A] -b [SAMPLE_b] --min_dPSI [value] [...]  
                                        --print_all_events
                                        ```
                                        By default, the command will generate a table ```AllEvents-[parameters].tab```
                                        for all events that pass the coverage filters and thresholds.
                                        
                                        If you prefer, you can also provide your own pre-filtered table. It should 
                                        include the following columns:
                                        
                                        * **EventID** - VastDB exon IDs
                                        * **PSI_A** - inclusion in Sample A
                                        * **PSI_B** - inclusion in Sample B
                                        * **dPSI** - difference between PSI_B and PSI_A
                                        * **TYPE** - you can leave it empty but include it in your table

                                        2. Select exons.
                                        
                                        To work with only exons, you can use _--onlyEX_ of the _combine_ module of 
                                        vast-tools. If you already combined the output for all events and generated a table
                                        from Step 1, you can run the following command to select exons from 
                                        ```AllEvents-[parameters].tab```:
                                        ```
                                        awk 'NR==1; {if ($1 ~ /EX/) print}' AllEvents-[parameters].tab > InputData.tab
                                        ```
                                        3. Select supported species for VastDB data.
                                        4. Specify names for conditions.
                                        5. Upload table.
                                        6. Specify \u0394PSI threshold for regulated events.
                                        7. Explore your data. You may change the default \u0394PSI value and choose your 
                                        favourite colours!
                                        ''')
                                ],
                                className='tab-content mt-4'
                            ),
                        ]
                        ),
                # Data Tab
                dcc.Tab(className='sidebar-tab',
                        label='Data',
                        children=[
                            html.Div(
                                [
                                    # Species selection
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                [
                                                    html.P('Select species')
                                                ]
                                            ),
                                            dbc.Col(
                                                [
                                                    dcc.Dropdown(id='select-species',
                                                                 options=['Homo_sapiens',
                                                                          'Mus_musculus',
                                                                          'Rattus_norvegicus',
                                                                          'Danio_rerio'],
                                                                 value='Homo_sapiens')]
                                            ),
                                        ]
                                    ),
                                    # Rename Sample A
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                [
                                                    html.P('Sample A Name')
                                                ]
                                            ),
                                            dbc.Col(
                                                [
                                                    dbc.Input(id='sample-a',
                                                              value='Control',
                                                              placeholder='Specify column name')
                                                ]
                                            )
                                        ]
                                    ),
                                    # Rename Sample B
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                [
                                                    html.P('Sample B Name')]
                                            ),
                                            dbc.Col(
                                                [
                                                    dbc.Input(id='sample-b',
                                                              value='Experiment',
                                                              placeholder='Specify column name')
                                                ]
                                            )
                                        ]
                                    ),
                                    dmc.Space(h='lg'),
                                    # Buttons
                                    dbc.Row(
                                        [
                                            dmc.Group(
                                                [
                                                    # Upload Table button
                                                    html.Div(
                                                        [
                                                            dcc.Upload(
                                                                id='upload-data',
                                                                className='upload-button',
                                                                children=html.Div('Upload Table',
                                                                                  className='button-text')
                                                            ),
                                                            dcc.Store(id='uploaded-data'),
                                                            html.Div(id='output-data-upload'),

                                                        ]
                                                    ),
                                                    # View Table button
                                                    html.Div(
                                                        [
                                                            dmc.Drawer(children=[
                                                                html.H4('Uploaded Table')
                                                            ],
                                                                id='drawer-table',
                                                                position='bottom',
                                                                padding='md',
                                                                size='85%'),

                                                            dbc.Button(
                                                                [
                                                                    html.Div('View Table',
                                                                             className='button-text')
                                                                ],
                                                                id='drawer-button'
                                                            )
                                                        ]
                                                    ),
                                                ],
                                                direction='row',
                                                position='center',
                                                spacing='sm'
                                            ),
                                        ]
                                    ),
                                    dmc.Space(h='lg'),
                                    # dPSI threshold
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                [
                                                    dmc.Tooltip(
                                                        children=[
                                                            html.Div(
                                                                [
                                                                    dmc.Group(
                                                                        [
                                                                            html.P(
                                                                                '\u0394PSI Threshold'),
                                                                            DashIconify(
                                                                                className='info-icon',
                                                                                icon='akar-icons:info',
                                                                                color='gray',
                                                                                width=15)
                                                                        ],
                                                                        align='center',
                                                                        position='center',
                                                                        spacing='xs',
                                                                    ),
                                                                ]
                                                            )
                                                        ],
                                                        label='\u0394PSI is the difference in inclusion between '
                                                              'two conditions. By default, ExonViewer considers '
                                                              'exons to be regulated with a minimum \u0394PSI \u00B110',
                                                        withArrow=True,
                                                        wrapLines=True,
                                                        width=250,
                                                        arrowSize=3,
                                                        position='top',
                                                        placement='start'
                                                    )
                                                ]
                                            ),
                                            dbc.Col(
                                                [
                                                    dbc.Input(id='dpsi-threshold',
                                                              type='number',
                                                              value=10,
                                                              step=5,
                                                              min=10,
                                                              max=100),
                                                    dcc.Store(id='diff-data')
                                                ]
                                            ),
                                        ]
                                    ),
                                    # Maximum Exon Length
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                [
                                                    html.P('Maximum Exon Length [nt]'),
                                                ]
                                            ),
                                            dbc.Col(
                                                [
                                                    dbc.Input(id='max-length',
                                                              type='number',
                                                              value=100,
                                                              step=25,
                                                              min=50)
                                                ]
                                            ),
                                        ]
                                    ),
                                    # Colour selection
                                    dmc.Space(h='lg'),
                                    dbc.Row(
                                        [
                                            dmc.Group(
                                                [
                                                    html.Div(
                                                        [
                                                            html.P('Microexons:'),
                                                            dmc.ColorPicker(id='color-mic',
                                                                            format='hex',
                                                                            style={'width': '100px'},
                                                                            size='sm',
                                                                            value='#F5AA42')
                                                        ]
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.P('Long Exons:'),
                                                            dmc.ColorPicker(id='color-long',
                                                                            format='hex',
                                                                            style={'width': '100px'},
                                                                            size='sm',
                                                                            value='#35BCDE')
                                                        ]
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.P('Sample A:'),
                                                            dmc.ColorPicker(id='color-sample-a',
                                                                            format='hex',
                                                                            style={'width': '100px'},
                                                                            size='sm',
                                                                            value='#008080')
                                                        ]
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.P('Sample B:'),
                                                            dmc.ColorPicker(id='color-sample-b',
                                                                            format='hex',
                                                                            style={'width': '100px'},
                                                                            size='sm',
                                                                            value='#800020')
                                                        ]
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.P('Regulated:'),
                                                            dmc.ColorPicker(id='color-regulated',
                                                                            format='hex',
                                                                            style={'width': '100px'},
                                                                            size='sm',
                                                                            value='#23AD3C')
                                                        ]
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.P('Unregulated:'),
                                                            dmc.ColorPicker(id='color-unregulated',
                                                                            format='hex',
                                                                            style={'width': '100px'},
                                                                            size='sm',
                                                                            value='#B6B9BF')
                                                        ]
                                                    )
                                                ],
                                                spacing='xl',
                                                position='center',
                                                noWrap=False
                                            ),
                                        ]
                                    ),
                                ],
                                className='tab-content'
                            ),
                        ]
                        ),
            ]
        ),
    ],
)

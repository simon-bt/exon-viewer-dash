from dash import html
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

header = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dmc.Group(
                            [
                                html.H1('ExonViewer',
                                        className='title'
                                        ),
                                html.H3('Visualise alternative splicing profile of exons',
                                        className='subtitle'
                                        )
                            ],
                            noWrap=True,
                            align='center',
                            position='left',
                            spacing='xs',
                        )
                    ]
                )
            ],
            fluid=True)
    ],
    className="header"
)

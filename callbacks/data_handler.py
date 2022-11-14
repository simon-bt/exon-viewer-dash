from app import app
from dash import html, dash_table, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import sqlite3
import pandas
import base64
import io
from datetime import datetime


# Data upload
@app.callback(
    Output('uploaded-data', 'data'),
    Input('upload-data', 'contents'),
    Input('select-species', 'value'),
    Input('sample-a', 'value'),
    Input('sample-b', 'value'),
)
def upload_data(content: str,
                selected_species: str,
                sample_a: str,
                sample_b: str
                ):
    """
    Uploads table and processed dataframe.

    :param content: Uploaded file.
    :param selected_species: Selected VastDB species.
    :param sample_a: Specified new name for PSI_A columns.
    :param sample_b: Specified new name for PSI_B columns.
    :return: Processed and json-ified dataframe.
    """

    if content is None:
        raise PreventUpdate

    else:
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)
        df = pandas. \
            read_csv(io.StringIO(decoded.decode('utf-8')), sep='\t'). \
            drop('TYPE', axis=1). \
            rename(columns={'PSI_A': sample_a, 'PSI_B': sample_b})

        with sqlite3.connect('./data/meta.db') as con:
            result = pandas.read_sql \
                (f'SELECT * FROM meta WHERE Species == \'{selected_species}\'', con=con)
            upload_df = df. \
                merge(result, on='EventID'). \
                drop(['index', 'Species'], axis=1)
            upload_df['ExonType'] = upload_df['Length']. \
                apply(lambda x: 'MIC' if x <= 27 else 'LONG')
            orf_mapping = {
                'NonCoding': 'NonCoding',
                '5/3 UTR': '5/3 UTR',
                'ORF-disruption (exc)': 'ORF-disruption (exc)',
                'Alternative isoform': 'Alternative isoform',
                'ORF-disruption (inc)': 'ORF-disruption (inc)',
                'Alternative isoform (alt. stop)': 'Alternative isoform',
                'CDS (uncertain)': 'CDS (uncertain)',
                'Alternative isoform (alt. ATG)': 'Alternative isoform',
                'NaN': 'NaN'
            }
            upload_df['ImpactOnto'] = upload_df['Impact']. \
                map(orf_mapping)

        return upload_df.to_json(date_format='iso', orient='split')


# Data display
@app.callback(
    Output('drawer-table', 'children'),
    Input('diff-data', 'data'),
    Input('sample-a', 'value'),
    Input('sample-b', 'value'),
    Input('dpsi-threshold', 'value'),
    Input('color-regulated', 'value'),
)
def from_uploaded(data: str,
                  sample_a: str,
                  sample_b: str,
                  dpsi_value: int,
                  color_reg: str,
                  ):
    """
    Displays uploaded table in a drawer and renders a data download button.

    :param data: Processed and json-ified dataframe.
    :param sample_a: Sample A name.
    :param sample_b: Sample B name.
    :param dpsi_value: Minimum +/- dPSI threshold.
    :param color_reg: Colour for regulated exons under a specified dPSI threshold.
    :return: Dataframe.
    """

    if not data:
        return html.Div(
            dmc.Alert('Upload a table and come back!',
                      title='Ooops! Nothing to display.',
                      color='orange',
                      radius='md',
                      variant='outline'),
        )

    else:
        df = pandas.read_json(data, orient='split')
        df[sample_a] = df[sample_a].round(2)
        df[sample_b] = df[sample_b].round(2)
        df['dPSI'] = df['dPSI'].round(2)

        return html.Div(
            [
                dmc.Group(
                    [
                        html.H4('Uploaded Table'),
                        dbc.Button(
                            [
                                html.Div('Download Table',
                                         className='button-text')
                            ],
                            id='download-button'
                        ),
                        dcc.Download(id="download-data"),
                    ],
                    direction='row',
                    spacing='lg'
                ),
                dmc.Space(h='lg'),
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df.columns],
                    sort_action='native',
                    sort_mode='multi',
                    style_cell={
                        'font-family': 'Helvetica',
                        'textAlign': 'center'},
                    style_header={
                        'backgroundColor': 'lightgrey',
                        'fontWeight': 'bold'
                    },
                    style_table={
                        'height': '500px',
                        'overflowY': 'scroll',
                    },

                    style_data_conditional=[
                        {
                            'if': {
                                'filter_query': '{{dPSI}} >= {} || {{dPSI}} <= {}'.format(dpsi_value, -dpsi_value),
                                'column_id': 'dPSI'
                            },
                            'backgroundColor': f'{color_reg}',
                            'color': 'white'
                        }
                    ]

                ),
            ]
        )


# dPSI update
@app.callback(
    Output('diff-data', 'data'),
    Input('uploaded-data', 'data'),
    Input('dpsi-threshold', 'value'),
    prevent_initial_call=True
)
def update_dpsi(data: str,
                dpsi_value: int
                ):
    """
    Updates table with selected dPSI threshold and creates new column - 'Diff'.

    :param data: Uploaded table.
    :param dpsi_value: dPSI threshold.
    :return: Updated table with regulated and unregulated exons under selected dPSI threshold.
    """
    loaded_df = pandas.read_json(data, orient='split')
    loaded_df['Diff'] = loaded_df['dPSI']. \
        apply(lambda x: 'Yes' if abs(x) >= dpsi_value else 'No')

    return loaded_df.to_json(date_format='iso', orient='split')


# Drawer
@app.callback(
    Output(f'drawer-table', 'opened'),
    Input(f'drawer-button', 'n_clicks'),
    State(f'drawer-table', 'opened'),
)
def toggle_drawer(click: bool,
                  opened: bool):
    """
    Toggles the drawer.

    :param click: On click function.
    :param opened: Bool.
    :return: Opens the drawer.
    """
    if click:
        return not opened


# Data download
@app.callback(
    Output('download-data', 'data'),
    Input('diff-data', 'data'),
    Input('dpsi-threshold', 'value'),
    Input('download-button', 'n_clicks')
)
def download_data(data, dpsi_value, n_clicks):
    """
    Saves dataframe to a .tab file.

    :param data: Processed and json-ified dataframe.
    :param dpsi_value: dPSI threshold.
    :param n_clicks: Bool.
    :return: Tab-delimited file.
    """
    if n_clicks:
        timestamp = datetime.today().strftime('%Y%m%d')
        df =  pandas.read_json(data, orient='split')
        return dcc.send_data_frame(df.to_csv,
                                   f'ExonViewer_diff-data_dPSI-{dpsi_value}_{timestamp}.tab',
                                   sep='\t',
                                   index=False)

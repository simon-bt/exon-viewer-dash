from app import app
from dash import Input, Output
import pandas
import plotly.graph_objects as go
from layouts import helpers


@app.callback(
    Output('regulated-mic', 'children'),
    Output('unregulated-mic', 'children'),
    Output('regulated-long', 'children'),
    Output('unregulated-long', 'children'),
    Input('diff-data', 'data')
)
def summarise_data(data: str):
    """
    Extracts counts of regulated and unregulated exons by ExonType.

    :param data: Processed and json-ified dataframe.
    :return: Counts of regulated and unregulated exons for the summary cards.
    """

    def __count_diff(df: pandas.DataFrame):
        count_reg, count_unreg = 0, 0
        for value in df['Diff'].values:
            if value == 'Yes':
                count_reg += 1
            else:
                count_unreg += 1
        return count_reg, count_unreg

    if not data:
        mic_reg, mic_unreg, long_reg, long_unreg = 0, 0, 0, 0

    else:
        loaded_df = pandas.read_json(data, orient='split')
        mic_data = loaded_df.query('ExonType == \'MIC\'')
        long_data = loaded_df.query('ExonType == \'LONG\'')
        mic_reg, mic_unreg = __count_diff(mic_data)
        long_reg, long_unreg = __count_diff(long_data)

    return mic_reg, mic_unreg, long_reg, long_unreg


@app.callback(
    Output('pie-chart', 'figure'),
    Input('diff-data', 'data'),
    Input('color-mic', 'value'),
    Input('color-long', 'value')
)
def plot_pie(data: str,
             color_mic: str,
             color_long: str):
    """
    Plots a pie chart summarising regulated exons by type.

    :param data: Processed and json-ified dataframe.
    :param color_mic: Colour for micorexons.
    :param color_long: Colour for longer exons.
    :return: Pie chart.
    """

    if not data:
        return helpers.PLACEHOLDER

    else:

        df = pandas.read_json(data, orient='split')
        df_truly = df.query('Diff == \'Yes\'')
        counts_diff = dict(df_truly['ExonType']. \
                           value_counts())
        if len(counts_diff) == 0:
            counts_diff.update({'LONG': 0, 'MIC': 0})

        elif not 'LONG' in counts_diff.keys():
            counts_diff.update({'LONG': 0})

        elif not 'MIC' in counts_diff.keys():
            counts_diff.update({'MIC': 0})

        fig_pie = go.Figure(data=[go.Pie(labels=['MIC', 'LONG'],
                                         values=[counts_diff['MIC'],
                                                 counts_diff['LONG']],
                                         )
                                  ]
                            )
        fig_pie.update_traces(
            hoverinfo='label+percent',
            textinfo='value',
            textfont_size=40,
            marker=dict(colors=[color_mic, color_long],
                        line=dict(color='#000000', width=4)))
        fig_pie.update_layout(
            template=helpers.FIG_TEMPLATE,
            width=350,
            height=350,
            legend=dict(font=dict(size=14), x=0.8, y=1, orientation='h', xanchor='auto', yanchor='auto'),
            margin=dict(l=50, r=50, b=10, t=10, pad=10)
        )

        return fig_pie

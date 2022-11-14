from app import app
from dash import Input, Output
import pandas
import numpy
import plotly.express as px
import plotly.graph_objects as go
from layouts import helpers


@app.callback(
    Output('dpsi-plot', 'figure'),
    Input('select-dpsi-plot', 'value'),
    Input('diff-data', 'data'),
    Input('dpsi-threshold', 'value'),
    Input('max-length', 'value'),
    Input('color-mic', 'value'),
    Input('color-long', 'value'),
    Input('color-regulated', 'value'),
    Input('color-unregulated', 'value')
)
def plot_dpsi(dropdown_selection: str,
              data: str,
              dpsi_value: int,
              max_length: int,
              color_mic: str,
              color_long: str,
              color_reg: str,
              color_unreg: str
              ):
    """
    Plots inclusion figures - proportion or scatter.

    :param dropdown_selection: Selected type of plot.
    :param data: Processed and json-ified dataframe.
    :param dpsi_value: Minimum +/- dPSI threshold.
    :param max_length: Maximum exon length.
    :param color_mic: Colour for microexons.
    :param color_long: Colour for long exons.
    :param color_reg: Colour for regulated exons.
    :param color_unreg: Colour for unregulated exons.
    :return:
    """

    if not data:
        return helpers.PLACEHOLDER

    else:
        df = pandas.read_json(data, orient='split')

        if dropdown_selection == '\u0394PSI Distribution':

            __mic_data = df.query('ExonType == \'MIC\'')['dPSI']
            __long_data = df.query('ExonType == \'LONG\'')['dPSI']
            __cumsum_mic = numpy.cumsum(abs(__mic_data))
            __cumsum_long = numpy.cumsum(abs(__long_data))

            fig_cumsum = go.Figure()
            fig_cumsum.add_trace(
                go.Scatter(y=sorted(__mic_data),
                           x=1. * numpy.arange(len(__cumsum_mic)) / (len(__cumsum_mic) - 1),
                           mode='lines',
                           name='MIC',
                           line=dict(color=color_mic, width=5))

            )
            fig_cumsum.add_trace(
                go.Scatter(y=sorted(__long_data),
                           x=1. * numpy.arange(len(__cumsum_long)) / (len(__cumsum_long) - 1),
                           mode='lines',
                           name='LONG',
                           line=dict(color=color_long, width=5))
            )
            fig_cumsum.update_layout(
                template=helpers.FIG_TEMPLATE,
                width=450,
                height=450,
                yaxis=dict(title='Change in inclusion [\u0394PSI]'),
                xaxis=dict(title='Proportion'),
                legend=dict(x=0.5, y=1.15, orientation='h', xanchor='auto', yanchor='auto'),
                margin=dict(pad=0, l=75, r=50, b=100, t=10)
            )
            fig_cumsum.update_xaxes(showgrid=False, ticks='outside', ticklen=5, tickwidth=2, showline=True,
                                    linecolor='black', tickcolor='black', mirror=True, linewidth=2,
                                    zeroline=False)
            fig_cumsum.update_yaxes(showgrid=False, ticks='outside', ticklen=5, tickwidth=2, showline=True,
                                    linecolor='black', tickcolor='black', mirror=True, linewidth=2,
                                    zeroline=False)

            return fig_cumsum

        else:

            fig_length = px.scatter(df, x='Length',
                                    y='dPSI',
                                    color='ExonType',
                                    hover_data=df.columns,
                                    labels={'ExonType': 'Exon Type'},
                                    color_discrete_sequence=[color_long, color_mic])
            fig_length.update_layout(
                template=helpers.FIG_TEMPLATE,
                width=450,
                height=450,
                yaxis=dict(title='Change in inclusion [\u0394PSI]'),
                xaxis=dict(title='Length [nt]'),
                legend=dict(font=dict(size=14), x=0.5, y=1.2, orientation='h', xanchor='auto', yanchor='auto'),
                margin=dict(pad=0, l=75, r=50, b=100, t=10)
            )
            fig_length.add_hline(y=dpsi_value,
                                 line_width=2,
                                 line_dash='dash',
                                 line_color='grey')
            fig_length.add_hline(y=-dpsi_value,
                                 line_width=2,
                                 line_dash='dash',
                                 line_color='grey')
            fig_length.add_hrect(y0=dpsi_value,
                                 y1=-dpsi_value,
                                 line_width=0,
                                 fillcolor=color_unreg,
                                 opacity=0.3)
            fig_length.add_hrect(y0=dpsi_value,
                                 y1=df['dPSI'].max() + 1.5,
                                 line_width=0,
                                 fillcolor=color_reg, opacity=0.15)
            fig_length.add_hrect(y0=-dpsi_value,
                                 y1=df['dPSI'].min() - 1.5,
                                 line_width=0,
                                 fillcolor=color_reg,
                                 opacity=0.15)
            fig_length.update_xaxes(showgrid=False, ticks='outside', ticklen=5, tickwidth=2, showline=True,
                                    linecolor='black', tickcolor='black', mirror=True, linewidth=2,
                                    zeroline=False, range=[0, max_length])
            fig_length.update_yaxes(showgrid=False, ticks='outside', ticklen=5, tickwidth=2, showline=True,
                                    linecolor='black', tickcolor='black', mirror=True, linewidth=2,
                                    zeroline=False, nticks=10)
            return fig_length

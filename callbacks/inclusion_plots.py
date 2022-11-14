from app import app
from dash import Input, Output
import pandas
import plotly.express as px
import plotly.graph_objects as go
from layouts import helpers


@app.callback(
    Output('psi-plot', 'figure'),
    Input('select-psi-plot', 'value'),
    Input('diff-data', 'data'),
    Input('sample-a', 'value'),
    Input('sample-b', 'value'),
    Input('color-sample-a', 'value'),
    Input('color-sample-b', 'value'),
    Input('color-regulated', 'value'),
    Input('color-unregulated', 'value')
)
def plot_psi(dropdown_selection: str,
             data: str,
             sample_a: str,
             sample_b: str,
             color_a: str,
             color_b: str,
             color_reg: str,
             color_unreg: str
             ):
    """
    Plots inclusion figures - scatter or violin.

    :param dropdown_selection: Selected type of plot.
    :param data: Processed and json-ified dataframe.
    :param sample_a: Sample A name.
    :param sample_b: Sample B name.
    :param color_a: Colour for Sample A.
    :param color_b: Colour for Sample B.
    :param color_reg: Colour for regulated exons under a specified dPSI threshold.
    :param color_unreg: Colour for unregulated exons under a specified dPSI threshold.
    :return: Inclusion plot.
    """

    if not data:
        return helpers.PLACEHOLDER

    else:
        df = pandas.read_json(data, orient='split')

        if dropdown_selection == 'PSI Scatter':
            fig_scatter = px.scatter(df,
                                     x=sample_a,
                                     y=sample_b,
                                     color='Diff',
                                     hover_data=df.columns,
                                     color_discrete_sequence=[color_unreg, color_reg],
                                     labels={'Diff': 'Regulated'})
            fig_scatter.update_layout(
                template=helpers.FIG_TEMPLATE,
                width=450,
                height=450,
                xaxis=dict(title=f'{sample_a} PSI [%]'),
                yaxis=dict(title=f'{sample_b} PSI [%]'),
                showlegend=True,
                legend=dict(font=dict(size=14), x=0.5, y=1.15, orientation='h', xanchor='auto', yanchor='auto'),
                margin=dict(pad=0, l=75, r=50, b=75, t=10)
            )
            fig_scatter.update_xaxes(showgrid=False, ticks='outside', ticklen=10, tickwidth=2, showline=True,
                                     linecolor='black', tickcolor='black', mirror=True, linewidth=2,
                                     zeroline=False)
            fig_scatter.update_yaxes(ticks='outside', ticklen=10, tickwidth=2, showline=True,
                                     linecolor='black', tickcolor='black', mirror=True, linewidth=2,
                                     zeroline=False, showgrid=False)
            fig_scatter.update_traces(marker=dict(size=9,
                                                  line=dict(width=2, color=True)),
                                      selector=dict(mode='markers'),
                                      opacity=0.6)
            fig_scatter.add_shape(type='line',
                                  x0=0.5, y0=0, x1=100, y1=100,
                                  line=dict(color='lightgrey', width=2))
            return fig_scatter

        else:
            __data_melt = df. \
                query('Diff == \'Yes\''). \
                melt(id_vars=['EventID', 'ExonType', 'dPSI', 'GeneName', 'GeneID', 'Impact'],
                     value_vars=[sample_a, sample_b],
                     value_name='PSI',
                     var_name='Condition')

            __df_a = __data_melt.query(f'Condition == \'{sample_a}\'')
            __df_b = __data_melt.query(f'Condition == \'{sample_b}\'')

            show_legend = [True, False, False, False]
            pointpos_a = [-0.5, -0.5,
                          0, 0]
            pointpos_b = [0.5, 0.5,
                          1, 1]

            fig_violin = go.Figure()
            for i in range(0, 2):
                fig_violin.add_trace(
                    go.Violin(x=__df_a['ExonType'][(__df_a['ExonType'] == pandas.unique(__df_a['ExonType'])[i])],
                              y=__df_a['PSI'][(__df_a['ExonType'] == pandas.unique(__df_a['ExonType'])[i])],
                              legendgroup=sample_a,
                              scalegroup=sample_a,
                              name=sample_a,
                              side='negative',
                              pointpos=pointpos_a[i],
                              line_color=color_a,
                              showlegend=show_legend[i])
                )
                fig_violin.add_trace(
                    go.Violin(x=__df_b['ExonType'][(__df_b['ExonType'] == pandas.unique(__df_b['ExonType'])[i])],
                              y=__df_b['PSI'][(__df_b['ExonType'] == pandas.unique(__df_b['ExonType'])[i])],
                              legendgroup=sample_b,
                              scalegroup=sample_b,
                              name=sample_b,
                              side='positive',
                              pointpos=pointpos_b[i],
                              line_color=color_b,
                              showlegend=show_legend[i])
                )

            fig_violin.update_layout(
                template=helpers.FIG_TEMPLATE,
                width=450,
                height=450,
                violingap=0,
                violingroupgap=0.3,
                violinmode='overlay',
                yaxis=dict(title='PSI [%]'),
                xaxis=dict(title='Exon Type'),
                legend=dict(font=dict(size=14), x=0.5, y=1.15, orientation='h', xanchor='auto', yanchor='auto'),
                margin=dict(pad=0, l=75, r=50, b=75, t=10)
            )
            fig_violin.update_traces(meanline_visible=True,
                                     points='all',
                                     jitter=0.1,
                                     scalemode='count')
            fig_violin.update_xaxes(showgrid=False, ticks='outside', ticklen=5, tickwidth=2, showline=True,
                                    linecolor='black', tickcolor='black', mirror=True, linewidth=2,
                                    zeroline=False, range=[-0.5, 1.5])
            fig_violin.update_yaxes(showgrid=False, ticks='outside', ticklen=5, tickwidth=2, showline=True,
                                    linecolor='black', tickcolor='black', mirror=True, linewidth=2,
                                    zeroline=False, nticks=10, range=[-15, 115])

            return fig_violin

from app import app
from dash import Input, Output
import pandas
import plotly.express as px
from layouts import helpers


@app.callback(
    Output('supplementary-plot', 'figure'),
    Input('select-supplementary-plot', 'value'),
    Input('diff-data', 'data'),
)
def plot_supplementary(dropdown_selection: str,
                       data:str
                       ):
    """
    Plots supplementary figures - impact on ORF.

    :param dropdown_selection: Selected type of plot.
    :param data: Processed and json-ified dataframe.
    :return: Pie chart.
    """

    if not data:
        return helpers.PLACEHOLDER

    else:
        df = pandas.read_json(data, orient='split')

        if dropdown_selection == 'Impact on ORF':
            df_truly = df[~df['Impact'].isna()]. \
                query('Diff == \'Yes\' & ImpactOnto != \'NaN\'')
            __exon_info = dict(df_truly['ExonType'].value_counts())
            __onto_counts = pandas.DataFrame(df_truly. \
                                             groupby('ExonType')['ImpactOnto']. \
                                             value_counts()). \
                rename(columns={'ImpactOnto': 'Count'}). \
                reset_index()
            __onto_counts['N_Exons'] = __onto_counts['ExonType'].map(__exon_info)
            __onto_counts['Pct'] = __onto_counts. \
                apply(lambda x: round(x['Count'] * 100 / x['N_Exons'], 2), axis=1)

            fig_orf = px.bar(__onto_counts, x='ExonType', y='Pct', color='ImpactOnto',
                             category_orders={'ExonType': ['LONG', 'MIC']},
                             labels={'ImpactOnto': 'Impact'}
                             )

            fig_orf.update_layout(
                template=helpers.FIG_TEMPLATE,
                xaxis=dict(title='Exon Type'),
                yaxis=dict(title='% of Events'),
                width=450,
                height=450,
                legend=dict(font=dict(size=14), x=2, y=1, orientation='v', xanchor='auto', yanchor='auto'),
                margin=dict(pad=0, l=75, r=50, b=100, t=25)
            )
            fig_orf.update_xaxes(showgrid=False, ticks='outside', ticklen=5, tickwidth=2, showline=True,
                                 linecolor='black', tickcolor='black', mirror=True, linewidth=2,
                                 zeroline=False)
            fig_orf.update_yaxes(showgrid=False, ticks='outside', ticklen=5, tickwidth=2, showline=True,
                                 linecolor='black', tickcolor='black', mirror=True, linewidth=2,
                                 zeroline=False)

            return fig_orf
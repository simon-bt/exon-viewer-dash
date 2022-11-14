import plotly.graph_objects as go

# Figure template
FIG_TEMPLATE = dict(
    layout=go.Layout(
        autosize=False,
        title_font=dict(family='Helvetica',
                        size=18),
        font=dict(family='Helvetica',
                  size=18,
                  color='#1e2125'),
    )
)

# Figure placeholder
PLACEHOLDER = go.Figure()
PLACEHOLDER.update_layout(
    xaxis={'visible': False},
    yaxis={'visible': False},
    annotations=[
        {
            'text': 'Waiting for table upload!',
            'xref': 'paper',
            'yref': 'paper',
            'showarrow': False,
            'font': {'size': 20}
        }
    ]
)

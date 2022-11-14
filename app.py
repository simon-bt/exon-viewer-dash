import dash
import dash_bootstrap_components as dbc

external_styles = ['https://kit.fontawesome.com/4c169f4e7c.js', 'assets/css/main.css']
app = dash.Dash(__name__,
                external_stylesheets=[
                    dbc.themes.BOOTSTRAP,
                    external_styles,
                    dbc.icons.FONT_AWESOME
                ],
                meta_tags=[
                    {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}
                ],
                title='ExonViewer'
                )

app.config.suppress_callback_exceptions = True

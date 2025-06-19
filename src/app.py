import os
from dash import Dash
from src.ui.layout import create_layout
from src.core.callbacks import register_callbacks


assets_path = os.path.join(os.path.dirname(__file__), "ui", "assets")
app = Dash(__name__, assets_folder=assets_path)
app.layout = create_layout()
register_callbacks(app)


def run():
    app.run(debug=True)


if __name__ == "__main__":
    run()

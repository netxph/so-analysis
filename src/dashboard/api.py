from flask import Blueprint
from wrangles import Plots
import json, plotly

api_bp = Blueprint('api_pb', __name__)

@api_bp.route("/graph/satisfy")
def graph_satisfy():
    plots = Plots("data/so_data.csv")

    return json.dumps(plots.get_satisfy(), cls=plotly.utils.PlotlyJSONEncoder)

@api_bp.route("/graph/factors")
def graph_factors():
    plots = Plots("data/so_data.csv")

    return json.dumps(plots.get_factors(), cls=plotly.utils.PlotlyJSONEncoder)
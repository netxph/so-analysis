import pandas as pd
import numpy as np
import plotly.graph_objects as go

from wrangles.utils import *

class Plots:

    def __init__(self, file):
        self.data = pd.read_csv(file)

    def get_satisfy(self):
        df = self.data[["job_seek", "job_sat"]]
        job_sat = count_percentage("job_sat", "job_seek", df)

        fig = go.Figure()

        sat = job_sat.job_sat.unique().tolist()

        for job_seek in job_sat.job_seek.unique():
            fig.add_trace(go.Bar(
                x = sat,
                y = job_sat[job_sat.job_seek == job_seek].percent.tolist(),
                name = job_seek))
        
        fig.update_layout(
            title = "Percentage of job satisfaction by job seek",
            xaxis = dict(
                title='Job satisfaction'),
            yaxis=dict(
                title='Percentage'))

        return fig

    def get_factors(self):

        factors = self.data[["employment", "job_factors"]].dropna()
        factors["job_factors"] = factors.job_factors.str.split(";")

        factors_exp = factors.explode("job_factors")

        x,y = 'employment', 'job_factors'

        factors_g = count_percentage(x, y, factors_exp)

        emp = factors_g.employment.unique().tolist()

        fig = go.Figure()

        for job_factors in factors_g.job_factors.unique():
            fig.add_trace(go.Bar(
            x = emp,
            y = factors_g[factors_g.job_factors == job_factors].percent.tolist(),
            name = job_factors))

        fig.update_layout(
            title = "Job Factors per Employoment",
            xaxis = dict(
                title="Employment"),
            yaxis=dict(
                title='Percentage'))

        return fig
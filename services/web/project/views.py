import json
from datetime import datetime
import plotly
import plotly.graph_objs as go
from flask_table import Col, Table

from .models import Patient, Exam, Note

def plot_labour(user):

    user_time = datetime.fromtimestamp(user.in_labour)
    exams = Exam.query.filter_by(name=user.name).all()
    notes = Note.query.filter_by(name=user.name).all()

    exam_data = {
        "time": [],
        "dilation": [],
        "bishops": [],
    }
    for ex in exams:
        exam_data["time"].append(ex.timestamp)
        exam_data["dilation"].append(ex.dilation)
        exam_data["bishops"].append(ex.dilation + ex.effacement + ex.station)

    ref_data = {
        "time": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "dilation": [0, 0, 2, 3, 4, 5, 5, 7, 8, 9, 10],
    }

    t_min = min(ref_data["time"])
    t_max = max(ref_data["time"])
    y_max = max(ref_data["dilation"])

    note_data = {
        "time": [],
        "note": [],
    }

    for note in notes:
        note_data["time"].append(note.timestamp)
        note_data["note"].append(note.note)

    N =  len(note_data["time"])
    line_data = [
        # go.Scatter(mode="lines", x=ref_data["time"], y=ref_data["dilation"],),
        go.Scatter(mode="markers+lines", x=ref_data["time"], y=ref_data["dilation"], name="Dilation"),
        go.Scatter(mode="lines", x=[user_time, user_time], y=[0, y_max], name="Entered Labor"),
        go.Scatter(mode="markers", x=note_data["time"], y=[10]*N,text=note_data["note"], name="Patient notes"),
        # go.Scatter(mode="lines", x=ref_data["time"], y=df_exam.bishops,)

    ]

    layout = go.Layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")

    ln_fig = go.Figure(data=line_data, layout=layout)

    ln_fig.update_xaxes(showgrid=False, title_text="time")
    ln_fig.update_yaxes(showgrid=True, title_text="dilation")

    ln_json = json.dumps(ln_fig, cls=plotly.utils.PlotlyJSONEncoder)

    return ln_json

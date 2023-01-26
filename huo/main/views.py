import os
import pandas as pd
import plotly.express as px
from plotly.offline import plot
from django.conf import settings
import plotly.graph_objects as go
from django.shortcuts import render


def index(request):
    file_path = os.path.join(settings.FILES_DIR, 'test.csv')
    df = pd.read_csv(file_path)
    fig = px.line(df.tail(240), x="dt", y="rub", title='Huobi Money')
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return render(request, "index.html", context={'plot_div': plot_div})

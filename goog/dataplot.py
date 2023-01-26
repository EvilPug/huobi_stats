import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('test.csv')

fig = px.line(df, x="dt", y="rub", title='Huobi Money')
fig.show()

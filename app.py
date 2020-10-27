import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

pio.templates.default = "plotly_white"

# Load data
text_df = pd.read_csv('text_df.csv')
# Most used stickers
stickers_df = text_df[text_df['media_type']=='sticker'].groupby(['sticker_url','from']).agg({'from_id':'count'}).reset_index()
stickers_df = stickers_df.pivot(index='sticker_url',columns='from',values='from_id').reset_index()
stickers_df['total'] = stickers_df['🐑💛🌙'] + stickers_df['🐥💛🌻']
stickers_df = stickers_df.sort_values(['total'], ascending=False).head(10)
stickers_df['🐑💛🌙'] = stickers_df['🐑💛🌙'].astype(int)
stickers_df['🐥💛🌻'] = stickers_df['🐥💛🌻'].astype(int)
stickers_df['total'] = stickers_df['total'].astype(int)

stickers_df['sticker_html'] = '<img src="'+ stickers_df['sticker_url'] + '" width="30" height="30"/>'

pd.set_option('display.max_colwidth', None)

# HTML(stickers_df[['sticker_html','🐑💛🌙','🐥💛🌻','total']].to_html(escape=False))
st.write(stickers_df[['sticker_html','🐑💛🌙','🐥💛🌻','total']].to_html(escape=False), unsafe_allow_html=True)

# Message count and message length

overview_df = text_df.groupby('from').agg({'text2':'count','word_count':'mean','hour':'median'}).reset_index()
overview_df.rename(columns={'text2':'Message_count',
                            'word_count':'Average_message_length',
                            'hour':'Median_hour'},
                   inplace=True)
st.write(overview_df.style.format({'Message_count': '{:.0f}', 'Average_message_length': '{:.2f}', 'hour': '{:.0f}'}))

fig = px.bar(overview_df, x='Message_count', y='from',
             color='from', orientation='h',
             color_discrete_map={
                "🐑💛🌙": 'rgb(246, 207, 113)',
                "🐥💛🌻": "rgb(102, 197, 204)"},
             text='Message_count',
             color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig)
# overview_df.style.set_precision(2)
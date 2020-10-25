import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from IPython.display import Image, HTML

path = 'D:/OneDrive/Personal/OneDrive/Projects/telegram_text/'
text_df = pd.read_csv('text_df.csv')
text_df['sticker_img'] = np.where(text_df['media_type']=='sticker', 
                                   path + 'ChatExport/' + text_df['file'],
                                   np.nan)

df = text_df[text_df['media_type']=='sticker'].groupby(['sticker_img','from']).agg({'from_id':'count'}).reset_index()
df = df.pivot(index='sticker_img',columns='from',values='from_id').reset_index()
df['total'] = df['🐑💛🌙'] + df['🐥💛🌻']
df = df.sort_values(['total'], ascending=False).head(10)

df['sticker_img'] = '<img src="'+ df['sticker_img'] + '" width="30" height="30"/>'
# def path_to_image_html(path):
#     return '<img src="'+ path + '" width="30" height="30"/>'

# pd.set_option('display.max_colwidth', None)

st.write(df.to_html(escape=False), unsafe_allow_html=True)
# HTML(df.to_html(escape=False ,formatters=dict(sticker_img=path_to_image_html)))
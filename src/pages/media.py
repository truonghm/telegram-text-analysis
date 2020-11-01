import streamlit as st
import pandas as pd
import altair as alt

from src.utils import get_data

def write(df):
   """Used to write the page in the app.py file"""
   with st.spinner("Loading Media Page---"):
      st.write(f"# Stickers and other Media usage")

   stickers_df = get_data(filepath=df,columns=None, head=None)
   stickers_df = stickers_df.merge(stickers_df[['sticker_url']].drop_duplicates().reset_index(), on='sticker_url')
   stickers_df.rename(columns={'from':'sender','from_id':'total_count'}, inplace=True)
   stickers_df.sort_values('total_count',ascending=False,inplace=True)

   grouped_sticker_df = stickers_df.pivot(index='sticker_url',columns='sender',values='total_count').reset_index()
   grouped_sticker_df['total'] = grouped_sticker_df['🐑💛🌙'] + grouped_sticker_df['🐥💛🌻']
   grouped_sticker_df = grouped_sticker_df.sort_values(['total'], ascending=False).head(10)
   grouped_sticker_df['🐑💛🌙'] = grouped_sticker_df['🐑💛🌙'].astype(int)
   grouped_sticker_df['🐥💛🌻'] = grouped_sticker_df['🐥💛🌻'].astype(int)
   grouped_sticker_df['total'] = grouped_sticker_df['total'].astype(int)

   grouped_sticker_df['sticker_html'] = '<img src="'+ grouped_sticker_df['sticker_url'] + '" width="30" height="30"/>'

   st.markdown("## Most used stickers - Table")
   st.write(grouped_sticker_df[['sticker_html','🐑💛🌙','🐥💛🌻','total']].to_html(escape=False), unsafe_allow_html=True)

   st.markdown("## Most used stickers - Chart")
   input_dropdown = alt.binding_select(options=['🐑💛🌙','🐥💛🌻'])
   selection = alt.selection_single(fields=['sender'], bind=input_dropdown, name='From')
   color = alt.condition(selection,
                     alt.Color('sender:N', legend=None),
                     alt.value('lightgray'))

   img = alt.Chart(stickers_df).transform_filter(
      selection
   ).mark_image().encode(
      y=alt.Y('index:N', axis=alt.Axis(domainOpacity=0,ticks=False)),
      url="sticker_url:N"
   ).transform_window(
      rank='rank(total_count)',
      sort=[alt.SortField('total_count', order='descending')]
   ).transform_filter(
      (alt.datum.rank < 10)
   ).properties(height=300)

   chart = alt.Chart(stickers_df).add_selection(
      selection
   ).transform_filter(
      selection
   ).mark_bar().encode(
      y=alt.Y('index:N', axis=None),
      x=alt.X('total_count:Q'),
      text='total_count:Q'
   ).transform_window(
      rank='rank(total_count)',
      sort=[alt.SortField('total_count', order='descending')]
   ).transform_filter(
      (alt.datum.rank < 10)
   ).properties(height=300)


   c= alt.concat(
      img, chart
   ).configure_concat(
      spacing=0
   )

   st.altair_chart(c, use_container_width=True)
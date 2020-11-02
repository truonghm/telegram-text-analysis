
import altair as alt
from altair.vegalite.v4.api import selection
import streamlit as st
import numpy as np

from src.utils import *

def write(state):
    """Used to write the page in the app.py file"""
    local_css("style.css")
    with st.spinner("Loading Overview Page---"):
        st.write(f"# Overview")
    
    col1, col2 = st.beta_columns(2)

    with col1:
        # part 1
        url = state['text_url']
        df = state['text_df']
        date_started = min(df['datetime'])
        m1 = f"<div><span class='bold'>Date Started: <span class='highlight blue'>{date_started}</span></span></div>"
        total_messages = len(df['datetime'])
        m2 = f"<div><span class='bold'>Total Messages: <span class='highlight blue'>{total_messages}</span></span></div>"
        st.text("")
        st.markdown(m1, unsafe_allow_html=True)
        st.text("")
        st.markdown(m2, unsafe_allow_html=True)
        st.write("---")

        # part 2

    with col2:
        year_list = df['year'].unique().tolist()
        year_list.insert(0, "All")
        year_dropdown = alt.binding_select(options=year_list)
        year_selection = alt.selection_single(fields=['year'], bind=year_dropdown, name='Pick_a_')

        base = alt.Chart(url).add_selection(
            year_selection
            ).transform_filter(
            year_selection
            )

        upper=base.mark_bar().encode(
            y='from:N',
            x='count():Q',
            tooltip='count():Q',
            color=alt.Color('from:N',legend=None)
        ).properties(
            width=300 
        )

        lower=base.mark_bar().encode(
            y='from:N',
            x='average(word_count):Q',
            tooltip='average(word_count):Q',
            color=alt.Color('from:N',legend=None)
        ).properties(
            width=300 
        )

        c = alt.vconcat(upper, lower)
        c
        st.write(c)
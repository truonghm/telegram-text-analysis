
import altair as alt
import streamlit as st

from src.utils import *

def write(state):
    """Used to write the page in the app.py file"""
    local_css("style.css")
    with st.spinner("Loading Overview Page---"):
        st.write(f"# Overview")
    
    # part 1
    url = state['text_url']
    date_started = min(state['text_df']['datetime'])
    m1 = f"<div><span class='bold'>Date Started: <span class='highlight blue'>{date_started}</span></span></div>"
    total_messages = len(state['text_df']['datetime'])
    m2 = f"<div><span class='bold'>Total Messages: <span class='highlight blue'>{total_messages}</span></span></div>"
    st.markdown(m1, unsafe_allow_html=True)
    st.text("")
    st.markdown(m2, unsafe_allow_html=True)
    st.write("---")

    # part 2
    selection_year = st.selectbox(
    "Year:",
    ("2018", "2019", "2020")
    )

    upper=alt.Chart(url).transform_filter(
        alt.datum.year==selection_year
    ).mark_bar().encode(
        y='from:N',
        x='count():Q',
        color='from:N'
    )

    lower=alt.Chart(url).transform_filter(
        alt.datum.year==selection_year
    ).mark_bar().encode(
        y='from:N',
        x='average(word_count):Q',
        color='from:N'
    )

    c = alt.vconcat(upper, lower)
    c
    st.write(c)
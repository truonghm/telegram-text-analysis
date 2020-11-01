
import altair as alt
import streamlit as st

from src.utils import get_data

def write(df):
    """Used to write the page in the app.py file"""
    with st.spinner("Loading Overview Page---"):
        st.write(f"# Overview")

    upper=alt.Chart(df).mark_bar().encode(
        y='from:N',
        x='count():Q',
        color='from:N'
    )

    lower=alt.Chart(df).mark_bar().encode(
        y='from:N',
        x='average(word_count):Q',
        color='from:N'
    )

    c = alt.vconcat(upper, lower)
    c
    st.write(c)
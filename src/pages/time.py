import altair as alt
import streamlit as st

from src.utils import get_data

@st.cache
def write(df):
    """Used to write the page in the app.py file"""
    with st.spinner("Loading Texting through time Page---"):
        st.write(f"# Texting through time")
    
    # message overtime
    c1 = alt.Chart(df).mark_line().encode(
        x='date:T',
        y='count():Q',
        color='from:N',
        tooltip=['from:N', 'date:T','count():Q']
    ).properties(
        width=550,
        height=200
    ).interactive()

    c2 = alt.Chart(df).mark_bar().encode(
        x='month(datetime):N',
        y=alt.Y('count():Q', stack='normalize'),
        color='daypart:N',
    ).facet(column='year(datetime):N')

    st.altair_chart(c1)
    st.altair_chart(c2)
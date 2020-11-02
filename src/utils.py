import json
import pandas as pd
import numpy as np
import datetime as dt
import os
import streamlit as st

@st.cache
def get_data(filepath, columns, head):
    """get data from csv file"""
    if columns is None:
        df = pd.read_csv(filepath)
    else:
        df = pd.read_csv(filepath, usecols=columns)
    if head is None:
        "do nothing"
    else:
        df = df.head(head)
    return df


def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

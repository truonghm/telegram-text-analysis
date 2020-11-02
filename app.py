"""Main module for the streamlit app
Taking inspiration from:
https://discuss.streamlit.io/t/multi-page-app-with-session-state/3074
in order to preserve dataframes across multipage app"""

from streamlit.hashing import _CodeHasher
import streamlit as st
import pandas as pd

import src.pages.media
import src.pages.overview
import src.pages.time
from src.utils import *

dir_root = 'https://media.githubusercontent.com/media/truonghm/telegram-text-analysis/master/'
# dir_root = 'D:/OneDrive/Personal/OneDrive/Projects/telegram_text/'

try:
    # Before Streamlit 0.65
    from streamlit.ReportThread import get_report_ctx
    from streamlit.server.Server import Server
except ModuleNotFoundError:
    # After Streamlit 0.65
    from streamlit.report_thread import get_report_ctx
    from streamlit.server.server import Server

def main():
    """Main function of the app"""
    state = _get_state()
    PAGES = {
    "Data state": page_data_state,
    "Overview": page_overview,
    "Texting through time":page_time,
    "Media": page_media
    }

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        # page is a module with a 'def write()' function
        # Display the selected page with the session state
        page(state)

    # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
    state.sync()

def page_data_state(state):
    st.title(":wrench: Data State & Settings")
    display_state_values(state)

    st.write("---")

    import_state_values(state)

def page_overview(state):
    return src.pages.overview.write(state)

def page_time(state):
    return src.pages.time.write(state)

def page_media(state):
    return src.pages.media.write(state)

def import_state_values(state):
    if st.button("Get dataframe"):
        state['text_url'] = dir_root + 'data/text_df.csv'
        state['stickers_df'] = dir_root + 'data/stickers_df.csv'
        state['text_df'] = get_data(filepath=dir_root + 'data/text_df.csv', columns=None, head=None)

def display_state_values(state):
    st.write('**Sticker dataframe URL**:', state['stickers_df'])
    st.write('**Text dataframe URL**:', state['text_url'])
    if isinstance(state['text_df'], pd.DataFrame):
        st.write(state['text_df'].head(5))
    elif state['text_df'] is not None:
        st.write('**Text dataframe**: ', state['text_df'])
    else:
        st.write('**Text dataframe**: ', None)

    if st.button("Clear state"):
        state.clear()


class _SessionState:

    def __init__(self, session, hash_funcs):
        """Initialize SessionState instance."""
        self.__dict__["_state"] = {
            "data": {},
            "hash": None,
            "hasher": _CodeHasher(hash_funcs),
            "is_rerun": False,
            "session": session,
        }

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state["data"]:
                self._state["data"][item] = value

    def __getitem__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)
        
    def __getattr__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __setitem__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def __setattr__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value
    
    def clear(self):
        """Clear session state and request a rerun."""
        self._state["data"].clear()
        self._state["session"].request_rerun()
    
    def sync(self):
        """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing state value at each run.
        #
        # Example: state.value += 1
        if self._state["is_rerun"]:
            self._state["is_rerun"] = False
        
        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(self._state["data"], None):
                self._state["is_rerun"] = True
                self._state["session"].request_rerun()

        self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)


def _get_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    
    return session_info.session


def _get_state(hash_funcs=None):
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = _SessionState(session, hash_funcs)

    return session._custom_session_state


if __name__ == "__main__":
    main()
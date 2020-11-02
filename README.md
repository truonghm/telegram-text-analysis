# Telegram Text Message Analysis

Analyze messages sent through Telegram using Python & deployed to web app with Streamlit/Streamlit Sharing.

[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/truonghm/)

## Dependencies :construction:
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Streamlit 0.68](https://img.shields.io/badge/streamlit-0.69-red.svg)](https://discuss.streamlit.io/t/version-0-69-0-the-1-year-anniversary-release/6116)
[![Altair 4.10](https://img.shields.io/badge/altair-4.10-green.svg)](https://altair-viz.github.io/)

## References :flashlight:
- [Text mining with R](https://www.tidytextmining.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- The [Awesome Streamlit](https://awesome-streamlit.org/) Project ([Github repo](https://github.com/MarcSkovMadsen/awesome-streamlit))
- [Discussion thread](https://discuss.streamlit.io/t/multi-page-app-with-session-state/3074) about session state for multipage app

## Note/Issues :sos:
- Streamlit is still in its beta state and thus lacks some useful functionalities, notably session-state and multi-page app. My implementations are based on community ideas, however they are hacky and should be changed when future releases of Streamlit implement better solutions.  
- Altair charts work by sending the entire dataset to browser and processing it in the frontend; for this reason it does not work well for larger datasets. For this reason, loading large dataframes directly into Altair would slow down/crash the browser, as it triggers MaxRowError.

## To-do :runner:
- [X] Finish text mining portion of the project
- [X] Finish visualization 
- [X] Enable csv file uploading
- [X] Create tool to convert from json format to csv format
- [X] Expand to other messaging platforms

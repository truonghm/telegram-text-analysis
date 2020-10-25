call C:\Users\truonghm\anaconda3\Scripts\activate.bat
call C:\Users\truonghm\anaconda3\Scripts\python pywin32_postinstall.py -install
call conda create --name text-analysis python=3.8
call pip install numpy pandas datetime autopep8 flake8 matplotlib plotly seaborn streamlit

D:
SET mypath=%~dp0
cd mypath
pause
@echo off

rem Create python environment
python -m venv venv
call venv\Scripts\activate

rem Install the dependencies
pip install -r requirements.txt

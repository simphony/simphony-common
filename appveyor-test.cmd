"%sdkverpath%" -q -version:"%sdkver%"
call setenv /x64

flake8 .
if %errorlevel% neq 0 exit /b %errorlevel%
coverage run -m unittest discover -v -p test*
if %errorlevel% neq 0 exit /b %errorlevel%
python setup.py build_sphinx
if %errorlevel% neq 0 exit /b %errorlevel%
coverage report

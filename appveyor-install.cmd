"%sdkverpath%" -q -version:"%sdkver%"
call setenv /x64

rem install python packages
pip install numpy
rem builds currently fail
rem pip install numexpr
rem pip install tables >= 3.1.1
pip install -r dev_requirements.txt


rem install simphony-common 
python setup.py develop
if %errorlevel% neq 0 exit /b %errorlevel%
cd examples/plugin
python setup.py develop
if %errorlevel% neq 0 exit /b %errorlevel%
cd ..

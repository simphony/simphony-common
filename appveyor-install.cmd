"%sdkverpath%" -q -version:"%sdkver%"
call setenv /x64

rem install python packages
pip install numpy
rem builds currently fail
rem pip install numexpr
rem pip install tables >= 3.1.1
pip install enum34>=1.0.4
pip install stevedore>=1.2.0
pip install click>=3.3
pip install pyyaml>=3.11
pip install sphinx>1.3
pip install sphinxcontrib-napoleon>=0.2.10
pip install tabulate>=0.7.4
pip install mock==1.0.1
pip install coverage
pip install flake8

rem install simphony-common
python setup.py develop
if %errorlevel% neq 0 exit /b %errorlevel%
cd examples/plugin
python setup.py develop
if %errorlevel% neq 0 exit /b %errorlevel%
cd ..

python -m venv venv

venv\Scripts\python -m pip install ../../pyscp
venv\Scripts\python -m pip install cx_Freeze ../.
venv\Scripts\python scripts\build.py build

makensis skippy.nsi

RD /S /Q "venv"
RD /S /Q "build"

ECHO Success compiled!

PAUSE
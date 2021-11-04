python -m venv venv

venv\Scripts\python -m pip install cx_Freeze ../.
venv\Scripts\python scripts\build.py build

makensis skippy.nsi

rm -rf "venv"
rm -rf "build"
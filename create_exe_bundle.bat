REM change the path below to the your correct path
pyinstaller -F --onefile --add-data C:\Python311\tcl\tix8.4.3;tcl\tix8.4.3 macro_jx.py -y 

REM NOW mo to the dest folder
cp -R assets dist\
mkdir dist\macro

ECHO Running macro_jx.exe
start dist\macro_jx.exe
echo "DONE"


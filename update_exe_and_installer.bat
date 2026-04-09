pyinstaller .\SparxFast.spec
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
mv Output\SparxFastSetup.exe .\apps\SparxFastSetup.exe
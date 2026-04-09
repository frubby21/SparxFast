[Setup]
AppName=SparxFast
AppVersion=1.0.2
DefaultDirName={commonpf}\SparxFast
DefaultGroupName=SparxFast
PrivilegesRequired=admin
OutputDir=.\Output
OutputBaseFilename=SparxFastSetup
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\SparxFast.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\SparxFast"; Filename: "{app}\SparxFast.exe"
Name: "{commondesktop}\SparxFast"; Filename: "{app}\SparxFast.exe"

[Run]
Filename: "{app}\SparxFast.exe"; Description: "Launch SparxFast"; Flags: nowait postinstall skipifsilent
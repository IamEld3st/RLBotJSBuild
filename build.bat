@echo off

powershell -Command "Invoke-WebRequest https://nodejs.org/dist/index.tab -OutFile index.txt"

DEL temp.txt
for /F %%a in ('findstr /R v10.*.* index.txt') do (
    echo %%a>>temp.txt
)
SET /p NODEVER=<temp.txt
DEL temp.txt

echo Latest v10 node is %NODEVER%
powershell -Command "Invoke-WebRequest https://nodejs.org/dist/%NODEVER%/node-%NODEVER%-win-x64.zip -OutFile node-download.zip"
powershell -Command "Expand-Archive node-download.zip -DestinationPath ."

MOVE .\node-%NODEVER%-win-x64 .\node

SET PATH=%~dp0\node\;%PATH%
CD node
.\npm install -g windows-build-tools
.\npm install -g IamEld3st/RLBotJS
.\npm uninstall -g windows-build-tools
CD ..

powershell -Command "Compress-Archive -Path %~dp0\node\ -DestinationPath rlbot-node.zip"

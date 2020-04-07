# https://nodejs.org/dist/index.tab
# https://nodejs.org/dist/%NODEVER%/node-%NODEVER%-win-x64.zip
import requests
import json
import os
import shutil
from zipfile import ZipFile, PyZipFile
from io import BytesIO


# Find latest LTS node version
index = json.loads(requests.get("https://nodejs.org/dist/index.json").text)
for version_index in index:
    if version_index['lts'] != False:
        latest_lts = version_index
        print(f"Latest LTS is {latest_lts['version']} {latest_lts['lts']}")
        break


# Create build folder and download node
if os.path.exists('./build/'):
    shutil.rmtree('./build/')

node_zip = requests.get(
    f"https://nodejs.org/dist/{latest_lts['version']}/node-{latest_lts['version']}-win-x64.zip").content
uncompressed_data = ZipFile(BytesIO(node_zip))
uncompressed_data.extractall('./')
os.rename(f"./node-{latest_lts['version']}-win-x64/", "./build/")

# Execute build
os.system(".\\build\\npm.cmd install -g windows-build-tools")
os.system(".\\build\\npm.cmd install -g SuperVK/RLBotJS")
os.system(".\\build\\npm.cmd uninstall -g windows-build-tools")

# Zip the dist
if not os.path.exists('./dist/'):
    os.mkdir('./dist/')

with ZipFile(f"./dist/node-rlbot-{latest_lts['version']}-{latest_lts['lts']}.zip", 'w') as zipObj:
    # Iterate over all the files in directory
    for folderName, subfolders, filenames in os.walk('./build/'):
        for filename in filenames:
            # create complete filepath of file in directory
            filePath = os.path.join(folderName, filename)
            # Add file to zip
            zipObj.write(filePath)

shutil.rmtree('./build/')

from datetime import datetime
import os
import requests
import subprocess
import sys
import yaml

config = yaml.safe_load(open("settings.yml"))

def downloadResourceList(url):
  r = requests.get(url)
  return r.text.splitlines()

def parseResourceList(resourceList):
  headers = parseResourceHeaders(resourceList[:3])
  gameFiles = resourceList[3:]

  timestamp = headers[0]
  resCount = headers[1]
  resSize = headers[2]

  print(f"=> Found a resource list generated on {timestamp}")
  print(f"=> It contains {resCount} files for a total size of {resSize} MB")

  print("\n=> Fetching files\n")

  for line in gameFiles:
    items = line.split(',')

    filename = items[0]
    ts = items[1]
    size = f"{round(int(items[2]) / 1000000, 1)} MB"

    print(f"=> Downloading {filename} ({size})")

    r = requests.get(f"{config['root']}/{filename}_{ts}.pkg")

    with open(os.path.join(f"{config['dldir']}", f"{filename}.pkg"), 'wb') as outfile:
      outfile.write(r.content)

def parseResourceHeaders(header):
  ts = header[0]
  resCount = header[1]
  resSize = header[2]

  # Format the filelist timestamp into a valid datetime string
  listGenTime = datetime(int(ts[:4]), int(ts[4:6]), int(ts[6:8]), int(ts[8:10]), int(ts[10:12]), int(ts[12:14])).strftime("%a %B %d %Y at %-I:%M%p")
  # How many files are there to download?
  resCount = int(resCount)
  # Translate file list size from bytes into megabytes
  resSize = round(int(resSize) / 1000000, 2)

  return [listGenTime, resCount, resSize]

def pullAssetStrings():
  assets = os.listdir(config['dldir'])

  for item in assets:
    strings = subprocess.check_output(["strings", f"{config['dldir']}/{item}"])
    
    with open(os.path.join(config['parsedir'], f"{item}.txt"), "wb") as outfile:
      outfile.write(strings)
    
    print(f"=> Parsed {item}. Strings are in {item}.txt")

def getInput():
    print("Please enter the URL of a resource list to parse")
    url = input('> ')

    print("=> Downloading resource list")
    resourceList = downloadResourceList(url)

    print("=> Parsing resource list")
    parseResourceList(resourceList)

    print("Do you want to run strings on the files too? (y/n)")
    strings = input('(y/n): ')
    
    if (strings):
      pullAssetStrings()

    print("=> Done!")

getInput()

def setRunFlagOFF():
    import json
    import os

    statusFile = ".\\runStatus.json"
    with open(statusFile, 'r') as f:
        json_data = json.load(f)
    json_data["runFlag"] = 'stop'  # On this line you needed to add ['embed'][0]
    with open(statusFile, 'w') as f:
        json.dump(json_data, f,indent=2)
setRunFlagOFF()
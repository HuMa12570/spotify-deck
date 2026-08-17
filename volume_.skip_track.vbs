Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "curl -X POST ""http://127.0.0.1:8000/api/location/1/0/2/press""", 0, False
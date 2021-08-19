import os
import sys
import requests
from quart import Quart
from quart import request
from threading import Thread
from time import sleep
import json

if os.name == 'nt':
    os.system("title Spotify for OBS by VihangaTheTurtle")
    os.system("ie4uinit.exe -show")
else:
    sys.stdout.write("\x1b]2;Spotify for OBS by VihangaTheTurtle\x07")

appVersion = "1.2"

print("Running version " + appVersion)

app = Quart(__name__)



def spotyRefresh(code):
    headers = {
        'Authorization': 'Basic ZjM2OTI4OWFjMmQwNGE3M2JiZGFkMjEwOWMyMWVmMWQ6MjU0OWUxNmI4NDVhNDQ1YzkxYWNlMGMyYmQ4OGE2Mzc=',
    }

    data = {
      'grant_type': 'refresh_token',
      'redirect_uri': 'http://localhost:28591',
      'refresh_token': code
    }

    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    return response.text

def spotyAuth(code):
    headers = {
        'Authorization': 'Basic ZjM2OTI4OWFjMmQwNGE3M2JiZGFkMjEwOWMyMWVmMWQ6MjU0OWUxNmI4NDVhNDQ1YzkxYWNlMGMyYmQ4OGE2Mzc=',
    }

    data = {
      'grant_type': 'authorization_code',
      'redirect_uri': 'http://localhost:28591',
      'code': code
    }

    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    return response.text

@app.route('/')
async def main():
    if getattr(sys, 'frozen', False):
        basedir = sys._MEIPASS
    else:
        basedir = basedir = os.path.dirname(sys.argv[0])

    mpath = basedir + "/index.html"
    with open(mpath, 'r') as html:
        return html.read()

@app.route('/refresh')
async def refresh():
    res = request.headers.get('code')
    res = spotyRefresh(res)
    return json.loads(res)["access_token"]
    
@app.route('/verify')
async def verify():
    res = request.headers.get('code')
    res = spotyAuth(res)
    if getattr(sys, 'frozen', False):
        basedir = sys._MEIPASS
    else:
        basedir = basedir = os.path.dirname(sys.argv[0])

    mpath = basedir + "/index.html"
    with open(mpath, 'r') as html:
        try:
            return json.loads(res)["access_token"] + "!" + json.loads(res)["refresh_token"]
        except:
            return "reauth"

@app.route('/auth')
async def auth():
    return '<script>document.location = "https://accounts.spotify.com/authorize?client_id=f369289ac2d04a73bbdad2109c21ef1d&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A28591&scope=user-read-currently-playing"</script>'

def startWServer():
    app.run(host='0.0.0.0', port='28591')

Thread(target=startWServer).start()
sleep(2)
print('Webserver started! Please visit:')
print('    http://localhost:28591')
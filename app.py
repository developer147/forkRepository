import os
import requests

from flask import Flask, request, render_template, redirect, json
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
# MAKE SURE TO CHANGE TO YOUR APP NUMBER!!!!!
#app_id = '301947'
app_id = '302861'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/authorize')
def authorize():
    return redirect('https://github.com/login/oauth/authorize?client_id='
                    #+'Iv1.704767f61055888b'
                    +'Iv1.9af4fde068c2b9f9'
                    +'&redirect_uri='
                    +'https://fork-repo-app.herokuapp.com/'
                    +'&state='
                    +'Nugget123')

@app.route('/forkRepo')
def fork_repo():
    code = request.args.get('code')
    state = request.args.get('state')
    print('code', code, 'state', state)
    #dictToSend = {'client_id':'Iv1.704767f61055888b', 'client_secret': 'd0d97dbb3355db790fd49c644ee84d71f9525bbc', 'code': code, 'redirect_uri': 'https://fork-repo-app.herokuapp.com/accessToken'}
    dictToSend = {'client_id': 'Iv1.9af4fde068c2b9f9', 'client_secret': '77279b0490345a51ba3cb1f4735da28be95a9fbb',
                  'code': code, 'redirect_uri': 'https://fork-repo-app.herokuapp.com/accessToken'}
    headers = {"Accept":"application/json"}
    response = requests.post('https://github.com/login/oauth/access_token', json=dictToSend, headers=headers)
    print("status code", response.status_code)
    json_res = response.json()
    print(response.text)
    #json_data = json.loads(response.text)
    print("access_token", json_res['access_token'], "expires_in", json_res['expires_in'], "refresh_token", json_res['refresh_token'], "refresh_token_expires_in", json_res["refresh_token_expires_in"], "token_type", json_res["token_type"], "scope", json_res["scope"])

    # fork repository code
    # https://docs.github.com/en/rest/repos/forks?apiVersion=2022-11-28#create-a-fork
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer ' + json_res['access_token'],
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = '{"name":"forkRepoClone","default_branch_only":false}'
    response = requests.post('https://api.github.com/repos/developer147/forkRepository/forks', headers=headers, data=data)

    json_res = json.loads(response.text)

    html_url = json_res["html_url"]
    print("HTML URL", json_res["html_url"])

    return redirect(html_url)

@app.route('/accessToken')
def access_token():
    access_token = request.args.get('access_token')
    print('access_token', access_token)
    return 'Ok'

# if __name__ == "__main__":
#     app.run(debug=True, port=9001)
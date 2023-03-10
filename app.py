import os
import requests

from flask import Flask, request, render_template, redirect, json
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
environment_configuration = os.environ['CONFIGURATION_SETUP']
app.config.from_object(environment_configuration)
github_app_client_id = app.config['GITHUB_APP_CLIENT_ID']
redirect_uri_on_authorization = app.config['REDIRECT_URI_ON_AUTHORIZATION']
redirect_state = app.config['REDIRECT_STATE']
github_app_client_secret = app.config['GITHUB_APP_CLIENT_SECRET']
redirect_uri_for_access_token = app.config['REDIRECT_URI_FOR_ACCESS_TOKEN']
github_fork_repo_app_uri = app.config['GITHUB_FORK_REPO_APP_URI']
authorization_uri = app.config['AUTHORIZATION_URI']

@app.route('/')
def index():
    return render_template('index.html', github_app_uri=github_fork_repo_app_uri)

@app.route('/main')
def main():
    return render_template('main.html', auth_uri=authorization_uri)

@app.route('/authorize')
def authorize():
    return redirect('https://github.com/login/oauth/authorize?client_id='
                    + github_app_client_id
                    +'&redirect_uri='
                    + redirect_uri_on_authorization
                    +'&state='
                    + redirect_state)

@app.route('/forkRepo')
def fork_repo():
    code = request.args.get('code')
    state = request.args.get('state')

    dictToSend = {'client_id': github_app_client_id, 'client_secret': github_app_client_secret,
                  'code': code, 'redirect_uri': redirect_uri_for_access_token}
    headers = {"Accept":"application/json"}
    response = requests.post('https://github.com/login/oauth/access_token', json=dictToSend, headers=headers)
    json_res = response.json()

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

    return redirect(html_url)

@app.route('/accessToken')
def access_token():
    access_token = request.args.get('access_token')
    return redirect('/main')

if __name__ == "__main__":
    #app.run(debug=True, port=9001)
    app.run()
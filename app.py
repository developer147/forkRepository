import os
import requests

from flask import Flask, request, render_template, redirect, json
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
environment_configuration = os.environ['CONFIGURATION_SETUP']
app.config.from_object(environment_configuration)
print(f"Environment: {app.config['ENV']}")
print(f"Debug: {app.config['DEBUG']}")

# github_app_id = app.config['GITHUB_APP_ID']
# print(f"Github App ID: {github_app_id}")

github_app_client_id = app.config['GITHUB_APP_CLIENT_ID']
print(f"Github App Client ID: {github_app_client_id}")

redirect_uri_on_authorization = app.config['REDIRECT_URI_ON_AUTHORIZATION']
print(f"Redirect Uri On Authorization: {redirect_uri_on_authorization}")

redirect_state = app.config['REDIRECT_STATE']
print(f"Redirect State: {redirect_state}")

github_app_client_secret = app.config['GITHUB_APP_CLIENT_SECRET']
print(f"Github App Client Secret: {github_app_client_secret}")

redirect_uri_for_access_token = app.config['REDIRECT_URI_FOR_ACCESS_TOKEN']
print(f"Redirect Uri For Access Token: {redirect_uri_for_access_token}")

github_fork_repo_app_uri = app.config['GITHUB_FORK_REPO_APP_URI']
print(f"Github Fork Repo App URI: {github_fork_repo_app_uri}")

authorization_uri = app.config['AUTHORIZATION_URI']
print(f"Authorization URI: {authorization_uri}")


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
    print('code', code, 'state', state)

    dictToSend = {'client_id': github_app_client_id, 'client_secret': github_app_client_secret,
                  'code': code, 'redirect_uri': redirect_uri_for_access_token}
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

if __name__ == "__main__":
    #app.run(debug=True, port=9001)
    app.run()
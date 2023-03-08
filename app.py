import os
import requests

from flask import Flask, request, render_template, redirect, url_for, json
from flask_bootstrap import Bootstrap
from github import Github, GithubIntegration

app = Flask(__name__)
Bootstrap(app)
# MAKE SURE TO CHANGE TO YOUR APP NUMBER!!!!!
app_id = '301947'
# Read the bot certificate
with open(
        os.path.normpath(os.path.expanduser('/Users/jharkar/Downloads/fork-repo-github-app.2023-03-06.private-key.pem')),
        'r'
) as cert_file:
    app_key = cert_file.read()

# Create an GitHub integration instance
git_integration = GithubIntegration(
    app_id,
    app_key,
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/forkRepoInit')
def forkRepoInit():
    # return redirect(url_for('https://github.com/login/oauth/authorize',
    #                         client_id="Iv1.704767f61055888b",
    #                         redirect_uri='https://smee.io/JNYSzlLh34wKUp7d',
    #                         state='Nugget123'))
    return redirect('https://github.com/login/oauth/authorize?client_id='
                    +'Iv1.704767f61055888b'
                    +'&redirect_uri='
                    +'http://127.0.0.1:9001/temporaryCode'
                    +'&state='
                    +'Nugget123')
    #return requests.get('https://github.com/login/oauth/authorize?client_id='+'Iv1.704767f61055888b')

@app.route('/temporaryCode')
def temporary_code():
    code = request.args.get('code')
    state = request.args.get('state')
    print('code', code, 'state', state)
    dictToSend = {'client_id':'Iv1.704767f61055888b', 'client_secret': 'd0d97dbb3355db790fd49c644ee84d71f9525bbc', 'code': code, 'redirect_uri': 'http://127.0.0.1:9001/accessToken'}
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

    data = '{"name":"test2","default_branch_only":false}'
    #response = requests.post('https://github.com/api/v3/repos/developer147/forkRepository/forks', headers=headers, data=data)
    response = requests.post('https://api.github.com/repos/developer147/securesocial/forks', headers=headers, data=data)

    json_res = response.json
    print(json_res)
    #print("message", json_res['message'])

    print("fork repo response status", response.status_code, "text response", response.text)
    return 'Ok'

@app.route('/accessToken')
def access_token():
    access_token = request.args.get('access_token')
    print('access_token', access_token)
    return 'Ok'

@app.route("/", methods=['POST'])
def bot():
    # Get the event payload
    payload = request.json

    # Check if the event is a GitHub PR creation event
    if not all(k in payload.keys() for k in ['action', 'pull_request']) and \
            payload['action'] == 'opened':
        return "ok"

    owner = payload['repository']['owner']['login']
    repo_name = payload['repository']['name']

    # Get a git connection as our bot
    # Here is where we are getting the permission to talk as our bot and not
    # as a Python webservice
    git_connection = Github(
        login_or_token=git_integration.get_access_token(
            git_integration.get_installation(owner, repo_name).id
        ).token
    )
    repo = git_connection.get_repo(f"{owner}/{repo_name}")

    issue = repo.get_issue(number=payload['pull_request']['number'])

    # Call meme-api to get a random meme
    response = requests.get(url='https://meme-api.com/gimme')
    if response.status_code != 200:
        return 'ok'

    # Get the best resolution meme
    meme_url = response.json()['preview'][-1]
    # Create a comment with the random meme
    issue.create_comment(f"![Alt Text]({meme_url})")
    return "ok"


if __name__ == "__main__":
    app.run(debug=True, port=9001)